from team.views import TeamView, ISPTeamList
from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'^teams/isp/(?P<isp_id>.+)', ISPTeamList)

urlpatterns = [
    url(r'^teams/$', TeamView.as_view(), name='team'),
    url(r'^', include(router.urls))
]