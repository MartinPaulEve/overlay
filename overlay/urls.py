from django.conf.urls import patterns, url, include
from django.contrib import admin
from journal.views import user_login, user_logout, OverlayManage, new_container, new_article, del_article, HomePageView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OLHSignUp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/', OverlayManage.as_view(), name="manage"),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^newissue/$', new_container, name='new_issue'),
    url(r'^newarticle/(?P<cont>\d{1,10})/$', new_article, name='new_article'),
    url(r'^delarticle/(?P<article>\d{1,10})/$', del_article, name='del_article'),
)