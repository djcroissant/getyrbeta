from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'trips'

urlpatterns = [
    url(r'^$', views.TripList.as_view(), name='trip_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.TripView.as_view(), name='trip_detail'),
    url(r'^create/$',
        views.TripCreateView.as_view(), name='trip_create'),
    url(r'^(?P<trip_id>[0-9]+)/create/(?P<location_type>[\w]+)/$',
        views.LocationCreateView.as_view(), name='location_create'),
    url(r'^(?P<trip_id>[0-9]+)/edit/(?P<location_type>[\w]+)/(?P<pk>[0-9]+)/$',
        views.LocationEditView.as_view(), name='location_edit'),
    url(r'^(?P<trip_id>[0-9]+)/delete/(?P<location_type>[\w]+)/(?P<pk>[0-9]+)/$',
        views.LocationDeleteView.as_view(), name='location_delete'),
    url(r'^notifications/$', views.notifications, name='notifications'),
]
