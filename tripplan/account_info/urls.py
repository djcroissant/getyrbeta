from django.conf.urls import url

from . import views

app_name = 'account_info'
urlpatterns = [
    url(r'^profile/$',
        views.profile, name='account_profile'),
    ]
