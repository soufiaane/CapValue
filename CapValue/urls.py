from django.conf.urls import include, url

from CapValue.views import IndexView

urlpatterns = [
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include('job.urls')),
    url(r'^api/v1/', include('seed.urls')),
    url(r'^api/v1/', include('mail.urls')),
    url(r'^api/v1/', include('team.urls')),
    url(r'^api/v1/', include('isp.urls')),
    url(r'^api/v1/', include('proxy.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^.*$', IndexView.as_view(), name='index')
]
