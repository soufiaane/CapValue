from isp.views import ISPView, TeamISPList
from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'^isps/team/(?P<team_id>.+)', TeamISPList)

urlpatterns = [
    url(r'^isps/$', ISPView.as_view(), name='isp'),
    url(r'^', include(router.urls))
]