from django import template

from trips.models import TripLocation

register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]
