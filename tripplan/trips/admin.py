from django.contrib import admin

from .models import Trip

# class VehicleInline(admin.TabularInline):
#     model = Vehicle
#     extra = 0

class TripAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['start_date']}),
        ('Number of nights', {'fields': ['number_nights']}),
    ]
    list_display = ('title', 'start_date', 'is_in_the_past')
    list_filter = ['start_date']
    search_fields = ['title']

admin.site.register(Trip, TripAdmin)
