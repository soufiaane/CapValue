from django.conf.urls import patterns, url, include
from rest_framework import routers

from proxies.views import ProxyViewSet

router = routers.SimpleRouter()
router.register(r'', ProxyViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
