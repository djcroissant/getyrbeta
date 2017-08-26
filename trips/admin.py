from django.contrib import admin

from .models import User, Vehicle

admin.site.register([User, Vehicle])
