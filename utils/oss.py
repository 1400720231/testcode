import json
import datetime

import oss2
import time
import hashlib
from random import Random
from django.conf import settings


def upload_file(user_id='', file_obj=None):
    """

    :param user_d: 当前用户的user_id
    :param uid: 当前操作的唯一id
    :param file_obj: 文件对象
    :return:
    """
    media_url = settings.PREFIX + settings.BUCKET_NAME + '.' + settings.END_POINT + '/'
    auth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.END_POINT, settings.BUCKET_NAME)
    suffix = file_obj.name.split('.')[1]  # 文件后缀名字
    # 生成一个唯一文件名
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    filename = f'{year}/{month}/{day}/{user_id}.{suffix}'
    # 还有后缀没有处理，比如.png .pdf具体用到再处理
    res = bucket.put_object(filename, file_obj.file)
    if res.status == 200:
        return media_url + filename
    else:
        # 这个其实没用，因为如果上传不成功，oss2这个包直接raise了，连给你错误信息返回的机会都没有．
        return None


def read_spec_from_oss(oss_path=""):
    """

    :param oss_path: 阿里云oss path
    :return:
    """
    auth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.END_POINT, settings.BUCKET_NAME)
    data = bucket.get_object(oss_path)

    return [i.decode("utf-8").strip("\n") for i in data]
