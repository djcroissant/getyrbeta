from django import template

from trips.models import TripLocation

register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def convert_location(location):
    if location == TripLocation.BEGIN:
        return 'trailhead'
    elif location == TripLocation.END:
        return 'endpoint'
    elif location == TripLocation.OBJECTIVE:
        return 'objective'
    elif location == TripLocation.CAMP:
        return 'camp'
