from django.conf.urls import url

from . import views

app_name = 'pdfgen'

urlpatterns = [
    url(r'^test/$', views.hello_world, name='test'),
]
