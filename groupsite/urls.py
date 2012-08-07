from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'groupsite.views.home'),
    url(r'^people/$', 'groupsite.views.people'),
    url(r'^people/(\d+)/$', 'groupsite.views.peopleview'),
    url(r'^newspaper/$', 'groupsite.views.newspaper'),
    url(r'^news/$', 'groupsite.views.news'),
    url(r'^news/(\d+)/$', 'groupsite.views.newsview'),
    url(r'^science/$', 'groupsite.views.science'),
    url(r'^science/(\d+)/$', 'groupsite.views.scienceview'),
    url(r'^publications/$', 'groupsite.views.publications'),
    url(r'^blog/$', 'groupsite.views.blog'),
    url(r'^posts/$', 'groupsite.views.posts'),
    url(r'^posts/(\d+)/$', 'groupsite.views.postview'),
    url(r'^restricted/edit/$', 'groupsite.views.editprofile'),
    url(r'^restricted/networking/$', 'groupsite.views.editnetwork'),
    url(r'^restricted/configs/$', 'groupsite.views.editconfigs'),
    url(r'^restricted/create_news/$', 'groupsite.views.createnews'),
    url(r'^restricted/create_post/$', 'groupsite.views.createpost'),
    url(r'^restricted/create_video/$', 'groupsite.views.createvideo'),
    url(r'^restricted/create_image/$', 'groupsite.views.createimage'),
    url(r'^restricted/create_attachment/$', 'groupsite.views.createattachment'),
    url(r'^restricted/editor/$', 'groupsite.views.editorview'),
    url(r'^restricted/authorize_post/(\d+)/$', 'groupsite.views.authpost'),
    url(r'^restricted/deny_post/(\d+)/$', 'groupsite.views.denypost'),
    url(r'^restricted/authorize_news/(.*)/$', 'groupsite.views.authnews'),
    url(r'^restricted/deny_news/(\d+)/$', 'groupsite.views.denynews'),
    url(r'^restricted/authorize_science/(\d+)/$', 'groupsite.views.authscience'),
    url(r'^restricted/deny_science/(\d+)/$', 'groupsite.views.denyscience'),
    url(r'^restricted/upload_publication/$', 'groupsite.views.uploadpublication'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'gmaologin.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/gmao/login/'}),    
    url(r'^--moo/$', 'groupsite.views.moo'),    
    url(r'^pres/$', 'groupsite.views.presentation'),
    )
