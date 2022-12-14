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

from common.validate import MyValidationError
from utils.oss import upload_file
from apps.ecs.tasks import celery_create_ecs_task
from utils.redis_client import rds


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


# 文件上传
class FileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ecs_ser.FileCreateSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        file_obj = serializer.validated_data.get('file')
        url = upload_file(file_obj=file_obj, user_id=self.request.user.id)

        return {"url": url}
