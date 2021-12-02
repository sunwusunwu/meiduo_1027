from rest_framework.views import APIView
from random import randint
from django_redis import get_redis_connection
from rest_framework.response import Response
import logging
from meiduo_mall.libs.yuntongxun.sms import CCP
from rest_framework import status
from . import constants

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """短信验证码"""
    def get(self, request, mobile):

        # 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 获取redis获取短信标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({'message':'手机发送验证码频繁,请稍后再试'}, status=status.HTTP_400_BAD_REQUEST)
        # 生成验证码
        sms_code = '%06d' % randint(0, 999999)
        logger.info("获取的验证码:" + sms_code)
        # 创建redis管道，减少连接redis的操作
        pl = redis_conn.pipeline()
        # 存储验证码到redis
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 存储一个获取验证码后的标记，有效期60s
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行管道命令
        pl.execute()
        # 容联云发送短信
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
        # logger.info("mobile:" + mobile)
        # logger.info("sms_code:" + sms_code)
        # logger.info("短信有效时间:" + str(constants.SMS_CODE_REDIS_EXPIRES // 60))
        res = CCP().send_template_sms('15556616638', ['1234', 5], 1)
        # res = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
        # res = send_sms_code.delay(mobile, sms_code) # 触发异步任务
        # logger.info("发送短信结果:" + str(res))
        # 响应
        return Response({"message":'ok'})