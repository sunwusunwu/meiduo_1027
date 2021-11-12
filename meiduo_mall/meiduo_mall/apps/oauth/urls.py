# -*- coding:utf-8 -*-
# Author : Sunwu
# Date : 2021/11/9 14:04
from django.conf.urls import url

from . import views


urlpatterns = [
    # 拼接QQ登录url
    url(r'^qq/authorization/$', views.QQOauthURLView.as_view()),
    # QQ登录后的回调
    url(r'^qq/user/$', views.QQAuthUserView.as_view()),
]