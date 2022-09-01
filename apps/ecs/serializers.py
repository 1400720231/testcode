from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.ecs import models as md
from common.validate import MyValidationError

User = get_user_model()


class EcsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = md.Ecs
        fields = "__all__"


# 创建服务器资源表单
class EcsCreateSerializer(serializers.Serializer):
    spce_path = serializers.CharField(help_text='配置文件的oss path', max_length=256, required=True, allow_blank=False,
                                      error_messages={
                                          "max_length": "最大长度不应该超过256个字符",
                                          "required": "该字段必传",
                                          "allow_blank": "该字段必填"
                                      })

    def validate(self, attrs):
        if 1:
            raise MyValidationError("配置文件错误")

        return attrs


# 文件上传
class FileCreateSerializer(serializers.Serializer):
    file = serializers.FileField(help_text="上传文件对象", required=True,
                                 allow_empty_file=False,
                                 error_messages={
                                     "allow_empty_file": "文件内容为空",
                                     "required": "该字段必传",
                                     "allow_blank": "该字段必填"
                                 })


