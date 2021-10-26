# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 22:48
# @Author  : Sunwu

from celery_tasks.sms.yuntongxun.sms import CCP
from celery_tasks.sms import constants
from celery_tasks.main import celery_app


@celery_app.task(name='send_sms_code') # 注册任务
def send_sms_code(mobile, sms_code):
    """
    发送短信异步任务
    @param mobile: 手机号
    @param sms_code: 验证码
    @return: None
    """
    CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
