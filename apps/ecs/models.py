from django.db import models
from django.contrib.auth.models import AbstractUser


class Ecs(models.Model):
    user_id = models.IntegerField(default=0, verbose_name="用户id")
    server_id = models.CharField(default="", verbose_name="目标机器的id,比如serverA serverB", max_length=32)
    status = models.CharField(default="", verbose_name="创建的状态,0创建中1创建成功2创建失败", max_length=32)
    batch_id = models.CharField(default="", verbose_name="操作的批次号", max_length=32)
    code = models.CharField(default="", verbose_name="唯一标识", max_length=32)
    cpu = models.CharField(default="", verbose_name="cpu型号", max_length=32)
    memory = models.CharField(default="", verbose_name="内存大小", max_length=32)
    disk = models.CharField(default="", verbose_name="硬盘存储大小", max_length=32)
    original_specs = models.CharField(default="", verbose_name="原始上传配置的文件oss地址", max_length=256)
    reason = models.CharField(default="", verbose_name="创建失败原因", max_length=256)
    request_content = models.TextField(default="", verbose_name="调用创建虚拟机对象的请求原文")
    response_content = models.TextField(default="", verbose_name="调用创建虚拟机对象的响应原文")
