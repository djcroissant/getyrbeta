import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Trip, Vehicle, User

def create_trip(title, days):
    """
    Create a trip with the give 'title' and with a start_date the given
    number of 'days' offset from now (negative for past, positive for future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Trip.objects.create(title=title, start_date=time)

def create_user(first_name, last_name):
    """
    Create a user with the given 'first_name' and 'last_name'
    """
    return User.objects.create(first_name=first_name, last_name=last_name)

def create_vehicle(user, year, make, model):
    """
    Create a vehicle with the given 'year', 'make', and 'model'
    NOTE: future functionality should include a user association
    """
    return user.vehicle_set.create(year=year, make=make, model=model)

class TripModelTests(TestCase):

    def test_is_in_the_past_with_today_trip(self):
        """
        is_in_the_past() returns False for trips whose start_date is today
        or in the future
        """
        date = timezone.now().date()
        future_trip = Trip(start_date=date)
        self.assertIs(future_trip.is_in_the_past(), False)

    def test_is_in_the_past_with_past_trip(self):
        """
        is_in_the_past() returns True for trips whose start_date is in the past
        """
        date = timezone.now().date() - datetime.timedelta(days=1)
        future_trip = Trip(start_date=date)
        self.assertIs(future_trip.is_in_the_past(), True)

class TripListViewTests(TestCase):
    def test_no_trips(self):
        """
        If no trips exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('trips:trip_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no trip information available")
        self.assertQuerysetEqual(response.context['upcoming_trip_list'], [])

    def test_past_trip(self):
        """
        Trips with a start_date in the past are not displayed on the trip_list
        page
        """
        create_trip(title="Past trip", days = -1)
        response = self.client.get(reverse('trips:trip_list'))
        self.assertContains(response, "There is no trip information available")
        self.assertQuerysetEqual(response.context['upcoming_trip_list'], [])

    def test_future_trip(self):
        """
        Trips with a start_date today or in the future are displayed on the
        trip_list page
        """
        create_trip(title="Future trip", days = 0)
        response = self.client.get(reverse('trips:trip_list'))
        self.assertQuerysetEqual(
            response.context['upcoming_trip_list'],
            ['<Trip: Future trip>']
        )

    def test_future_trip_and_past_trip(self):
        """
        When both past and future trips exist, only trips with start_date
        today or in the future are displayed
        """
        create_trip(title="Past trip", days = -1)
        create_trip(title="Future trip", days = 0)
        response = self.client.get(reverse('trips:trip_list'))
        self.assertQuerysetEqual(
            response.context['upcoming_trip_list'],
            ['<Trip: Future trip>']
        )

    def test_two_future_trips(self):
        """
        When thre are multiple future trips, both are displayed
        """
        create_trip(title="Today trip", days = 0)
        create_trip(title="Future trip", days = 30)
        response = self.client.get(reverse('trips:trip_list'))
        self.assertQuerysetEqual(
            response.context['upcoming_trip_list'],
            ['<Trip: Today trip>', '<Trip: Future trip>']
        )

class VehicleViewTests(TestCase):
    def test_invalid_vehicle_id(self):
        """
        If no vehicles exists for the given id, a 404 response is given
        """
        url = reverse('trips:vehicle_detail', args=(9999999999999,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_valid_vehicle(self):
        """
        When a valid vehicle exists for the given id, it is displayed
        appropriately
        """
        user = create_user(first_name="Bob", last_name="Hope")
        vehicle = create_vehicle(user=user, year="2010", make="Toyota", model="Tacoma")
        url = reverse('trips:vehicle_detail', args=(vehicle.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
