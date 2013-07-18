from django.conf.urls.defaults import patterns, include, url
#from models import FeedFetcher

urlpatterns = patterns('',
    url(r'^$', 'expwatch.views.home'),
    url(r'^list/$', 'expwatch.views.explist'),
#    url(r'^news/$', 'cmipstatus.views.newslist'),
#    url(r'^news/feed/$', FeedFetcher()),
    url(r'^expview/(\d+)/$', 'expwatch.views.expview'),
    url(r'^include/$', 'expwatch.views.includenew'),
#    url(r'^validation/(\w{3}\d{3})(_\d+)?/$', 'cmipstatus.views.expvalview'),
#    url(r'^outputs/$', 'cmipstatus.views.outputsview'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'gmaologin.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/exps/login/'}),
    )
