import json
import os
import pprint
import re

from common import mixins
from apps.ecs import serializers as ecs_ser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.ecs.models import Ecs
from apps.ecs import paginations as ecs_per
from apps.ecs import filters
from uuid import uuid4
from django.conf import settings
from common.validate import MyValidationError
from utils.oss import upload_file
from apps.ecs.tasks import celery_create_ecs_task
from utils.redis_client import rds
from utils.algorithm import generate_plans, score_plan
from utils.loads_file_to_json import file_to_json


class EcsViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    authentication_classes = [JSONWebTokenAuthentication]  #
    pagination_class = ecs_per.PageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.Ecs

    def get_queryset(self):
        return Ecs.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ecs_ser.EcsListSerializer
        if self.action == "create":
            return ecs_ser.EcsCreateSerializer

    def perform_create(self, serializer):
        # todo 这个分布式锁可以做全局封装

        request_id = serializer.data['request_id']

        if not rds.setnx(request_id, request_id):
            raise MyValidationError("请勿重复创建")
        else:
            # 10s过期 防止redis炸
            rds.expire(request_id, 10)

        batch_id = str(uuid4()).replace("-", "")
        celery_create_ecs_task.delay(batch_id, serializer.data['spce_path'], self.request.user.id)

        rds.delete(request_id)
        return {"batch_id": batch_id}


class Ecs2ViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    authentication_classes = []  # JSONWebTokenAuthentication
    pagination_class = ecs_per.PageNumberPagination
    permission_classes = []  # IsAuthenticated
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.Ecs

    def get_queryset(self):
        return Ecs.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ecs_ser.EcsListSerializer
        if self.action == "create":
            return ecs_ser.Ecs2CreateSerializer

    def perform_create(self, serializer):

        request_id = serializer.data['request_id']

        if not rds.setnx(request_id, request_id):
            raise MyValidationError("请勿重复创建")
        else:
            # 10s过期 防止redis炸
            rds.expire(request_id, 10)

        # 分配计划生成plans/下的文件
        plan_fold_path = generate_plans(settings.UPLOAD_PATH + serializer.data['spce_path'])
        plan_fold_list = list(os.walk(plan_fold_path))[0][2]
        socre_input_list = {"serverA": [], "serverB": []}
        # 最后得分
        dispatch_score_dict = dict()
        for i in plan_fold_list:
            with open(settings.BASE_DIR + "/plans/" + i) as f:
                data = json.loads(f.readline())

            for line in data["serverA"]:
                socre_input_list["serverA"].append({
                    "id": int(line.split(",")[0]),
                    "cpu": line.split(",")[1],
                    "memory": line.split(",")[2],
                    "disk": line.split(",")[3],
                })
            for line in data["serverB"]:
                socre_input_list["serverB"].append({
                    "id": int(line.split(",")[0]),
                    "cpu": line.split(",")[1],
                    "memory": line.split(",")[2],
                    "disk": line.split(",")[3],
                })
            # 计算分数
            score = score_plan(socre_input_list)
            if score:
                dispatch_score_dict[score] = data

        # dict根据key排序 取最高分
        highest_score = sorted(dispatch_score_dict.keys())[-1]  # 最高分

        highest_score_score_dict = dispatch_score_dict[highest_score]  # 最高分分配具体详情
        # 求分配搭配serverA和serverB的总配置
        total_serverA = {"cpu": 0, "memory": 0, "disk": 0}
        total_serverB = {"cpu": 0, "memory": 0, "disk": 0}
        pprint.pprint(highest_score_score_dict)
        for line in highest_score_score_dict["serverA"]:
            cpu = re.findall(r'\d+(?:\.\d+)?', line.split(",")[1])

            memory = re.findall(r'\d+(?:\.\d+)?', line.split(",")[2])
            disk = re.findall(r'\d+(?:\.\d+)?', line.split(",")[3])
            total_serverA["cpu"] += int(cpu[0])
            if "Gi" in line:
                total_serverA["memory"] += int(memory[0]) * 1024  # 1g=1024M
            else:
                total_serverA["memory"] += int(memory[0])
            if "Tb" in line:
                total_serverA["disk"] += int(disk[0]) * 1024  # 1g=1024M
            else:
                total_serverA["disk"] += int(disk[0])

        for line in highest_score_score_dict["serverB"]:
            cpu = re.findall(r'\d+(?:\.\d+)?', line.split(",")[1])

            memory = re.findall(r'\d+(?:\.\d+)?', line.split(",")[2])
            disk = re.findall(r'\d+(?:\.\d+)?', line.split(",")[3])
            total_serverB["cpu"] += int(cpu[0])
            if "Gi" in line:
                total_serverB["memory"] += int(memory[0]) * 1024  # 1g=1024M
            else:
                total_serverB["memory"] += int(memory[0])
            if "Tb" in line:
                total_serverB["disk"] += int(disk[0]) * 1024  # 1g=1024M
            else:
                total_serverB["disk"] += int(disk[0])
        # pprint.pprint(highest_score_score_dict)

        # 异步任务
        batch_id = str(uuid4()).replace("-", "")
        celery_create_ecs_task.delay(batch_id, serializer.data['spce_path'], self.request.user.id)
        rds.delete(request_id)

        return {"batch_id": batch_id,
                "highest_score": highest_score, "detail": highest_score_score_dict,
                "serverA": {"cpu": str(total_serverA.get("cpu")) + "核",
                            "memory": str(total_serverA.get("memory")) + "Mi",
                            "disk": str(total_serverA.get("disk")) + "Gb"
                            },
                "serverB": {"cpu": str(total_serverB.get("cpu")) + "核",
                            "memory": str(total_serverB.get("memory")) + "Mi",
                            "disk": str(total_serverB.get("disk")) + "Gb"
                            }
                }


# 文件上传
class FileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ecs_ser.FileCreateSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        file_obj = serializer.validated_data.get('file')
        url = upload_file(file_obj=file_obj, user_id=self.request.user.id)

        return {"url": url}


# 文件上传
class UploadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ecs_ser.FileCreateSerializer
    authentication_classes = []  # JSONWebTokenAuthentication
    permission_classes = []  # IsAuthenticated

    def perform_create(self, serializer):
        file_obj = serializer.validated_data.get('file')
        file_list = file_obj.read().decode().split("\n")
        uid = str(uuid4()).replace("-", "")
        path = f"{uid}-{file_obj.name}"
        with open(settings.UPLOAD_PATH + path, encoding="utf-8", mode="w") as f:
            f.write(json.dumps(file_list, ensure_ascii=False))
        return {"spec_path": path}
