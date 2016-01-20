from django.conf.urls import patterns, url, include
from rest_framework import routers

from proxies.views import ProxyViewSet, IPViewSet

router = routers.SimpleRouter()
router.register(r'', ProxyViewSet)
router.register(r'/?<proxy_pk>/ip/$', IPViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
