# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from blog.models import Article

from utils import StringOfTitle

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    article = models.ForeignKey(Article, verbose_name=u'文章')
    text = models.TextField(verbose_name=u'评论内容')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name=u'引用')

    class Meta:
        verbose_name_plural = verbose_name = u'评论'
        ordering = ['-create_time']
        app_label = StringOfTitle('vcomments', u"评论管理")

    def __unicode__(self):
        return self.text

    __str__ = __unicode__

