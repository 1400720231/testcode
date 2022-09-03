# coding:utf-8

from testcode.celery import app as celery_app
from apps.ecs.models import Ecs
from utils.oss import read_spec_from_oss


@celery_app.task
def celery_create_ecs_task(batch_id, oss_path, user_id):
    """
    :param batch_id: 这次创建的虚拟机的批次号
    :param oss_path: oss_path
    :param user_id:
    :return:
    """
    # 异步实际创建虚拟机api接口的伪代码，前端可根据返回的batch_id查询返回当前
    # 资源对象创建的状态
    pass
    # spec_data = read_spec_from_oss(oss_path)
    # for i in spec_data:
    #     Ecs.objects.create(**{
    #         "user_id": user_id,
    #         "batch_id": batch_id,
    #         "code": i.split(",")[0],
    #         "cpu": i.split(",")[0],
    #         "memory": i.split(",")[0],
    #         "disk": i.split(",")[0],
    #         "original_specs": oss_path
    #     })
