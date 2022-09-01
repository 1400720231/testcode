from django.db import models
from django.contrib.auth.models import AbstractUser


class Ecs(models.Model):
    user_id = models.IntegerField(default=0, verbose_name="用户id")
    batch_id = models.CharField(default="", verbose_name="操作的批次号", max_length=32)
    code = models.CharField(default="", verbose_name="唯一标识", max_length=32)
    cpu = models.CharField(default="", verbose_name="cpu型号", max_length=32)
    memory = models.CharField(default="", verbose_name="内存大小", max_length=32)
    disk = models.CharField(default="", verbose_name="硬盘存储大小", max_length=32)
    original_specs = models.CharField(default="", verbose_name="原始上传配置的文件oss地址", max_length=256)
