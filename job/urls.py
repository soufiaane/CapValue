from django.conf.urls import patterns, url, include
from rest_framework import routers
from job.views import JobViewSet

router = routers.SimpleRouter()
router.register(r'', JobViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
