from django.conf.urls import include, url
from CapValue.views import IndexView

urlpatterns = [
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include('job.urls')),
    url(r'^api/v1/', include('seed.urls')),
    url(r'^api/v1/', include('emails.urls')),
    url(r'^api/v1/', include('team.urls')),
    url(r'^api/v1/', include('isp.urls')),
    url(r'^api/v1/proxies/', include('proxies.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^.*$', IndexView.as_view(), name='index')
]
