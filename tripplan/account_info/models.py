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
        return self.full_name

    def get_preferred_name(self):
        return self.preferred_name

#TESTING TO ADD:
# -vehicle is deleted with user
class Vehicle(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=4, blank=True)
    color = models.CharField(max_length=20, blank=True)
    lic_plate_num = models.CharField(max_length=20, blank=True)
    lic_plate_st = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.year + ' ' + self.make + ' ' + self.model

#TESTING TO ADD:
# -contact is deleted with user
class EmergencyContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    preferred_name = models.CharField(max_length=255, blank=True)
    relationship = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=100, blank=True)
    primary_phone = models.CharField(max_length=20, blank=True)
    secondary_phone = models.CharField(max_length=20, blank=True)
    street_address_line1 = models.CharField(max_length=50, blank=True)
    street_address_line2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
