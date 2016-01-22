from django.conf.urls import include, url
from rest_framework_nested import routers

from authentication.views import AccountViewSet
from job.views import AccountJobViewSet

router = routers.SimpleRouter()
router.register(r'^', AccountViewSet)

accounts_router = routers.NestedSimpleRouter(
    router, r'^', lookup='account'
)

accounts_router.register(r'jobs', AccountJobViewSet)
# accounts_router.register(r'seeds', AccountSeedViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(accounts_router.urls))
]
