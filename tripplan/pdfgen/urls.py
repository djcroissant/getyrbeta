from django.conf.urls import url

from . import views

app_name = 'pdfgen'

urlpatterns = [
    url(r'^test/$', views.hello_world, name='test'),
    url(r'^trip_plan/$', views.TripPlanView.as_view(), name='trip_plan'),
]
