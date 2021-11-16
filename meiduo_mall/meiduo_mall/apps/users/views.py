from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """校验用户名是否已存在"""
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class MobileCountView(APIView):
    """校验手机号是否已存在"""
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'username': mobile,
            'count': count
        }
        return Response(data)


class UserDetailView(RetrieveAPIView):
    """用户信息展示"""
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class EmailView(UpdateAPIView):
    """保存邮箱"""
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user


class EmailVerifyView(APIView):
    """激活邮箱"""
    def get(self, request):
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '用户信息异常'}, status=status.HTTP_400_BAD_REQUEST)
        # 解密token查询user
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '激活失败'}, status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()
        # 响应
        return Response({'message': 'ok'})