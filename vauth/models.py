# !/usr/bin/python
# -*-coding:utf-8-*-

from __future__ import unicode_literals
from utils import StringOfTitle

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class VmaigUser(AbstractUser):
    img = models.CharField(max_length=200, default='/static/tx/default.jpg',
                           verbose_name=u'头像地址')
    intro = models.CharField(max_length=200, blank=True, null=True,
                             verbose_name=u'简介')

    class Meta(AbstractUser.Meta):
        app_label = StringOfTitle('vauth', u"用户管理")