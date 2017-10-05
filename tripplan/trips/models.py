import datetime

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
        """
        This function will return the TripLocation object corresponding
        to the trailhead, if it exists. Otherwise, returns None
        """
        try:
            th = self.triplocation_set.filter(
                location_type=TripLocation.BEGIN)[0]
        except IndexError:
            th = None
        return th

    def get_endpoint(self):
        """
        This function will return the TripLocation object corresponding
        to the endpoint, if it exists. Otherwise, returns None
        """
        try:
            ep = self.triplocation_set.filter(
                location_type=TripLocation.END)[0]
        except IndexError:
            ep = None
        return ep

    def get_datehash(self):
        """
        This funtion will return a dictionary that relates the specific
        dates of a multi-night trip to the day number
        (e.g. {10/01/2017: 'Day 1'})
        """
        objectives = self.triplocation_set.all()
        datehash = {None: 'Unassigned'}
        for i in range(0, self.number_nights):
            key = self.start_date + datetime.timedelta(days=i)
            value = "Day " + str(i + 1)
            datehash[key] = value
        return datehash

    def get_location_context(self, location_type):
        """
        This funtion will return a dictionary with keys 'datelist',
        'locationlist', and 'locationrange'.

        The value corresponding to 'datelist' is a list of
        days for which objectives have been defined, in day number format
        (e.g. 'datelist': ['Unassigned', 'Day 2', 'Day 5']). 'Unassigned' is
        included when there are objectives that don't have a date.

        The value corresponding to 'locationlist' is a list of lists.
        Each sublist is a list of TripLocation objects corresponding to
        locations for the date in the corresponding element of datelist

        The value corresponding to 'locationrange' is a range from 0 to the
        number of elements in datelist. this also corresponds to the number of
        1st level lists in locationlist. It must be passed via context to
        the template because the template does not support the 'range' tag.

        Special circumstances are defined when the Trip has no locations for
        the relevant location_type or when the trip has number_nights == 0
        """
        locations = self.triplocation_set.filter(
            location_type=location_type)
        if locations.count() == 0:
            datelist = loclist = locrange = None
        elif self.number_nights == 0 and location_type == TripLocation.OBJECTIVE:
            datelist = ['Day 1']
            loclist = [list(locations)]
            locrange = range(len(datelist))
        else:
            datelist = []
            loclist = []
            datehash = self.get_datehash()
            # Address the special case for locations with no date assigned
            # this will be listed as 'unassigned'
            date = None
            filtered_locations = locations.filter(date=date)
            if filtered_locations.count() > 0:
                datelist.append(datehash[date])
                loclist.append(list(filtered_locations))
            # Address all locations with specific dates assigned.
            for i in range(0, self.number_nights):
                date = self.start_date + datetime.timedelta(days=i)
                filtered_locations = locations.filter(date=date)
                if filtered_locations.count() > 0:
                    datelist.append(datehash[date])
                    loclist.append(list(filtered_locations))
            locrange = range(len(datelist))
        return{
            'datelist': datelist,
            'locationlist': loclist,
            'locationrange': locrange
        }





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

    def __init__(self):
        super(TripLocation, self).__init__()
        datehash = self.trip.get_datehash()
        date_choices = []
        for key, value in datehash:
            date_choices.append((key, value))
        date_choices = tuple(date_choices)

    location_type = models.CharField(max_length=2,
        choices=LOCATION_TYPE_CHOICES)
    title = models.CharField(max_length = 255, blank=True)
    date = models.DateField(null=True, blank=True, choices=date_choices, default = None)
    latitude = models.CharField(max_length = 31, blank=True)
    longitude = models.CharField(max_length = 31, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
