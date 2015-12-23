from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework_nested import routers
from authentication.views import AccountViewSet
from CapValue.views import IndexView

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/v1/', include(router.urls)),

                       url('^.*$', IndexView.as_view(), name='index'),
                       )
