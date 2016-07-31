# !/usr/bin/python
# -*-coding:utf-8-*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import VmaigUser
from .forms import VmaigUserCreationForm

# Register your models here.


class VmaigUserAdmin(UserAdmin):
    add_form = VmaigUserCreationForm
    add_fieldsets = (
        (None, {
            u'classes': (u'wide',),
            u'fields': (u'username', u'email', u'password1', u'password2',)
        }),
    )
    fieldsets = (
        (u'基本信息', {u'fields': (u'username', u'password', u'email')}),
        (u'权限', {u'fields': (u'is_active', u'is_staff', u'is_superuser')}),
        (u'时间信息', {u'fields': (u'last_login', u'date_joined')}),
    )

admin.site.unregister(Group)
admin.site.register(VmaigUser, VmaigUserAdmin)
