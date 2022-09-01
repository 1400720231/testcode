from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.ecs import models as md

User = get_user_model()


class EcsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = md.Ecs
        fields = "__all__"
