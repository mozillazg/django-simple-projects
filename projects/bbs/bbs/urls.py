#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bbs.views.home', name='home'),
    # url(r'^bbs/', include('bbs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # url(r'^$', 'bb.views.index'),
    url(r'^$', 'bb.views.page', ),
    url(r'^page/(?P<page_id>\d+)/$', 'bb.views.page'),
    url(r'^popular/$', 'bb.views.page', {'popular': True}),
    url(r'^popular/page/(?P<page_id>\d+)$', 'bb.views.page', {'popular': True}),
    url(r'^nodes/$', 'bb.views.nodes'),
    url(r'^node/(?P<node_id>\d+)/$', 'bb.views.page'),
    url(r'^node/(?P<node_id>\d+)/page/(?P<page_id>\d+)/$', 'bb.views.page'),
    url(r'^topic/(?P<topic_id>\d+)$', 'bb.views.topic', name="topic_view"),
    url(r'^topic/(?P<topic_id>\d+)/page/(?P<page_id>\d+)$', 'bb.views.topic'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    # url(r'^reply/(\d+)$', 'bb.views.reply'),
    # url(r'^signup$', 'bb.views.signup'),
    url(r'^account/signin$', 'bb.views.signin'),
    url(r'^account/signup$', 'bb.views.signup'),
    url(r'^account$', 'bb.views.change_password'),
    url(r'^account/logout$', 'bb.views.log_out'),
    url(r'^create$', 'bb.views.create'),
)
