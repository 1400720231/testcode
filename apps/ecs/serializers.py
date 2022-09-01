from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.ecs import models as md

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
