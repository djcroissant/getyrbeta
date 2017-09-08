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

    is_in_the_past.admin_order_field = 'start_date'
    is_in_the_past.boolean = True
    is_in_the_past.short_description = 'Past Trip?'
