from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.user import models as md

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = md.User
        fields = "__all__"
