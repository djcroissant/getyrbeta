from django.db import models
from django.utils import timezone


class Trip(models.Model):
    title = models.CharField(max_length = 255)
    destination = models.CharField(max_length = 255, blank=True)
    start_date = models.DateField()
    number_nights = models.PositiveSmallIntegerField(default=0)
    trip_members = models.ManyToManyField('account_info.User',
        through='TripMember')

    def __str__(self):
        return self.title

    def get_trailhead(self):
        try:
            th = self.triplocation_set.filter(
                location_type=TripLocation.BEGIN)[0]
        except IndexError:
            th = None
        return th

    def get_endpoint(self):
        try:
            ep = self.triplocation_set.filter(
                location_type=TripLocation.END)[0]
        except IndexError:
            ep = None
        return ep
    
    def is_in_the_past(self):
        return self.start_date < timezone.now().date()

    is_in_the_past.admin_order_field = 'start_date'
    is_in_the_past.boolean = True
    is_in_the_past.short_description = 'Past Trip?'

class SunTime(models.Model):
    dawn = models.TimeField()
    dusk = models.TimeField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    date = models.DateField()
    latitude = models.CharField(max_length = 31, blank=True)
    longitude = models.CharField(max_length = 31, blank=True)
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

class TripLocation(models.Model):
    BEGIN = 'ST'
    END = 'EN'
    OBJECTIVE = 'OB'
    CAMP = 'CM'

    LOCATION_TYPE_CHOICES = (
        (BEGIN, 'Start Location'),
        (END, 'End Location'),
        (OBJECTIVE, 'Objective Location'),
        (CAMP, 'Camp Location'),
    )

    # LABEL_CHOICES = {
    #     BEGIN: 'Trailhead description',
    #     END: 'End point description',
    #     OBJECTIVE: 'Description',
    #     CAMP: 'Description'
    # }

    location_type = models.CharField(max_length=2,
        choices=LOCATION_TYPE_CHOICES)
    title = models.CharField(max_length = 255, blank=True)
    date = models.DateField(blank=True)
    latitude = models.CharField(max_length = 31, blank=True)
    longitude = models.CharField(max_length = 31, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
