from django.contrib import admin

from .models import Trip

# class VehicleInline(admin.TabularInline):
#     model = Vehicle
#     extra = 0

class TripAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['start_date']}),
        ('Location information', {'fields': ['trailhead_latitude',
            'trailhead_longitude'], 'classes': ['collapse']}),
    ]
    list_display = ('title', 'start_date', 'is_in_the_past')
    list_filter = ['start_date']
    search_fields = ['title']

# class UserAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['first_name', 'last_name', 'nickname']}),
#     ]
#     inlines = [VehicleInline]

admin.site.register(Trip, TripAdmin)
# admin.site.register(User, UserAdmin)
