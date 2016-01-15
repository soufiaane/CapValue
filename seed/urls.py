from django.conf.urls import patterns, url, include
from rest_framework import routers
from seed.views import SeedViewSet

router = routers.SimpleRouter()
router.register(r'', SeedViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
