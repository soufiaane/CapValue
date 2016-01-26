from isp.views import ISPView
from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter()
# router.register(r'^seeds/(?P<username>.+)', AccountSeedList)

urlpatterns = [
    url(r'^isps/$', ISPView.as_view(), name='isp'),
    # url(r'^', include(router.urls))
]