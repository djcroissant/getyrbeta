from django.db import models
from django.utils import timezone

class Trip(models.Model):
    trailhead_latitude = models.CharField(max_length = 20)
    trailhead_longitude = models.CharField(max_length = 20)
    title = models.CharField(max_length = 50)
    start_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.title

    def is_in_the_past(self):
        return self.start_date < timezone.now().date()

class User(models.Model):
    trips = models.ManyToManyField(Trip)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20)
    lic_plate_num = models.CharField(max_length=20)
    lic_plate_st = models.CharField(max_length=2)

    def __str__(self):
        return self.year + ' ' + self.make + ' ' + self.model
