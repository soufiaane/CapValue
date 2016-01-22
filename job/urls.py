from django.conf.urls import url, include
from rest_framework import routers

from job.views import JobViewSet

router = routers.SimpleRouter()
router.register(r'^', JobViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
