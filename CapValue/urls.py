from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework_nested import routers
from authentication.views import AccountViewSet, LoginView, LogoutView
from CapValue.views import IndexView

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
                       url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
                       url(r'^api/v1/', include(router.urls)),
                       url('^.*$', IndexView.as_view(), name='index'),
                       )
