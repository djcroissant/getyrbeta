from django.conf import settings
from django.db import models

from authtools.models import AbstractEmailUser

class User(AbstractEmailUser):
    full_name = models.CharField('full name', max_length=255, blank=True)
    preferred_name = models.CharField('preferred name',
        max_length=255, blank=True)
    primary_phone = models.CharField(max_length=20, blank=True)
    secondary_phone = models.CharField(max_length=20, blank=True)
    street_address_line1 = models.CharField(max_length=50, blank=True)
    street_address_line2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)


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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    make = models.CharField(max_length=50, blank=False)
    model = models.CharField(max_length=50, blank=False)
    year = models.CharField(max_length=4, blank=True)
    color = models.CharField(max_length=20, blank=False)
    lic_plate_num = models.CharField(max_length=20, blank=False)
    lic_plate_st = models.CharField(max_length=2, blank=False)

    def __str__(self):
        if self.year:
            return self.year + ' ' + self.make + ' ' + self.model
        else:
            return self.make + ' ' + self.model

    def get_owner(self):
        return self.owner

class EmergencyContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=False)
    preferred_name = models.CharField(max_length=255, blank=True)
    relationship = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=100, blank=True)
    primary_phone = models.CharField(max_length=20, blank=True)
    secondary_phone = models.CharField(max_length=20, blank=True)
    street_address_line1 = models.CharField(max_length=50, blank=True)
    street_address_line2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        if self.preferred_name:
            return self.relationship + ': ' + self.preferred_name
        else:
            return self.relationship + ': ' + self.full_name

    def get_user(self):
        return self.user
