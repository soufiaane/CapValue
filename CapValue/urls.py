from django.conf.urls import patterns, include, url
from CapValue.views import IndexView

urlpatterns = patterns('',
                       url(r'^api/v1/auth/', include('authentication.urls')),
                       url(r'^api/v1/jobs/', include('job.urls')),
                       url(r'^api/v1/seeds/', include('seed.urls')),
                       url(r'^api/v1/accounts/', include('authentication.accounts_urls')),
                       url('^.*$', IndexView.as_view(), name='index'),
                       )
