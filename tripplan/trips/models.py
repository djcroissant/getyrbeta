from django.db import models
from django.utils import timezone

class TrailheadLocation(models.Model):
    """
    An abstract base class that provides trailhead coordinates
    """
    trailhead_latitude = models.CharField(max_length = 31, blank=True)
    trailhead_longitude = models.CharField(max_length = 31, blank=True)

    class Meta:
        abstract = True

class Trip(TrailheadLocation):
    title = models.CharField(max_length = 255)
    destination = models.CharField(max_length = 255, blank=True)
    start_date = models.DateField()
    number_nights = models.PositiveSmallIntegerField(default=0)
    trip_members = models.ManyToManyField('account_info.User',
        through='TripMember')

    def __str__(self):
        return self.title

    def is_in_the_past(self):
        return self.start_date < timezone.now().date()

    is_in_the_past.admin_order_field = 'start_date'
    is_in_the_past.boolean = True
    is_in_the_past.short_description = 'Past Trip?'

class SunTime(TrailheadLocation):
    dawn = models.TimeField()
    dusk = models.TimeField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    date = models.DateField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

class Item(models.Model):
    description = models.CharField(max_length = 255)
    quantity = models.PositiveSmallIntegerField(default=1)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    item_owners = models.ManyToManyField('account_info.User', through='ItemOwner')

class ItemOwner(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey('account_info.User', on_delete=models.CASCADE)
    accept_reqd = models.BooleanField(default=False)

class TripMember(models.Model):
    member = models.ForeignKey('account_info.User', on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    organizer = models.BooleanField(default=False)
    accept_reqd = models.BooleanField(default=False)
