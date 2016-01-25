from authentication.views import LoginView, LogoutView
from django.conf.urls import url


urlpatterns = [
    url(r'^auth/login/$', LoginView.as_view(), name='login'),
    url(r'^auth/logout/$', LogoutView.as_view(), name='logout'),
]
