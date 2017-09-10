from django.conf.urls import url

from . import views

app_name = 'authentication'

urlpatterns = [
    url(r'^signin/$', views.SignInView.as_view(), name='signin'),
    url(r'^signout/$', views.SignOutView.as_view(), name='signout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
]
