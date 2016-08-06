# !/usr/bin/python
# -*-coding:utf-8-*-

from django.conf.urls import url

from .views import IndexView, ArticleView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^article/(?P<slug>\w+).html$', ArticleView.as_view(), name='article-detail-view'),
]
