import copy
from rest_framework.permissions import BasePermission
from .validate import MyValidationError

"""
    自定义的公共权限模块.
"""


class ExamplePermission(BasePermission):
    raise MyValidationError(code=403, detail="请进行实名认证")
