from proxies.views import ProxyView, IPViewSet
from django.conf.urls import url, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'^<proxy_pk>/ip', IPViewSet)

urlpatterns = [
    url(r'^proxy/$', ProxyView.as_view(), name='proxy'),
    url(r'^', include(router.urls))
]
