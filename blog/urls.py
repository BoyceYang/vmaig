# !/usr/bin/python
# -*-coding:utf-8-*-

from django.conf.urls import url

from .views import IndexView, ArticleView, AllView, ColumnView, CategoryView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^article/(?P<slug>\w+).html$', ArticleView.as_view(), name='article-detail-view'),

    url(r'^all/$', AllView.as_view(), name='all-view'),
    url(r'^column/(?P<column>\w+)/$', ColumnView.as_view(), name='column-detail-view'),
    url(r'^category/(?P<category>\w+)/$', CategoryView.as_view(), name='category-detail-view'),
]
