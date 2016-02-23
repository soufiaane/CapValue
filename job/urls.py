from job.views import JobView, AccountJobList
from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'^jobs/(?P<username>.+)', AccountJobList)

urlpatterns = [
    url(r'^jobs/$', JobView.as_view(), name='job'),
    url(r'^', include(router.urls))
]
