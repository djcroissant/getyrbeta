from django.conf import settings
from django.db import models

from authtools.models import AbstractEmailUser

from trips.models import TripGuest, TripMember

class User(AbstractEmailUser):
    full_name = models.CharField('full name', max_length=255, blank=True)
    preferred_name = models.CharField('preferred name',
        max_length=255, blank=True)
    primary_phone = models.CharField(max_length=31, blank=True)
    secondary_phone = models.CharField(max_length=31, blank=True)
    street_address_line1 = models.CharField(max_length=255, blank=True)
    street_address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        '''
        After saving a new user, check if any TripGuest instances exist
        for the user's email. If so, create corresponding instances of
        TripMember with 'accept_reqd' = True.
        '''
        # User instance will not have pk if it is being created
        if not self.pk:
            # save instance so it can be referenced by TripMember
            response = super(User, self).save(*args, **kwargs)
            trip_guests = TripGuest.objects.filter(email__iexact=self.email)
            for trip_guest in trip_guests:
                TripMember.objects.create(
                    member=self,
                    trip=trip_guest.trip,
                    organizer=True,
                    accept_reqd=True
                )
                trip_guest.delete()
            return response
        else:
            super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.email

    def get_short_name(self):
        if self.preferred_name:
            return self.preferred_name
        elif self.full_name:
            return self.full_name
        else:
            return self.email

class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=63)
    model = models.CharField(max_length=63)
    year = models.CharField(max_length=4, blank=True)
    color = models.CharField(max_length=63)
    lic_plate_num = models.CharField(max_length=15)
    lic_plate_st = models.CharField(max_length=2)

    def __str__(self):
        if self.year:
            return self.year + ' ' + self.make + ' ' + self.model
        else:
            return self.make + ' ' + self.model

    def get_owner(self):
        return self.owner

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    preferred_name = models.CharField(max_length=255, blank=True)
    relationship = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    primary_phone = models.CharField(max_length=31, blank=True)
    secondary_phone = models.CharField(max_length=31, blank=True)
    street_address_line1 = models.CharField(max_length=255, blank=True)
    street_address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=15, blank=True)

    def __str__(self):
        if self.preferred_name:
            return self.relationship + ': ' + self.preferred_name
        else:
            return self.relationship + ': ' + self.full_name

    def get_user(self):
        return self.user
