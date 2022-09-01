from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from common.validate import MyValidationError

User = get_user_model()


# 登录表单
class LoginFormSerializer(serializers.Serializer):
    username = serializers.CharField(help_text='系统账户名', max_length=150, required=True, allow_blank=False,
                                     error_messages={
                                         "max_length": "最大长度不应该超过150个字符",
                                         "required": "该字段必传",
                                         "allow_blank": "该字段必填"
                                     })
    password = serializers.CharField(help_text="密码", max_length=128, required=True, allow_blank=False,
                                     error_messages={
                                         "max_length": "最大长度不应该超过128个字符",
                                         "required": "该字段必传",
                                         "allow_blank": "该字段必填"
                                     })

    def validate(self, attrs):
        user = authenticate(**{"username": attrs.get('username'), "password": attrs.get('password')})
        if not user:
            raise MyValidationError("账户名或密码错误")

        return attrs
