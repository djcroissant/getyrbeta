from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from tripplan.site_info import views as site_views


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='authentication:login', permanent=False)),
    url(r'^account_info/', include('account_info.urls')),
    url(r'^trips/', include('trips.urls')),
    url(r'^about/', site_views.AboutView.as_view(), name='about'),

    # User management. Allauth urls overwritten in authentication app
    # will be matched first.
    url(r'^accounts/', include('authentication.urls')),
    url(r'^accounts/', include('allauth.urls')),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
]
if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
