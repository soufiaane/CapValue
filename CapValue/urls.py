from django.conf.urls import include, url
from rest_framework_nested import routers

from CapValue.views import IndexView
from authentication.views import LoginView, LogoutView, AccountViewSet
from isp.views import IspViewSet, AccountIspViewSet

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'isps', IspViewSet)

account_isp = routers.NestedSimpleRouter(router, r'accounts', lookup='account')
account_isp.register(r'isp', AccountIspViewSet)

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls))
    url(r'^api/v1/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(account_isp.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url('^.*$', IndexView.as_view(), name='index')
]
