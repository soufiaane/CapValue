from seed.views import SeedView, AccountSeedList
from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'^seeds/(?P<username>.+)', AccountSeedList)

urlpatterns = [
    url(r'^seeds/$', SeedView.as_view(), name='seed'),
    url(r'^', include(router.urls))
]