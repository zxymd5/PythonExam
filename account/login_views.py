from django.db import transaction  # 导入事务
from django.views.decorators.csrf import csrf_exempt  # 跨域访问

from utils.response import json_response


@csrf_exempt
@transaction.atomic
def normal_login(request):
    return json_response(200, 'OK', {
        'user_info': '123456',
        'has_login': bool("True")
    })
