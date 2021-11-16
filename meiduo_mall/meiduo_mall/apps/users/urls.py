# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 14:45
# @Author  : Sunwu
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    url(r'^users/$', views.UserView.as_view()),  # 注册用户
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),  # 判断用户名是否已注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),  # 判断手机号是否已注册
    url(r'^authorizations/$', obtain_jwt_token),  # jwt登录
    url(r'^user/$', views.UserDetailView.as_view()),  # 用户中心详情
    url(r'^email/$', views.EmailView.as_view()),  # 设置邮箱并保存
    url(r'^emails/verification/$', views.EmailVerifyView.as_view()),  # 激活邮箱
]