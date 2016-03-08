from django.conf.urls import include, url
from rest_framework_nested import routers

from CapValue.views import IndexView
from authentication.views import LoginView, LogoutView, AccountViewSet
from isp.views import IspViewSet, AccountIspViewSet
from seed.views import SeedViewSet, AccountSeedViewSet

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'isps', IspViewSet)
router.register(r'seeds', SeedViewSet)

account_isp = routers.NestedSimpleRouter(router, r'accounts', lookup='account')
account_isp.register(r'isp', AccountIspViewSet)

account_seed = routers.NestedSimpleRouter(router, r'accounts', lookup='account')
account_seed.register(r'seed', AccountSeedViewSet)

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls))
    url(r'^api/v1/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(account_isp.urls)),
    url(r'^api/v1/', include(account_seed.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url('^.*$', IndexView.as_view(), name='index')
]
