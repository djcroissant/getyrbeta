from django.contrib import admin

from .models import User, EmergencyContact

admin.site.register(User)
admin.site.register(EmergencyContact)
