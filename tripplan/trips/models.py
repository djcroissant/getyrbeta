import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
import pytz
import requests


class Trip(models.Model):
    title = models.CharField(max_length = 255)
    start_date = models.DateField()
    number_nights = models.PositiveSmallIntegerField(default=0)
    trip_members = models.ManyToManyField(settings.AUTH_USER_MODEL,
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

    def get_date_choices(self, date_type='day'):
        """
        This function returns a list of choices for the date field.
        Example: [Day X - Month, DD YYYY", ...]
        TripLocation.date field will hold one of these choices as a string.
        """
        datelist = []
        if date_type == 'night':
            range_limit = self.number_nights
            prefix = 'Night'
        else:
            range_limit = self.number_nights + 1
            prefix = 'Day'

        for i in range(0, range_limit):
            text_half = prefix + " " + str(i + 1)
            date_half = self.start_date + datetime.timedelta(days=i)
            datelist.append(text_half + ' - ' + str(date_half))
        return datelist

    def get_location_context(self, location_type):
        """
        This function returns a dictionary. There is a key for each date
        returned by get_date_choices(). Each value is a list of locations
        corresponding to the key.
        """
        context = {}
        if location_type == TripLocation.CAMP:
            datelist = self.get_date_choices(date_type='night')
        else:
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

    def clean_fields(self, exclude=None):
        super(Trip, self).clean_fields(exclude=None)
        if self.is_in_the_past():
            raise ValidationError('The start date may not be in the past')

    is_in_the_past.admin_order_field = 'start_date'
    is_in_the_past.boolean = True
    is_in_the_past.short_description = 'Past Trip?'

class Item(models.Model):
    description = models.CharField(max_length = 255)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    item_owners = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='ItemOwner')

    def __str__(self):
        return self.description

class ItemOwner(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    accept_reqd = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.email

class TripMember(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    organizer = models.BooleanField(default=False)
    accept_reqd = models.BooleanField(default=False)

    def __str__(self):
        return self.member.email

class TripGuest(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class TripLocation(models.Model):
    # Set variables to allow human-friendly access to location types
    BEGIN = 'ST'
    END = 'EN'
    OBJECTIVE = 'OB'
    CAMP = 'CM'

    # Types of locations
    LOCATION_TYPE_CHOICES = (
        (BEGIN, 'Trailhead'),
        (END, 'Endpoint'),
        (OBJECTIVE, 'Objective'),
        (CAMP, 'Camp'),
    )

    # Used in trips/views.py
    LOCATION_TYPE = {
        'trailhead': BEGIN,
        'endpoint': END,
        'objective': OBJECTIVE,
        'camp': CAMP
    }

    # Model fields
    location_type = models.CharField(
        max_length=2,
        choices=LOCATION_TYPE_CHOICES
    )
    title = models.CharField(max_length = 255, blank=True)
    date = models.CharField(
        max_length = 255,
        default='Unassigned',
    )
    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    # Celestial Times:
    dawn = models.TimeField(blank=True, null=True)
    dusk = models.TimeField(blank=True, null=True)
    sunrise = models.TimeField(blank=True, null=True)
    sunset = models.TimeField(blank=True, null=True)

    @property
    def get_location_type_verbose(self):
        """
        Uses @property decorator so it can be called from template.
        This function will return the verbose form of the location_type
        """
        location_type = {
            self.BEGIN: 'trailhead',
            self.END: 'endpoint',
            self.OBJECTIVE: 'objective',
            self.CAMP: 'camp'
        }
        return location_type[self.location_type]

    def get_date(self):
        """
        This function returns the date if it is assigned.
        Else raises an ValueError exception
        """
        try:
            date_components = self.date.split(' - ')
            date={}
            date['day'] = date_components[0]
            date['date'] = datetime.datetime.strptime(date_components[1], '%Y-%m-%d').date()
        except:
            raise ValueError('Could not parse date correctly: %s' % self.date)
        return date['date']

    def get_date_choices(self, date_type='day'):
        """
        This function returns a list of choices for the date field on forms
        """
        return self.trip.get_date_choices(date_type)

    def clean_fields(self, exclude=None):
        """
        The value for date must be one of those returned by the
        Trip.get_date_choices() method
        """
        super(TripLocation, self).clean_fields(exclude=None)
        if self.location_type == self.CAMP:
            date_type = 'night'
        else:
            date_type = 'day'
        if self.date not in self.get_date_choices(date_type):
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

    def get_timezone(self):
        date_at_midnight = str(int(datetime.datetime.combine(
            self.get_date(),
            datetime.datetime.min.time()
        ).timestamp()))
        try:
            return_value = requests.get(
                'https://maps.googleapis.com/maps/api/timezone/json',
                params={
                    'location': f'{self.latitude}, {self.longitude}',
                    'timestamp': date_at_midnight,
                    'key': settings.GOOGLE_MAPS_API,
                }
            ).json()
        except KeyError:
            return_value = {}

        return return_value

    def get_suntimes_in_utc(self):
        """
        Get sun times from API. Requires latitude, longitude, and date
        to be specified. Otherwise returns an empty dict
        """
        try:
            suntime_response = requests.get(
                'https://api.sunrise-sunset.org/json',
                params={
                    'lat': self.latitude,
                    'lng': self.longitude,
                    'date': datetime.datetime.strftime(
                        self.get_date(), '%Y-%m-%d'
                    ),
                    'formatted': 0,
                }
            ).json()
            return_value = {
                'sunrise': datetime.datetime.strptime(
                    suntime_response['results']['sunrise'],
                    '%Y-%m-%dT%H:%M:%S+00:00'
                ).replace(tzinfo=pytz.utc),
                'sunset':  datetime.datetime.strptime(
                    suntime_response['results']['sunset'],
                    '%Y-%m-%dT%H:%M:%S+00:00'
                ).replace(tzinfo=pytz.utc),
            }
        except KeyError:
            return_value = {}

        return return_value

    def set_suntimes(self):
        """
        Set sun times in local timezone
        """
        local_timezone = pytz.timezone(
            self.get_timezone()['timeZoneId']
        )

        suntimes = self.get_suntimes_in_utc()
        self.sunrise = suntimes['sunrise'].astimezone(
            local_timezone
        ).strftime('%H:%M:%S %Z%z')
        self.sunset = suntimes['sunset'].astimezone(
            local_timezone
        ).strftime('%H:%M:%S %Z%z')

    def clear_suntimes(self):
        """
        Clear sun time values. To be used if a location is edited to no
        longer include lat/long/date
        """
        self.sunrise = None
        self.sunset = None

    def save(self, *args, **kwargs):
        """
        Set sun times for a location with specified coordinates and date
        """
        if self.latitude and self.longitude and self.date and self.date != 'Unassigned':
            self.set_suntimes()
        else:
            self.clear_suntimes()
        super(TripLocation, self).save(*args, **kwargs)

class ItemNotification(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='owners')
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length = 255)
