from django.conf.urls import url

from . import views

app_name = 'account_info'
urlpatterns = [
    url(r'^profile/$',
        views.ProfileView.as_view(), name='account_profile'),
    url(r'^emergency_contacts/$',
        views.EmergencyContactListView.as_view(), name='emerg_contact_list'),
    url(r'^emergency_contacts/create/$',
        views.EmergencyContactCreateView.as_view(), name='emerg_contact_create'),
    url(r'^emergency_contacts/(?P<pk>[0-9]+)/edit/$',
        views.EmergencyContactEditView.as_view(), name='emerg_contact_edit'),
    url(r'^emergency_contacts/(?P<pk>[0-9]+)/delete/$',
        views.EmergencyContactDeleteView.as_view(), name='emerg_contact_delete'),
    url(r'^vehicles/$',
        views.VehicleListView.as_view(), name='vehicle_list'),
    url(r'^vehicles/create/$',
        views.VehicleCreateView.as_view(), name='vehicle_create'),
    url(r'^vehicles/(?P<pk>[0-9]+)/edit/$',
        views.VehicleEditView.as_view(), name='vehicle_edit'),
    url(r'^vehicles/(?P<pk>[0-9]+)/delete/$',
        views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    ]
