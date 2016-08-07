# !/usr/bin/python
# -*-coding:utf-8-*-

import logging

from django.conf import settings
from django.db.models import Q
from django.core.cache import caches
from django.http import Http404
from django.views.generic import ListView, DetailView

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


class ArticleView(BaseMixin, DetailView):

    queryset = Article.objects.filter(Q(status=0) | Q(status=1))
    template_name = 'blog/article.html'
    context_object_name = 'article'
    slug_field = 'en_title'

    def get(self, request, *args, **kwargs):
        # 统计文章的访问访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        en_title = self.kwargs.get('slug')
        # 获取15*60s时间内访问过这篇文章的所有ip
        visited_ips = cache.get(en_title, [])

        # 如果ip不存在就把文章的浏览次数+1
        if ip not in visited_ips:
            try:
                article = self.queryset.get(en_title=en_title)
            except Article.DoesNotExist:
                LOG.error(u'[ArticleView]访问不存在的文章:[%s]' % en_title)
                raise Http404
            else:
                article.view_times += 1
                article.save()
                visited_ips.append(ip)

            # 更新缓存
            cache.set(en_title, visited_ips, 15 * 60)

        return super(ArticleView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(ArticleView, self).get_context_data(**kwargs)
