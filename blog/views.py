# !/usr/bin/python
# -*-coding:utf-8-*-

import json
import logging

from django import template
from django.conf import settings
from django.db.models import Q
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView

from .models import Article, Nav, Carousel, Category, Column

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


class AllView(BaseMixin, ListView):
    template_name = 'blog/all.html'
    context_object_name = 'article_list'

    def get_context_data(self, *args, **kwargs):
        kwargs['category_list'] = Category.objects.all()
        kwargs['PAGE_NUM'] = settings.PAGE_NUM
        return super(AllView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0).order_by("-pub_time")[0:settings.PAGE_NUM]
        return article_list

    def post(self, request, *args, **kwargs):
        val = self.request.POST.get("val", "")
        sort = self.request.POST.get("sort", "time")
        start = self.request.POST.get("start", 0)
        end = self.request.POST.get("end", settings.PAGE_NUM)

        start = int(start)
        end = int(end)

        if sort == 'time':
            sort = '-pub_time'
        elif sort == 'recommend':
            sort = '-view_times'
        else:
            sort = '-pub_time'

        if val == 'all':
            article_list = \
                Article.objects.filter(status=0).order_by(sort)[start:end + 1]
        else:
            try:
                article_list = Category.objects.get(
                    name=val
                ).article_set.filter(
                    status=0
                ).order_by(sort)[start:end + 1]
            except Category.DoesNotExist:
                LOG.error(u'[AllView]此分类不存在:[%s]' % val)
                raise PermissionDenied

        is_end = len(article_list) != (end-start+1)
        article_list = article_list[0:end - start]

        html = ""
        for article in article_list:
            html += template.loader.get_template(
                'blog/include/_all_posts.html'
            ).render(template.Context({'post': article}))

        my_dict = {"html": html, "isend": is_end}
        return HttpResponse(
            json.dumps(my_dict),
            content_type="application/json"
        )


class ColumnView(BaseMixin, ListView):
    queryset = Column.objects.all()
    template_name = 'blog/column.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, *args, **kwargs):
        column = self.kwargs.get('column', '')
        try:
            kwargs['column'] = Column.objects.get(name=column)
        except Column.DoesNotExist:
            LOG.error(u'[ColumnView]访问专栏不存在: [%s]' % column)
            raise Http404

        return super(ColumnView, self).get_context_data(**kwargs)

    def get_queryset(self):
        column = self.kwargs.get('column', '')
        try:
            article_list = Column.objects.get(name=column).article.all()
        except Column.DoesNotExist:
            LOG.error(u'[ColumnView]访问专栏不存在: [%s]' % column)
            raise Http404

        return article_list


class CategoryView(BaseMixin, ListView):
    template_name = "blog/category.html"
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        category = self.kwargs.get('category', '')
        try:
            article_list = Category.objects.get(name=category).article_set.all()
        except Category.DoesNotExist:
            LOG.error(u'[CategoryView]此分类不存在:[%s]' % category)
            raise Http404

        return article_list


class TagView(BaseMixin, ListView):
    template_name = 'blog/tag.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        article_list = Article.objects.only('tags').filter(tags__icontains=tag, status=0)
        return article_list


class SearchView(BaseMixin, ListView):
    template_name = 'blog/search.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, *args, **kwargs):
        kwargs['s'] = self.request.GET.get('s', '')
        return super(SearchView, self).get_context_data(**kwargs)

    def get_queryset(self):
        # 获取搜索的关键字
        s = self.request.GET.get('s', '')
        # 在文章的标题,summary和tags中搜索关键字
        article_list = Article.objects.only(
            'title', 'summary', 'tags'
        ).filter(
            Q(title__icontains=s) |
            Q(summary__icontains=s) |
            Q(tags__icontains=s),
            status=0
        )
        return article_list
