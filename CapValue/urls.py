from django.conf.urls import include, url
from rest_framework_nested import routers
from CapValue.views import IndexView
from authentication.views import LoginView, LogoutView, AccountViewSet, AccountProfileViewSet
from job.views import JobViewSet, AccountJobViewSet, RevokeJob, UpdateJobResults
from seed.views import SeedViewSet, AccountSeedViewSet
from team.views import TeamViewSet, AccountTeamViewSet, EntityTeamViewSet
from entity.views import EntityViewSet

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'seeds', SeedViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'entity', EntityViewSet)

account_team = routers.NestedSimpleRouter(router, r'accounts', lookup='account')
account_team.register(r'team', AccountTeamViewSet)

account_seed = routers.NestedSimpleRouter(router, r'accounts', lookup='account')
account_seed.register(r'seed', AccountSeedViewSet)

account_job = routers.NestedSimpleRouter(router, r'accounts', lookup='account')
account_job.register(r'job', AccountJobViewSet)

entity_team = routers.NestedSimpleRouter(router, r'entity', lookup='entity')
entity_team.register(r'teams', EntityTeamViewSet)


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls))
    url(r'^api/v1/jobs/revoke/$', RevokeJob.as_view(), name='revoke'),
    url(r'^api/v1/jobs/update_results/$', UpdateJobResults.as_view(), name='update_results'),
    url(r'^api/v1/accounts/profiles/$', AccountProfileViewSet.as_view(), name='account_profiles'),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(account_team.urls)),
    url(r'^api/v1/', include(account_seed.urls)),
    url(r'^api/v1/', include(account_job.urls)),
    url(r'^api/v1/', include(entity_team.urls)),
    url('^.*$', IndexView.as_view(), name='index')
]
