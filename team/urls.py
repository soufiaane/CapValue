from team.views import TeamView
from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter()
# router.register(r'^seeds/(?P<username>.+)', AccountSeedList)

urlpatterns = [
    url(r'^teams/$', TeamView.as_view(), name='team'),
    # url(r'^', include(router.urls))
]