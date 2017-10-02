import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.utils import DataError

from account_info.models import User

from trips.models import Trip, SunTime, Item, ItemOwner, TripMember


class TripModelTests(TestCase):
    def test_invalid_trip_without_title(self):
        title = ''
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        self.assertRaises(ValidationError, lambda: trip.full_clean())

    def test_invalid_trip_without_start_date(self):
        title = 'title'
        start_date = ''
        test = lambda: Trip.objects.create(title=title, start_date=start_date)
        self.assertRaises(ValidationError, test)

    def test_trip_number_nights_defaults_to_zero(self):
        '''  If trip.number_nights isn't specified, it will default to zero '''
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        self.assertEqual(trip.number_nights, 0)

    def test_valid_trip_with_only_required_fields(self):
        '''
        No exception raised when a trip is created with only the required
        fields defined: title and number_nights. trailhead_latitude,
        trailhead_longitude, destination, and start_date are all optional.
        '''
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        try:
            trip.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

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

    def test_string_representation(self):
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        self.assertEqual(str(trip), trip.title)

    def test_title_length_equal_to_255_is_valid(self):
        title = "x"*255
        start_date = timezone.now().date()
        try:
            trip = Trip.objects.create(title=title, start_date=start_date)
        except:
            self.fail("A title with 255 characters should be valid.")

    def test_title_length_greater_than_255_raises_DataError(self):
        title = "x"*256
        start_date = timezone.now().date()
        test = lambda: Trip.objects.create(title=title, start_date=start_date)
        self.assertRaises(DataError, test)

    def test_destination_length_equal_to_255_is_valid(self):
        title = 'title'
        start_date = timezone.now().date()
        destination = "x"*255
        try:
            trip = Trip.objects.create(title=title, start_date=start_date,
                destination=destination)
        except:
            self.fail("A destination with 255 characters should be valid.")

    def test_destination_length_greater_than_255_invalid(self):
        title = 'title'
        start_date = timezone.now().date()
        destination = "x"*256
        test = lambda: Trip.objects.create(title=title, start_date=start_date,
            destination=destination)
        self.assertRaises(DataError, test)

class SunTimeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create a valid instance of Trip '''
        cls.trip = Trip.objects.create(title='title',
            start_date=timezone.now().date())

    def test_invalid_SunTime_without_dawn(self):
        test = lambda: SunTime.objects.create(
            dawn='',
            dusk=timezone.now().time(),
            sunrise=timezone.now().time(),
            sunset=timezone.now().time(),
            date=timezone.now().date(),
            trip=self.trip
        )
        self.assertRaises(ValidationError, test)

    def test_invalid_SunTime_without_dusk(self):
        test = lambda: SunTime.objects.create(
            dawn=timezone.now().time(),
            dusk='',
            sunrise=timezone.now().time(),
            sunset=timezone.now().time(),
            date=timezone.now().date(),
            trip=self.trip
        )
        self.assertRaises(ValidationError, test)

    def test_invalid_SunTime_without_sunrise(self):
        test = lambda: SunTime.objects.create(
            dawn=timezone.now().time(),
            dusk=timezone.now().time(),
            sunrise='',
            sunset=timezone.now().time(),
            date=timezone.now().date(),
            trip=self.trip
        )
        self.assertRaises(ValidationError, test)

    def test_invalid_SunTime_without_sunset(self):
        test = lambda: SunTime.objects.create(
            dawn=timezone.now().time(),
            dusk=timezone.now().time(),
            sunrise=timezone.now().time(),
            sunset='',
            date=timezone.now().date(),
            trip=self.trip
        )
        self.assertRaises(ValidationError, test)

    def test_invalid_SunTime_without_date(self):
        test = lambda: SunTime.objects.create(
            dawn=timezone.now().time(),
            dusk=timezone.now().time(),
            sunrise=timezone.now().time(),
            sunset=timezone.now().time(),
            date='',
            trip=self.trip
        )
        self.assertRaises(ValidationError, test)

    def test_valid_SunTime_with_only_required_fields(self):
        '''
        No exception raised when a SunTime is created with only the required
        fields defined (all of them).
        '''
        test = SunTime.objects.create(
            dawn=timezone.now().time(),
            dusk=timezone.now().time(),
            sunrise=timezone.now().time(),
            sunset=timezone.now().time(),
            date=timezone.now().date(),
            trip=self.trip
        )
        try:
            test.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

class ItemModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create a valid instance of Trip '''
        cls.trip = Trip.objects.create(title='title',
            start_date=timezone.now().date())

    def test_invalid_item_without_description(self):
        test = Item.objects.create(description='', trip=self.trip)
        self.assertRaises(ValidationError, lambda: test.full_clean())

    def test_description_length_equal_to_255_is_valid(self):
        try:
            Item.objects.create(description=("x"*255), trip=self.trip)
        except:
            self.fail("A description with 255 characters should be valid.")

    def test_description_length_greater_than_255_invalid(self):
        test = lambda: Item.objects.create(description=("x"*256), trip=self.trip)
        self.assertRaises(DataError, test)

    def test_item_quantity_defaults_to_one(self):
        '''  If item.quantity isn't specified, it will default to one '''
        title = 'title'
        start_date = timezone.now().date()
        item = Item.objects.create(description='test', trip=self.trip)
        self.assertEqual(item.quantity, 1)

class ItemOwnerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create valid instances of Trip, User, and Item '''
        trip = Trip.objects.create(title='title',
            start_date=timezone.now().date())
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        cls.item = Item.objects.create(description='test', trip=trip)

    def test_accept_reqd_defaults_to_false(self):
        ''' If accept_reqd isn't specified, it will default to False '''
        item_owner = ItemOwner.objects.create(item=self.item, owner=self.user)
        self.assertEqual(item_owner.accept_reqd, False)

class TripMemberModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create valid instances of Trip and User '''
        cls.trip = Trip.objects.create(title='title',
            start_date=timezone.now().date())
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_accept_reqd_defaults_to_false(self):
        ''' If accept_reqd isn't specified, it will default to False '''
        trip_member = TripMember.objects.create(trip=self.trip, member=self.user)
        self.assertEqual(trip_member.accept_reqd, False)

    def test_organizer_defaults_to_false(self):
        ''' If organizer isn't specified, it will default to False '''
        trip_member = TripMember.objects.create(trip=self.trip, member=self.user)
        self.assertEqual(trip_member.organizer, False)

class ModelRelationshipTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create valid instances of User, Trip, and Item '''
        trip = Trip.objects.create(title='title',
            start_date=timezone.now().date())
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        item = Item.objects.create(description='test', trip=trip)
        ItemOwner.objects.create(item=item, owner=user)
        TripMember.objects.create(trip=trip, member=user)
        cls.trip = trip
        cls.item = item

    def test_trip_has_members_through_TripMember_model(self):
        '''
        Trip has a ManyToMany relationship with User through TripMember
        '''
        self.assertEqual(self.trip.trip_members.count(), 1)

    def test_item_has_owners_through_ItemOwner_model(self):
        '''
        Item has a ManyToMany relationship with User through ItemOwner
        '''
        self.assertEqual(self.item.item_owners.count(), 1)
