"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='#=j8t0s6t#bzh(2cn84!*w7&056%7k8wcisi0x96urmj&=#_rv')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

DEBUG_TOOLBAR_CONFIG = {
    'SKIP_TEMPLATE_PREFIXES': (
        'django/forms/widgets/',
        'admin/widgets/',
        'floppyforms/'
    ),
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
        # 'debug_toolbar.panels.redirects.TemplatesPanel'  <<<< Consider disabling templates  if page load is sloooow.
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}


# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
# Google Maps API key can be acquired here:
# https://developers.google.com/maps/documentation/javascript/get-api-key
GOOGLE_MAPS_API = env('GOOGLE_MAPS_API', default='AIzaSyDWhowSelvksmtGM7SOllzIuuzaNq-rI7E')
