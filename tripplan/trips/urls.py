from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'trips'

urlpatterns = [
    url(r'^$', views.TripList.as_view(), name='trip_list'),
    url(r'^trip/(?P<pk>[0-9]+)/$', views.TripView.as_view(), name='trip_detail'),
    url(r'^trip/addtrip/$',
        views.TripCreateView.as_view(), name='trip_create'),
    url(r'^profile/(?P<pk>[0-9]+)/$',
        views.VehicleView.as_view(), name='vehicle_detail'),
    url(r'^trip/(?P<pk>[0-9]+)/$',
        views.TripView.as_view(), name='trip_detail'),
    url(r'^profile/(?P<user_id>[0-9]+)/addvehicle/$',
        views.VehicleCreateView.as_view(), name='vehicle_create'),
    url(r'^notifications/$', views.notifications, name='notifications'),
]
