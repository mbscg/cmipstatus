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
    url(r'^cmip/outputs/$', 'cmipstatus.views.outputsview'),
    url(r'^cmip/login/$', 'django.contrib.auth.views.login', {'template_name' : 'cmiplogin.html'}),
    url(r'^cmip/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/cmip/login/'}),
    
    url(r'^gmao/$', 'groupsite.views.home'),
    url(r'^gmao/people/$', 'groupsite.views.people'),
    url(r'^gmao/people/(.*)/$', 'groupsite.views.people_view'),
    url(r'^gmao/newspaper/$', 'groupsite.views.newspaper'),
    url(r'^gmao/news/$', 'groupsite.views.news'),
    url(r'^gmao/news/(.*)/$', 'groupsite.views.news_view'),
    url(r'^gmao/science/$', 'groupsite.views.science'),
    url(r'^gmao/science/(.*)/$', 'groupsite.views.science_view'),
    url(r'^gmao/publications/$', 'groupsite.views.publications'),
    url(r'^gmao/blog/$', 'groupsite.views.blog'),
    url(r'^gmao/posts/$', 'groupsite.views.posts'),
    url(r'^gmao/posts/(.*)/$', 'groupsite.views.post_view'),
    url(r'^gmao/restricted/edit/$', 'groupsite.views.edit_profile'),
    url(r'^gmao/restricted/networking/$', 'groupsite.views.edit_network'),
    url(r'^gmao/restricted/configs/$', 'groupsite.views.edit_configs'),
    url(r'^gmao/restricted/create_news/$', 'groupsite.views.create_news'),
    url(r'^gmao/restricted/create_post/$', 'groupsite.views.create_post'),
    url(r'^gmao/restricted/create_video/$', 'groupsite.views.create_video'),
    url(r'^gmao/restricted/create_image/$', 'groupsite.views.create_image'),
    url(r'^gmao/restricted/editor/$', 'groupsite.views.editor_view'),
    url(r'^gmao/restricted/authorize_post/(.*)/$', 'groupsite.views.auth_post'),
    url(r'^gmao/restricted/deny_post/(.*)/$', 'groupsite.views.deny_post'),
    #url(r'^gmao/restricted/authorize_news/(.*)/$', 'groupsite.views.auth_news'),
    #url(r'^gmao/restricted/authorize_science/(.*)/$', 'groupsite.views.auth_science'),
    url(r'^gmao/restricted/upload_publication/$', 'groupsite.views.upload_publication'),
    url(r'^gmao/login/$', 'django.contrib.auth.views.login', {'template_name' : 'gmaologin.html'}),
    url(r'^gmao/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/gmao/login/'}),

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

