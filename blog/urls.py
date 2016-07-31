# !/usr/bin/python
# -*-coding:utf-8-*-

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import IndexView, UserView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^forget_password/$', TemplateView.as_view(template_name="blog/forget_password.html"),
        name='forget_password-view'),
    url(r'^login/$', TemplateView.as_view(template_name="blog/login.html"),
        name='login-view'),
    url(r'^register/$', TemplateView.as_view(template_name="blog/register.html"),
        name='register-view'),
    url(r'^userctl/(?P<slug>\w+)$', UserView.as_view(), name='user-view'),
]
