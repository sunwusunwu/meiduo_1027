# -*- coding: utf-8 -*-
# @Time    : 2021/11/15 22:45
# @Author  : Sunwu
from celery_tasks.main import celery_app
from django.core.mail import send_mail
from django.conf import settings


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
    发送激活邮箱
    :param to_email:
    :param verify_url:
    :return:
    """
    subject = "美多商城邮箱验证"  # 邮件主题/标题
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">请点击链接确认<a></p>' % (to_email, verify_url)
    # send_mail(subject:标题, message:普通邮件正文, 发件人, [收件人], html_message=超文本的邮件内容)
    send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)