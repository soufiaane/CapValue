from django.conf.urls import url, include
from rest_framework import routers

from seed.views import SeedViewSet, AccountSeedList

router = routers.SimpleRouter()
router.register(r'(?P<username>.+)', AccountSeedList)
router.register(r'', SeedViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
