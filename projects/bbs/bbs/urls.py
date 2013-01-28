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
    url(r'^$', 'app.views.index'),
    url(r'^node/(?P<node_id>\d+)/$', 'app.views.node'),
    url(r'^/topic/(?P<topic_id>\d+)/$', 'app.views.topic'),
    url(r'create/$', 'app.views.create_topic'),
    url(r'reply/(?P<topic_id>\d+)/$', 'app.views.reply'),
    url(r'accounts/$', 'app.views.account'),
    url(r'accounts/signup/$', 'app.views.signup'),
    url(r'accounts/login/$', 'app.views.log_in'),
    url(r'^accounts/logout/$', 'app.views.log_out'),
)
