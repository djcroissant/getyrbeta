from django.conf.urls import url

from . import views

app_name = 'account_info'
urlpatterns = [
    url(r'^profile/$',
        views.ProfileView.as_view(), name='account_profile'),
    ]
