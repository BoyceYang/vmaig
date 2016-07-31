# !/usr/bin/python
# -*-coding:utf-8-*-

import json
import logging

from django.contrib import auth
from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site

from .forms import VmaigUserCreationForm

logger = logging.getLogger(__name__)

# Create your views here.


class UserControl(View):
    def post(self, request, *args, **kwargs):
        # 获取要对用户进行什么操作
        slug = self.kwargs.get('slug')
        if slug == 'login':
            return self._login(request)
        elif slug == 'logout':
            return self._logout(request)
        elif slug == 'register':
            return self._register(request)

    def get(self, request, *args, **kwargs):
        # 如果是get请求直接返回404页面
        raise Http404

    def _login(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)

        errors = []

        if user is not None:
            auth.login(request, user)
        else:
            errors.append(u"密码或者用户名不正确")

        my_dict = {"errors": errors}
        return HttpResponse(
            json.dumps(my_dict),
            content_type="application/json"
        )

    def _logout(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse('OK')

    def _register(self, request):
        username = self.request.POST.get("username", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")
        email = self.request.POST.get("email", "")

        form = VmaigUserCreationForm(request.POST)

        errors = []
        # 验证表单是否正确
        if form.is_valid():
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
                logger.error(
                    u'[UserControl]用户注册邮件发送失败:[{}]/[{}]/[{}]'.format(
                        username, email, e1
                    )
                )
                return HttpResponse(u"发送邮件错误!\n注册失败", status=500)

            new_user = form.save()
            user = auth.authenticate(username=username, password=password1)
            auth.login(request, user)

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
