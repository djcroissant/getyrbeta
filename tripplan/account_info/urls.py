from django.conf.urls import url

from . import views

app_name = 'trips'
urlpatterns = [
    url(r'^profile/$',
        views.profile, name='account_profile'),
    ]
