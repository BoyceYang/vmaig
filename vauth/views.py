# !/usr/bin/python
# -*-coding:utf-8-*-

import json
import logging

from django.contrib import auth
from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from .forms import VmaigUserCreationForm, VmaigPasswordRestForm

LOG = logging.getLogger(__name__)

# Create your views here.


class VauthControl(View):
    def post(self, request, *args, **kwargs):

        slug = self.kwargs.get('slug')
        if slug == 'login':
            return self._login()
        elif slug == 'logout':
            return self._logout()
        elif slug == 'register':
            return self._register()

    def _login(self):
        username = self.request.POST.get("username", "")
        password = self.request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)

        errors = []

        if user is not None:
            auth.login(self.request, user)
        else:
            errors.append(u"密码或者用户名不正确")

        my_dict = {"errors": errors}
        return HttpResponse(
            json.dumps(my_dict),
            content_type="application/json"
        )

    def _logout(self):
        if not self.request.user.is_authenticated():
            LOG.error(u'[UserControl]用户未登陆')
            raise PermissionDenied
        else:
            auth.logout(self.request)
            return HttpResponse('OK')

    def _register(self):
        username = self.request.POST.get("username", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")
        email = self.request.POST.get("email", "")

        form = VmaigUserCreationForm(self.request.POST)

        errors = []
        # 验证表单是否正确
        if form.is_valid() and password1 == password2:
            current_site = get_current_site(self.request)
            site_name = current_site.name
            domain = current_site.domain
            title = u"欢迎来到 {} ！".format(site_name)
            message = "".join([
                u"你好！ {} ,感谢注册 {} ！\n\n".format(username, site_name),
                u"请牢记以下信息：\n",
                u"用户名：{}\n".format(username),
                u"邮箱：{}\n".format(email),
                u"网站：http://{}\n\n".format(domain),
            ])
            from_email = None
            try:
                send_mail(title, message, from_email, [email])
            except Exception as e1:
                LOG.error(
                    u'[UserControl]用户注册邮件发送失败:[{}]/[{}]/[{}]'.format(
                        username, email, e1
                    )
                )
                return HttpResponse(u"发送邮件错误!\n注册失败", status=500)

            form.save()
            user = auth.authenticate(username=username, password=password1)
            auth.login(self.request, user)

        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        my_dict = {"errors": errors}
        return HttpResponse(
            json.dumps(my_dict),
            content_type="application/json"
        )

    def _forget_password(self):
        username = self.request.POST.get("username", "")
        email = self.request.POST.get("email", "")

        form = VmaigPasswordRestForm(self.request.POST)
        errors = []

        # 验证表单是否正确
        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            opts = {
                'token_generator': token_generator,
                'from_email': from_email,
                'request': self.request,
            }
            user = form.save(**opts)
        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
        my_dict = {"errors": errors}
        return HttpResponse(
            json.dumps(my_dict),
            content_type="application/json"
        )
