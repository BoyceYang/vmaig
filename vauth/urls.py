# !/usr/bin/python
# -*-coding:utf-8-*-

from django.conf.urls import url
from .views import UserControl


urlpatterns = [
    url(r'^user/(?P<slug>\w+)$', UserControl.as_view()),
]
