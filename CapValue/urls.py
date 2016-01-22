from django.conf.urls import include, url

from CapValue.views import IndexView

urlpatterns = [
    url(r'^api/v1/auth', include('authentication.urls')),
    url(r'^api/v1/jobs', include('job.urls')),
    url(r'^api/v1/seeds', include('seed.urls')),
    url(r'^api/v1/proxies', include('proxies.urls')),
    url(r'^api/v1/accounts', include('authentication.accounts_urls')),
    url('^.*$', IndexView.as_view(), name='index')
]
