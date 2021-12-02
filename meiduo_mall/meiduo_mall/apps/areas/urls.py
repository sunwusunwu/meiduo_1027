<<<<<<< HEAD
# -*- coding:utf-8 -*-
# Author : Sunwu
# Date : 2021/11/18 10:44
from rest_framework.routers import DefaultRouter

from . import views

=======
# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 21:50
# @Author  : Sunwu
from rest_framework.routers import DefaultRouter

from areas import views
>>>>>>> origin/master

router = DefaultRouter()
router.register(r'areas', views.AreaViewSet, basename='area')
urlpatterns = [

]
urlpatterns += router.urls