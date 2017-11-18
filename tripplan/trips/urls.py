from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'trips'

urlpatterns = [
    url(r'^$', views.TripListView.as_view(), name='trip_list'),
    url(r'^(?P<pk>[0-9]+)/$',
        views.TripDetailView.as_view(), name='trip_detail'),
    url(r'^create/$', views.TripCreateView.as_view(), name='trip_create'),
    url(r'^(?P<trip_id>[0-9]+)/create/(?P<location_type>[\w]+)/$',
        views.LocationCreateView.as_view(), name='location_create'),
    url(r'^(?P<trip_id>[0-9]+)/edit/(?P<location_type>[\w]+)/(?P<pk>[0-9]+)/$',
        views.LocationEditView.as_view(), name='location_edit'),
    url(r'^(?P<trip_id>[0-9]+)/delete/(?P<location_type>[\w]+)/(?P<pk>[0-9]+)/$',
        views.LocationDeleteView.as_view(), name='location_delete'),
    url(r'^notifications/$',
        views.NotificationListView.as_view(), name='notifications'),
    url(r'^(?P<pk>[0-9]+)/members/$',
        views.TripMemberListView.as_view(), name='trip_members'),
    url(r'^ajax/user_exists/$',
        views.CheckUserExistsView.as_view(), name='user_exists'),
    url(r'^ajax/add_trip_member/$',
        views.AddTripMemberView.as_view(), name='add_trip_member'),
    url(r'^ajax/add_trip_guest/$',
        views.AddTripGuestView.as_view(), name='add_trip_guest'),
    url(r'^ajax/update_trip_member/$',
        views.UpdateTripMemberView.as_view(), name='update_trip_member'),
    url(r'^ajax/delete_trip_member/$',
        views.DeleteTripMemberView.as_view(), name='delete_trip_member'),
]
