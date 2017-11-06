from django.conf.urls import url

from . import views

app_name = 'authentication'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^social/signup/$',
        views.SocialSignupView.as_view(), name='socialaccount_signup'),
    url(r'^social/connections/$',
        views.SocialConnectionsView.as_view(),
        name='socialaccount_connections'),
]
