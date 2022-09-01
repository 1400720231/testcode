from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from apps.ecs import views as ecs_view
from apps.user import views as user_view

router = DefaultRouter(trailing_slash=False)
# ecs
router.register(r'ecs', ecs_view.EcsViewSet, basename='ecs')
router.register('file', ecs_view.FileViewSet, basename="file")  # 文件上传

# user
router.register(r'login', user_view.LoginViewSet, basename='login')
router.register(r'user', user_view.UserViewSet, basename='user')
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'api/v1/', include(router.urls)),
]
