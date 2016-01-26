from emails.views import EmailView, AccountEmailList
from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'^emails/(?P<username>.+)', AccountEmailList)

urlpatterns = [
    url(r'^emails/$', EmailView.as_view(), name='emails'),
    url(r'^', include(router.urls))
]