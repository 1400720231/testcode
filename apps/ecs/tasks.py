# coding:utf-8

from testcode.celery import app as celery_app


@celery_app.task
def celery_create_ecs_task():
    pass
