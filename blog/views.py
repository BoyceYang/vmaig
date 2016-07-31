# !/usr/bin/python
# -*-coding:utf-8-*-

import logging

from django.conf import settings
from django.shortcuts import render
from django.core.cache import caches
from django.views.generic import ListView, TemplateView

from .models import Article, Nav, Carousel

# Cache
try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']

# Logger
LOG = logging.getLogger(__name__)

# Create your views here.


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 网站标题等内容
            context['website_title'] = settings.WEBSITE_TITLE
            context['website_welcome'] = settings.WEBSITE_WELCOME
            # 热门文章
            context['hot_article_list'] = Article.objects.order_by(u"-view_times")[0:10]
            # 导航条
            context['nav_list'] = Nav.objects.filter(status=0)
            # 最新评论
            # context['latest_comment_list'] = Comment.objects.order_by(u"-create_time")[0:10]
            # 友情链接
            # context['links'] = Link.objects.order_by(u"create_time").all()
            '''
            colors = [u'primary', u'success', u'info', u'warning', u'danger']
            for index, link in enumerate(context['links']):
                link.color = colors[index % len(colors)]
            '''
            # 用户未读消息数
            user = self.request.user
            if user.is_authenticated():
                context['notification_count'] = \
                    user.to_user_notification_set.filter(is_read=0).count()

        except Exception as e1:
            LOG.error(u'[BaseMixin]加载基本信息出错! %s' % e1)
        return context


class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = u'article_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, *args, **kwargs):
        kwargs['carousel_page_list'] = Carousel.objects.all()
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0)
        return article_list


class UserView(BaseMixin, TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            LOG.error(u'[UserView]用户未登陆')
            return render(request, 'blog/login.html')

        slug = self.kwargs.get('slug')
        if slug == "changepassword":
            self.template_name = 'blog/user_change_password.html'
        elif slug == 'notification':
            self.template_name = 'blog/user_notification.html'

        return super(UserView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)

        slug = self.kwargs.get('slug')

        if slug == 'notification':
            """
            context['notifications'] = \
                self.request.user.to_user_notification_set.order_by(
                    '-create_time'
                ).all()
            """
        return context
