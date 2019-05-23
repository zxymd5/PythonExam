from account import login_views
from django.urls import path

# account
urlpatterns = [
    path('login_normal', login_views.normal_login, name='normal_login'),
    path('login_vcode', login_views.login_vcode, name='login_qrcode'),
]