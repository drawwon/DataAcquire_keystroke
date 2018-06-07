#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/7 15:00

from users.models import EmailVerifyRecord
import random,string
from django.core.mail import send_mail
from DataAcquire.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
    email_verify_record = EmailVerifyRecord()
    email_verify_record.email = email
    email_verify_record.code = generate_random_str()
    email_verify_record.send_type = send_type
    email_verify_record.save()
    if send_type == 'register':
        email_title = '西安交大人机交互平台数据采集中心激活邮件'
        email_body = '请点击如下链接激活你的账号:http:/127.0.0.1:8000/active/{}'.format(email_verify_record.code)
    else:
        email_title = '西安交大人机交互平台数据采集中心重置密码邮件'
        email_body = '请点击如下链接重置你的密码:http:/127.0.0.1:8000/reset/{}'.format(email_verify_record.code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass

def generate_random_str():
    chars = string.ascii_letters+string.digits
    random_char = random.sample(chars,10)
    random_char = ''.join(random_char)
    return random_char