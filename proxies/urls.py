from django.conf.urls import url, include
from rest_framework import routers

from proxies.views import ProxyViewSet, IPViewSet

router = routers.SimpleRouter()
router.register(r'', ProxyViewSet)
router.register(r'^P<proxy_pk>/ip', IPViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
