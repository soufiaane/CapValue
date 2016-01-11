from django.conf.urls import patterns, url, include
from rest_framework_nested import routers
from seed.views import SeedViewSet

router = routers.SimpleRouter()
router.register(r'seeds', SeedViewSet)

urlpatterns = patterns('',
                       url(r'^$', include(router.urls)),
                       )
