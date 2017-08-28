from django.conf.urls import url

from . import views

app_name = 'trips'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.user_profile, name='user_profile'),
    url(r'^vehicle/(?P<vehicle_id>[0-9]+)/$', views.vehicle_detail, name='vehicle_detail'),
]
