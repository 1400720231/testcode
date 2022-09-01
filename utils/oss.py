import oss2
import time
import hashlib
from random import Random
from django.conf import settings


def upload_file(user_d='', uid='', file_obj=None):
    media_url = settings.PREFIX + settings.BUCKET_NAME + '.' + settings.END_POINT + '/'
    auth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.END_POINT, settings.BUCKET_NAME)
    suffix = file_obj.name.split('.')[1]  # 文件后缀名字
    # 生成一个唯一文件名
    filename = f'{user_d}/{uid}.{suffix}'
    # 还有后缀没有处理，比如.png .pdf具体用到再处理
    res = bucket.put_object(filename, file_obj.file)
    if res.status == 200:
        return media_url + filename
    else:
        # 这个其实没用，因为如果上传不成功，oss2这个包直接raise了，连给你错误信息返回的机会都没有．
        return None
