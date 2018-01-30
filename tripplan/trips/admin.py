from django.contrib import admin

from .models import Trip, Item, ItemOwner, \
    TripMember, TripGuest, TripLocation, ItemNotification

admin_models = (
    Trip,
    Item,
    ItemOwner,
    TripMember,
    TripGuest,
    TripLocation,
    ItemNotification
)

admin.site.register(admin_models)
