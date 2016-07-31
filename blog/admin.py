# !/usr/bin/python
# -*-coding:utf-8-*-

from django.contrib import admin

# Register your models here.
from .models import Nav, Category, Carousel, Column, News, Article


class CategoryAdmin(admin.ModelAdmin):
    search_fields = (u'name',)
    list_filter = (u'status', u'create_time')
    list_display = (u'name', u'parent', u'rank', u'status')
    fields = (u'name', u'parent', u'rank', u'status')


class ArticleAdmin(admin.ModelAdmin):
    search_fields = (u'title', u'summary',)
    list_filter = (u'status', u'category', u'is_top', u'create_time', u'update_time')
    # list_display = (u'title', u'category', u'author', u'status', u'is_top', u'update_time',)
    list_display = (u'title', u'category', u'status', u'is_top', u'update_time',)
    fieldsets = (
        (u'基本信息', {
            u'fields': (
                u'title', u'en_title', u'img', u'category', u'tags', u'author', u'is_top', u'rank', u'status',
            )
        }),
        (u'内容', {
            u'fields': (
                u'content',
            )
        }),
        (u'摘要', {
            u'fields': (
                u'summary',
            )
        }),
        (u'时间', {
            u'fields': (
                u'pub_time',
            )
        }),
    )


class NewsAdmin(admin.ModelAdmin):
    search_fields = (u'title', u'summary',)
    list_filter = (u'news_from', u'create_time',)
    list_display = (u'title', u'news_from', u'url', u'create_time',)
    fields = (u'title', u'news_from', u'url', u'summary', u'pub_time',)


class NavAdmin(admin.ModelAdmin):
    search_fields = (u'name',)
    list_filter = (u'status', u'create_time',)
    list_display = (u'name', u'url', u'status', u'create_time',)
    fields = (u'name', u'url', u'status')


class ColumnAdmin(admin.ModelAdmin):
    search_fields = (u'name',)
    list_filter = (u'status', u'create_time',)
    list_display = (u'name', u'status', u'create_time',)
    fields = (u'name', u'status', u'article', u'summary')
    filter_horizontal = (u'article', )


class CarouselAdmin(admin.ModelAdmin):
    search_fields = (u'title',)
    list_display = (u'title', u'article', u'img', u'create_time', )
    list_filter = (u'create_time',)
    fields = (u'title', u'article', u'img', u'summary',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Nav, NavAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Carousel, CarouselAdmin)



