from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger('django')


def exception_handler(exc, context):
    # 调用drf原生框架处理异常的方法
    response = drf_exception_handler(exc, context)
    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message':"服务器内部错误"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response