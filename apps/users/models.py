from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    birthday = models.DateField(verbose_name='生日',default='1900-01-01')
    age = models.IntegerField(verbose_name='年龄',default=0)
    gender = models.CharField(max_length=10,verbose_name='性别',choices=(('male','男'),('female','女')),default='')
    address = models.CharField(max_length=100,default='')
    mobile = models.CharField(max_length=11,null=True,blank=True,default='')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name= '邮箱')
    send_type = models.CharField(choices=(('register','注册'),('forget','找回密码')),max_length=10,verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间') #记得去掉datetime.now的括号，不然只会记录class生成的时间
    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)