from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
<<<<<<< HEAD
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
=======
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
>>>>>>> origin/master

from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer, UserAddressSerializer, \
    AddressTitleSerializer
from rest_framework.views import APIView
from .models import User, Address
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging

logger = logging.getLogger('django')


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
        return  self.request.user


class EmailVerifyView(APIView):
    """激活邮箱"""
    def get(self, request):
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message':'用户信息异常'}, status=status.HTTP_400_BAD_REQUEST)
        # 解密token查询user
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '激活失败'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
<<<<<<< HEAD
        # 响应
        return Response({'message': 'ok'})


class AddressViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
=======


class AddressViewSet(UpdateModelMixin, GenericViewSet):
>>>>>>> origin/master
    """用户收货地址增删改查"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer

<<<<<<< HEAD
    # 获取地址查询集，方法重写，正向和反向都可以查询
=======
    # 获取地址查询集，方法重写，正向胡总和反向都可以查询
>>>>>>> origin/master
    def get_queryset(self):
        # return Address.objects.filter(is_deleted=False)
        return self.request.user.addresses.filter(is_deleted=False)

    # 新增用户地址
<<<<<<< HEAD
    def create(self, request, *args, **kwargs):
        user = request.user
        # count = user.addresses.all().count() # 反向关联查询
        count = Address.objects.filter(user=user).count()  # 正向查询
        if count > 20:
            return Response({'message': '收货地址数量达到上限'}, status=status.HTTP_400_BAD_REQUEST)
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)
=======
    def create(self, request):
        user = request.user
        # count = user.addresses.all().count() # 反向关联查询
        count = Address.objects.filter(user=user).count() # 正向查询
        if count > 20:
            return Response({'message':'收货地址数量达到上限'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
>>>>>>> origin/master

    # 获取地址列表
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
<<<<<<< HEAD
        # logger.info('default_address:' + str(user.default_address))
=======
>>>>>>> origin/master
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': 20,
            'addresses': serializer.data,
        })

    # 删除收货地址
    def destroy(self, request, *args, **kwargs):
        address = self.get_object()
        address.is_deleted = True
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 修改收获地址标题
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        address = self.get_object()
        serializer = AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # 设置默认地址
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        address = self.get_object()
<<<<<<< HEAD
        logger.info('address:' + str(request.user.default_address))
        request.user.default_address = address
        request.user.save()
        logger.info('user:' + str(request.user.default_address.title))
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)
=======
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)
>>>>>>> origin/master
