from django.conf import settings
from django.db import models


#TESTING TO ADD:
# -vehicle is deleted with user
class Vehicle(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20)
    lic_plate_num = models.CharField(max_length=20)
    lic_plate_st = models.CharField(max_length=2)

    def __str__(self):
        return self.year + ' ' + self.make + ' ' + self.model

#TESTING TO ADD:
# -contact is deleted with user
class EmergencyContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    preferred_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20)
    street_address_line1 = models.CharField(max_length=50)
    street_address_line2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
