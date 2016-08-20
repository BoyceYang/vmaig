# -*- coding: utf-8 -*-
from django.contrib import admin
from vcomments.models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'article__title', 'text')
    list_filter = ('create_time',)
    list_display = ('user', 'article', 'text', 'create_time')
    fields = ('user', 'article', 'parent', 'text')

admin.site.register(Comment, CommentAdmin)
