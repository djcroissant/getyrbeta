import datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Trip(models.Model):
    title = models.CharField(max_length = 255)
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

    def get_date_choices(self):
        """
        This function returns a list of choices for the date field.
        Example: ["Unassigned", "Day X - Month, DD YYYY"]
        TripLocation.date field will hold one of these choices as a string.
        """
        datelist = ["Unassigned"]
        for i in range(0, self.number_nights):
            day_value = "Day " + str(i + 1)
            date_value = self.start_date + datetime.timedelta(days=i)
            datelist.append(day_value + ' - ' + str(date_value))
        return datelist

    def get_location_context(self, location_type):
        """
        This function returns a dictionary. There is a key for each date
        returned by get_date_choices(). Each value is a list of locations
        corresponding to the key.
        """
        context = {}
        datelist = self.get_date_choices()
        for date in datelist:
            locations = self.triplocation_set.filter(
                location_type=location_type,
                date=date
            )
            context[date] = list(locations)
        return context

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
    email = models.CharField(max_length=255)

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

    location_type = models.CharField(
        max_length=2,
        choices=LOCATION_TYPE_CHOICES
    )
    title = models.CharField(max_length = 255, blank=True)
    date = models.CharField(
        max_length = 255,
        default='Unassigned',
    )
    latitude = models.CharField(max_length = 31, blank=True)
    longitude = models.CharField(max_length = 31, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def date_assigned(self):
        """
        This function returns false if date == "Unassigned"
        else true (i.e. date field has a Date assigned)
        """
        if self.date == "Unassigned":
            return False
        else:
            return True

    def get_date(self):
        """
        This function returns the date if it is assigned.
        Else returns "Unassigned"
        """
        if self.date_assigned():
            date_components = self.date.split(' - ')
            date={}
            date['day'] = date_components[0]
            date['date'] = datetime.datetime.strptime(date_components[1], '%Y-%m-%d').date()
            return date['date']
        else:
            return "Unassigned"

    def get_date_choices(self):
        """
        This function returns a list of choices for the date field on forms
        """
        return self.trip.get_date_choices()

    def clean_fields(self, exclude=None):
        """
        The value for date must be one of those returned by the
        Trip.get_date_choices() method
        """
        super(TripLocation, self).clean_fields(exclude=None)
        if self.date not in self.get_date_choices():
            if exclude and 'date' in exclude:
                raise ValidationError(
                    '%s is not a valid date format.' % self.date
                )
            else:
                raise ValidationError(
                    {
                        'date': '%s is not a valid date format.' % self.date
                    }
                )
