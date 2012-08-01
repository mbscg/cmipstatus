from django.conf.urls.defaults import patterns, include, url
from models import FeedFetcher

urlpatterns = patterns('',
    url(r'^$', 'cmipstatus.views.home'),
    url(r'^list/$', 'cmipstatus.views.explist'),
    url(r'^news/$', 'cmipstatus.views.newsview'),
    url(r'^news/feed/$', FeedFetcher()),
    url(r'^expview/(\w{3}\d{3})/$', 'cmipstatus.views.expview'),
    url(r'^validation/(\w{3}\d{3})(_\d+)?/$', 'cmipstatus.views.expvalview'),
    url(r'^outputs/$', 'cmipstatus.views.outputsview'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'gmaologin.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/cmip/login/'}),
    )
