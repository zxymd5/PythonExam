import base64
import uuid
from io import BytesIO

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction  # 导入事务
from django.views.decorators.csrf import csrf_exempt  # 跨域访问

from account.models import Profile

from utils.errors import UserError
from utils.redis.rprofile import (get_vcode, set_profile, set_vcode)

from utils.response import json_response
from utils.codegen import get_pic_code


@csrf_exempt
@transaction.atomic
def normal_login(request):
    """
    普通视图登录
    :param request: 请求对象
    :return: 返回json数据：user_info：用户信息；has_login：用户是否已登录
    """
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    sign = request.POST.get('sign', '')
    vcode = request.POST.get('vcode', '')
    result = get_vcode(sign)
    if not (result and (result.decode('utf-8') == vcode.lower())):
        return json_response(*UserError.VeriCodeError)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return json_response(*UserError.UserNotFound)
    user = authenticate(request, username=user.username, password=password)
    if user is not None:
        login(request, user)
        profile, created = Profile.objects.select_for_update().get_or_create(email=user.email)
        if profile.user_src != Profile.COMPANY_USER:
            profile.name = user.username
            profile.user_src = Profile.NORMAL_USER
            profile.save()
        request.session['uid'] = profile.uid
        request.session['username'] = profile.name
        set_profile(profile.data)
    else:
        return json_response(*UserError.PasswordError)
    return json_response(200, 'OK', {
        'user_info': profile.data,
        'has_login': bool(profile)
    })


def login_vcode(request):
    b = BytesIO()
    img, check = get_pic_code()
    img.save(b, format("png"))

    vcode = base64.b64encode(b.getvalue())
    sign = str(uuid.uuid1())
    set_vcode(sign, ''.join([str(i) for i in check]).lower())

    return json_response(200, 'OK', {
        'vcode': vcode.decode('utf-8'),
        'sign': sign
    })
