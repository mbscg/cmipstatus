from django.conf.urls.defaults import patterns, include, url
from views import Home, ExpList, ExpView, IncludeNewExp, ExcludeExp
from views import MemberView
from views import AlertView, AlertDismiss, Filecheck, FilecheckImgs
#from models import FeedFetcher

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name="home"),
    url(r'^list/$', ExpList.as_view(), name="exp_list"),
    url(r'^expview/(?P<expid>\d+)/$', ExpView.as_view(), name="exp_view"),
    url(r'^member/(?P<memberid>\d+)/$', MemberView.as_view(), name="member_view"),
    url(r'^include/$', IncludeNewExp.as_view(), name="include_exp"),
    url(r'^exclude/$', ExcludeExp.as_view(), name="exclude_exp"),
    url(r'^alert/view/(?P<alertid>\d+)/$', AlertView.as_view(), name="alert_view"),
    url(r'^alert/dismiss/(?P<alertid>\d+)/$', AlertDismiss.as_view(), name="alert_dismiss"),
    url(r'^filecheck/$', Filecheck.as_view(), name="filecheck_view"),
    url(r'^filecheck/(?P<decadal>\d+)/$', FilecheckImgs.as_view(), name="filecheck_view"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'gmaologin.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/exps/login/'}, name="logout"),
    )
