from django.contrib import admin

from .models import Trip, SunTime, Item, ItemOwner, \
    TripMember, TripGuest, TripLocation, ItemNotification

admin_models = (
    Trip,
    SunTime,
    Item,
    ItemOwner,
    TripMember,
    TripGuest,
    TripLocation,
    ItemNotification
)

admin.site.register(admin_models)
