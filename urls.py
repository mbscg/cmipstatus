from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from cmipstatus.models import FeedFetcher
from expwatch.urls import urlpatterns as exps_patterns
from groupsite.urls import urlpatterns as gmao_patterns

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^exps/', include(exps_patterns)),
    url(r'', include(gmao_patterns)),

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

