<<<<<<< HEAD
# -*- coding:utf-8 -*-
# Author : Sunwu
# Date : 2021/11/18 10:44
from rest_framework import serializers

=======
# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 21:53
# @Author  : Sunwu
from rest_framework import serializers
>>>>>>> origin/master
from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    """省的序列化器?"""

=======
    """行政区序列化器"""
>>>>>>> origin/master
    class Meta:
        model = Area
        fields = ['id', 'name']


class SubsSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    # 130000
    # 河北省模型.subs.all()
    """详情视图使用的序列化器"""
    subs = AreaSerializer(many=True)
    # subs = serializers.PrimaryKeyRelatedField()  # 只会序列化出 id
    # subs = serializers.StringRelatedField()  # 序列化的时模型中str方法返回值

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
=======
    """某一行政区下面的详情行政区序列器"""
    subs = AreaSerializer(many=True) # 反向查询某个行政区的所有关联行政区

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']

>>>>>>> origin/master
