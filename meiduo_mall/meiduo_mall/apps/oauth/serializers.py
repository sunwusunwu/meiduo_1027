# -*- coding:utf-8 -*-
# Author : Sunwu
# Date : 2021/11/9 14:05
from django_redis import get_redis_connection
from rest_framework import serializers

from .utils import check_save_user_token
from users.models import User
from .models import OAuthQQUser


class QQAuthUserSerializer(serializers.Serializer):
    """openid 绑定用户的序列化器"""
    # mobile  password  sms_code  access_token
    access_token = serializers.CharField(label='操作凭证')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')

    def validate(self, attrs):
        # 1.把加密的openid 取出来 加密
        access_token = attrs.pop('access_token')
        openid = check_save_user_token(access_token)
        if openid is None:
            raise serializers.ValidationError('openid无效')
        # 1.1 把原本的openid 重新添加到attrs 字典(以备后期create方法中绑定使用)
        attrs['openid'] = openid

        # 2. 校验验证码
        # 校验验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        # 向redis存储数据时都是以字条串进行存储的,取出来后都是bytes类型 [bytes]

        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('验证码错误')

        # 3.拿手机号查询 user表 如果能查到说明手机号已注册,如果已注册再绑定密码是否和用户匹配
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(attrs['password']) is False:
                raise serializers.ValidationError('密码错误')
            else:
                # 如果用户已存在,并且密码也正确 把当前的user对象存储到反序列化大字典中以备后期绑定使用
                attrs['user'] = user

        return attrs

    def create(self, validated_data):
        # 1.获取validated_data中的user,如果能取到user说明用户已存在
        user = validated_data.get('user')
        if user is None:
            # 2.如果validated_data 里面没有取出user,创建一个新用户
            user = User(
                username=validated_data.get('mobile'),
                mobile=validated_data.get('mobile')
            )
            user.set_password(validated_data.get('password'))
            user.save()
        # 3. 把openid和user绑定
        OAuthQQUser.objects.create(
            openid=validated_data.get('openid'),
            user=user
        )

        # 4.把user返回
        return user
