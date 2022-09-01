from django.contrib.auth import authenticate
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from common import mixins
from apps.user import serializers as user_ser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.user import paginations as user_per
from apps.user import filters as user_filter


# 登录
class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = user_ser.LoginFormSerializer
    authentication_classes = []
    permission_classes = []

    def perform_create(self, serializer):

        data = serializer.validated_data
        user = authenticate(**{"username": data["username"], "password": data["password"]})

        if user:
            payload = jwt_payload_handler(user)
            res_data = {
                "token": jwt_encode_handler(payload),  # jwt_token
                "username": user.username,
                "user_id": user.pk,
            }
        else:
            res_data = {
                "token": '',  # jwt_token
                "user_id": '',  #
                "username": ""

            }

        return res_data


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    pass

