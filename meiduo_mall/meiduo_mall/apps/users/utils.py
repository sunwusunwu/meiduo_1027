# -*- coding: utf-8 -*-
# @Time    : 2021/10/26 21:30
# @Author  : Sunwu



def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数,多追加 user_id和username"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }
