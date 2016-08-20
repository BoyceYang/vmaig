# !/usr/bin/python
# -*-coding:utf-8-*-

from blog.models import News

from django.conf.urls import url
from django.views.generic import DetailView, TemplateView

from .views import IndexView, ArticleView, AllView, ColumnView, CategoryView, TagView, SearchView, NewsView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^article/(?P<slug>\w+).html$', ArticleView.as_view(), name='article-detail-view'),

    url(r'^all/$', AllView.as_view(), name='all-view'),
    url(r'^column/(?P<column>\w+)/$', ColumnView.as_view(), name='column-detail-view'),
    url(r'^category/(?P<category>\w+)/$', CategoryView.as_view(), name='category-detail-view'),
    url(r'^tag/(?P<tag>\w+)/$', TagView.as_view(), name='tag-detail-view'),
    url(r'^search/$', SearchView.as_view()),
    url(r'^news/$', NewsView.as_view(), name='news-view'),
    url(r'^news/(?P<pk>\w+)$',
        DetailView.as_view(model=News), name='news-detail-view'),

    url(r'^forgetpassword/$', TemplateView.as_view(template_name="blog/forget_password.html")),
    url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        TemplateView.as_view(template_name="blog/reset_password.html"), name='resetpassword-view'),
]
