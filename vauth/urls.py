# !/usr/bin/python
# -*-coding:utf-8-*-

from django.conf.urls import url
from .views import VauthControl


urlpatterns = [
    url(r'^vauth/(?P<slug>\w+)$', VauthControl.as_view()),
]
