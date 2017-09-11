from django.conf.urls import url

from . import views

app_name = 'account_info'
urlpatterns = [
    url(r'^profile/(?P<pk>[0-9]+)/$',
        views.ProfileView.as_view(), name='account_profile'),
    ]
