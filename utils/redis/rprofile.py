import json

from utils.jsonencoder import JsonEncoder
from utils.redis.connect import r
from utils.redis.constants import (REDIS_USER_INFO, USER_SIGN_VCODE, )


def set_profile(data={}):
    if isinstance(data, dict):
        uid = data.get('uid', '')
        key = REDIS_USER_INFO % uid
        data = json.dumps(data, cls=JsonEncoder)
        r.set(key, data)


def set_vcode(sign, value):
    key = USER_SIGN_VCODE % sign
    r.setex(key, 90000, value)


def get_vcode(sign):
    key = USER_SIGN_VCODE % sign
    return r.get(key)
