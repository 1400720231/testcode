# -*- coding:utf-8 -*-
from django.conf import settings
from redis import StrictRedis


def _get_redis_client(uri, **kwargs):

    return StrictRedis.from_url(uri, **kwargs)


rds = _get_redis_client(settings.REDIS_URI, decode_responses=True)
