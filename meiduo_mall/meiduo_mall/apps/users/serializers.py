# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 17:47
# @Author  : Sunwu
import re
from rest_framework import serializers
from .models import User, Address
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings
from celery_tasks.email.tasks import send_verify_email


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    # 序列化器所有字段[id, username, password, password2, mobile, sms_code, allow]
    # 序列化字段[username, mobile]
    # 反序列化字段[username, password, password2, mobile, sms_code, allow]
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow', 'token']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            }
        }

    def validate_mobile(self, value):
        """校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    def validate_allow(self, value):
        """校验是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请先勾选用户协议')
        return value

    def validate(self, attrs):
        """校验密码和验证码"""
        # 校验密码
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次输入密码不一致')
        # 校验验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if attrs['sms_code'] == '':
            raise serializers.ValidationError('请先输入验证码')
        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('验证码不正确')
        return attrs

    @staticmethod
    def create(validated_data):
        """保存数据"""
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的叫jwt_payload_handler函数(生成payload)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用 生成jwt

        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成完整的jwt
        user.token = token
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户中心序列化器"""
    class Meta:
        model = User
        fields =['id', 'mobile', 'username', 'email', 'email_active']


class EmailSerializer(serializers.ModelSerializer):
    """更新和激活邮箱"""
    class Meta:
        model = User
        fields = ['id', 'email']
        extra_kwargs = {
            'email':{
                'required':True
            }
        }

    def update(self, instance, validated_data):
        """重写update方法，为了加上激活邮箱功能"""
        instance.email = validated_data.get('email')
        instance.save()
        # 拼接发送到第三方邮箱的url
        verify_url = instance.generate_email_verify_url()
        send_verify_email.delay(instance.email, verify_url=verify_url)
        return instance



class UserAddressSerializer(serializers.ModelSerializer):
    """用户收获地址序列化器"""
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省id', required=True)
    city_id = serializers.IntegerField(label='市id', required=True)
    district_id = serializers.IntegerField(label='区id', required=True)

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def validate_mobile(self, value):
        """校验手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        # return Address.objects.create(**validate_data)
        return super().create(validated_data)


class AddressTitleSerializer(serializers.ModelSerializer):
    """地址标题"""
    class Meta:
        model = Address

    def create(self, validate_data):
        user = self.context['request'].user
        validate_data['user'] = user
        address = Address.objects.create(**validate_data)
        return address

