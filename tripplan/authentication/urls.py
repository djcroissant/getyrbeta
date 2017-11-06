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
    url(r'^password/reset/$',
        views.PasswordResetView.as_view(), name='account_reset_password'),
    url(r'^password/reset/done/$',
        views.PasswordResetDoneView.as_view(),
        name='account_reset_password_done'),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.PasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$",
        views.PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done"),
]
