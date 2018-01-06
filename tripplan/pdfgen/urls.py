from django.conf.urls import url

from . import views

app_name = 'pdfgen'

urlpatterns = [
    url(r'^(?P<trip_id>[0-9]+)/trip_plan/$',
        views.TripPlanView.as_view(), name='trip_plan'),
]
