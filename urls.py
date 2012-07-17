from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from cmipstatus.models import FeedFetcher

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^cmip/$', 'cmipstatus.views.home'),
    url(r'^cmip/list/$', 'cmipstatus.views.explist'),
    url(r'^cmip/news/$', 'cmipstatus.views.newsview'),
    url(r'^cmip/news/feed/$', FeedFetcher()),
    url(r'^cmip/expview/(.*)/$', 'cmipstatus.views.expview'),
    url(r'^cmip/validation/(.*)/$', 'cmipstatus.views.expvalview'),
    url(r'^cmip/people_list/$', 'cmipstatus.views.peoplelist'),
    url(r'^cmip/profview/(.*)/$', 'cmipstatus.views.profview'),
    url(r'^cmip/profedit/$', 'cmipstatus.views.profedit'),
    url(r'^cmip/changepass/$', 'cmipstatus.views.passwedit'),
    url(r'^cmip/login/$', 'django.contrib.auth.views.login', {'template_name' : 'cmiplogin.html'}),
    url(r'^cmip/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/cmip/login/'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

