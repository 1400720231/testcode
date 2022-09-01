from common import mixins
from apps.user import serializers as user_ser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.user.models import User
from apps.user import paginations as user_per
from apps.user import filters as user_filter


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    authentication_classes = []  # JSONWebTokenAuthentication
    pagination_class = user_per.PageNumberPagination
    permission_classes = []  # IsAuthenticated
    filter_backends = (DjangoFilterBackend,)
    filterset_class = user_filter.UserFilter

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return user_ser.UserListSerializer
