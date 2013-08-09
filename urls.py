from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from expwatch.urls import urlpatterns as exps_patterns
from groupsite.urls import urlpatterns as gmao_patterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^exps/', include(exps_patterns)),
    url(r'', include(gmao_patterns)),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

