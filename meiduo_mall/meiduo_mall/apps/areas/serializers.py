# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 21:53
# @Author  : Sunwu
from rest_framework import serializers
from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    """行政区序列化器"""
    class Meta:
        model = Area
        fields = ['id', 'name']


class SubsSerializer(serializers.ModelSerializer):
    """某一行政区下面的详情行政区序列器"""
    subs = AreaSerializer(many=True) # 反向查询某个行政区的所有关联行政区

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']

