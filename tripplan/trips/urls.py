from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'trips'

urlpatterns = [
    url(r'^$', views.TripList.as_view(), name='trip_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.TripView.as_view(), name='trip_detail'),
    # url(r'^edit/(?P<pk>[0-9]+)/$', views.TripEditView.as_view(), name='trip_edit'),
    url(r'^create/$',
        views.TripCreateView.as_view(), name='trip_create'),
    url(r'^create/(?P<trip_id>[0-9]+)/trailhead/$',
        views.TrailheadCreateView.as_view(), name='trailhead_create'),
    url(r'^create/(?P<trip_id>[0-9]+)/objective/$',
        views.ObjectiveCreateView.as_view(), name='objective_create'),
    url(r'^create/(?P<trip_id>[0-9]+)/camp/$',
        views.CampCreateView.as_view(), name='camp_create'),
    url(r'^edit/(?P<trip_id>[0-9]+)/objective/(?P<pk>[0-9]+)/$',
        views.ObjectiveEditView.as_view(), name='objective_edit'),
    url(r'^edit/(?P<trip_id>[0-9]+)/camp/(?P<pk>[0-9]+)/$',
        views.CampEditView.as_view(), name='camp_edit'),
    url(r'^delete/(?P<trip_id>[0-9]+)/objective/(?P<pk>[0-9]+)/$',
        views.ObjectiveDeleteView.as_view(), name='objective_delete'),
    # url(r'^delete/(?P<trip_id>[0-9]+)/location/(?P<location_id>[0-9]+)/$',
    #     views.LocationDeleteView.as_view(), name='location_delete'),
    url(r'^notifications/$', views.notifications, name='notifications'),
]


    # url(r'^create/(?P<trip_id>[0-9]+)/(?P<location_type>[\w])/$',
    #     views.TrailheadCreateView.as_view(), name='trailhead_create'),

            # <a href="{% url 'trips:trailhead_create' trip_id=trip.id location_type='trailhead' %}">Add new location</a>
