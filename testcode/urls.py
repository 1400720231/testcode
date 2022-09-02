from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from apps.ecs import views as ecs_view
from apps.user import views as user_view

router = DefaultRouter(trailing_slash=False)
# ecs
router.register(r'ecs2', ecs_view.Ecs2ViewSet, basename='ecs2')  # 用本地文件创建虚拟机
router.register('upload', ecs_view.UploadViewSet, basename="upload")  # 文件上传到本地磁盘
# user
router.register(r'login', user_view.LoginViewSet, basename='login')
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'api/v1/', include(router.urls)),
]
