import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError

from account_info.models import User

from trips.models import Trip, SunTime, Item, ItemOwner, TripMember, \
    TripLocation


class TripModelTests(TestCase):
    def test_trip_invalid_without_title(self):
        title = ''
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        self.assertRaises(ValidationError, lambda: trip.full_clean())

    def test_trip_invalid_without_start_date(self):
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

    def test_trip_valid_with_only_required_fields(self):
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

    def test_trip_string_representation(self):
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        self.assertEqual(str(trip), trip.title)

    def test_trip_title_length_equal_to_255_is_valid(self):
        title = "x"*255
        start_date = timezone.now().date()
        try:
            trip = Trip.objects.create(title=title, start_date=start_date)
        except:
            self.fail("A title with 255 characters should be valid.")

    def test_trip_title_length_greater_than_255_raises_DataError(self):
        title = "x"*256
        start_date = timezone.now().date()
        test = lambda: Trip.objects.create(title=title, start_date=start_date)
        self.assertRaises(DataError, test)

    def test_get_trailhead_returns_trailhead_location_if_exists(self):
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        location_type = TripLocation.BEGIN
        trailhead = TripLocation.objects.create(
            location_type=location_type, trip=trip)
        self.assertEqual(trip.get_trailhead(), trailhead)

    def test_get_trailhead_returns_None_if_no_trailhead(self):
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        self.assertEqual(trip.get_trailhead(), None)

    def test_get_endpoint_returns_endpoint_location_if_exists(self):
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        location_type = TripLocation.END
        endpoint = TripLocation.objects.create(
            location_type=location_type, trip=trip)
        self.assertEqual(trip.get_endpoint(), endpoint)

    def test_get_endpoint_returns_None_if_no_endpoint(self):
        title = 'title'
        start_date = timezone.now().date()
        trip = Trip.objects.create(title=title, start_date=start_date)
        self.assertEqual(trip.get_endpoint(), None)

    def test_get_date_choices_method_for_number_nights_zero(self):
        """
        Trip.get_date_choices() should return a list with 'Day 1 - YYYY-MM-DD'
        as the only element if number_nights == 0 and date_type != 'night'
        """
        title = 'title'
        start_date = timezone.now().date()
        number_nights = 0
        trip = Trip.objects.create(
            title=title, start_date=start_date, number_nights=number_nights)
        self.assertEqual(trip.get_date_choices(), ['Day 1 - ' + str(start_date)])

    def test_get_date_choices_method_for_number_nights_greater_than_zero(self):
        """
        Trip.get_date_choices() should return a list with
        'Day N = YY/MM/DD' for each day of the trip if date_type != 'night'
        """
        title = 'title'
        start_date = timezone.now().date()
        number_nights = 2
        manual_date_list = [
            'Day 1 - ' + str(start_date),
            'Day 2 - ' + str(start_date + datetime.timedelta(days=1)),
            'Day 3 - ' + str(start_date + datetime.timedelta(days=2)),
        ]
        trip = Trip.objects.create(
            title=title, start_date=start_date, number_nights=number_nights)
        self.assertEqual(trip.get_date_choices(), manual_date_list)

    def test_get_date_choices_method_for_number_nights_zero_night(self):
        """
        Trip.get_date_choices() should return an empty list
        if number_nights == 0 and date_type == 'night'
        """
        title = 'title'
        date_type = 'night'
        start_date = timezone.now().date()
        number_nights = 0
        trip = Trip.objects.create(
            title=title, start_date=start_date, number_nights=number_nights)
        self.assertEqual(trip.get_date_choices(date_type), [])

    def test_get_date_choices_method_for_number_nights_greater_than_zero_night(self):
        """
        Trip.get_date_choices() should return a list with
        'Night N = YY/MM/DD' for each night of the trip if date_type == 'night'
        """
        title = 'title'
        date_type = 'night'
        start_date = timezone.now().date()
        number_nights = 2
        manual_date_list = [
            'Night 1 - ' + str(start_date),
            'Night 2 - ' + str(start_date + datetime.timedelta(days=1)),
        ]
        trip = Trip.objects.create(
            title=title, start_date=start_date, number_nights=number_nights)
        self.assertEqual(trip.get_date_choices(date_type), manual_date_list)

    def test_get_location_context_with_two_locations_and_dates(self):
        """
        Testing two TripLocation objects, both with date="Day 1 - ..."
        """
        title = 'title'
        start_date = timezone.now().date()
        number_nights = 1
        trip = Trip.objects.create(
            title=title, start_date=start_date, number_nights=number_nights)
        location_type = TripLocation.OBJECTIVE
        location_date = 'Day 1 - ' + str(start_date)
        for i in range(2):
            TripLocation.objects.create(
            title=str(i), location_type=location_type, trip=trip, date=location_date)
        manual_location_context = {
            location_date: list(trip.triplocation_set.filter(
                location_type=location_type, date=location_date)),
            ('Day 2 - ' + str(start_date + datetime.timedelta(days=1))): []
        }
        self.assertEqual(trip.get_location_context(location_type),
            manual_location_context)

    def test_get_location_context_with_two_locations_and_two_dates(self):
        """
        Testing four TripLocation objects: two with date="Day 1 - ..."
        and two with date="Day 2 - ..."
        """
        title = 'title'
        start_date = timezone.now().date()
        number_nights = 1
        trip = Trip.objects.create(
            title=title, start_date=start_date, number_nights=number_nights)
        location_type = TripLocation.OBJECTIVE
        location_date = "Day 1 - " + str(start_date)
        for i in range(2):
            TripLocation.objects.create(
            title=str(i), location_type=location_type, trip=trip, date=location_date)
        location_date = "Day 2 - " + str(start_date + datetime.timedelta(days=1))
        for i in range(2):
            TripLocation.objects.create(
            title=str(i), location_type=location_type, trip=trip, date=location_date)
        manual_location_context = {
            ("Day 1 - " + str(start_date)): list(trip.triplocation_set.filter(
            location_type=location_type, date="Day 1 - " + str(start_date))),
            ("Day 2 - " + str(start_date + datetime.timedelta(days=1))): list(trip.triplocation_set.filter(
                location_type=location_type, date=("Day 2 - " + str(start_date + datetime.timedelta(days=1)))))
        }
        self.assertEqual(trip.get_location_context(location_type),
            manual_location_context)

    def test_trip_is_in_the_past_with_today_trip(self):
        """
        is_in_the_past() returns False for trips whose start_date is today
        or in the future
        """
        date = timezone.now().date()
        future_trip = Trip(start_date=date)
        self.assertIs(future_trip.is_in_the_past(), False)

    def test_trip_is_in_the_past_with_past_trip(self):
        """
        is_in_the_past() returns True for trips whose start_date is in the past
        """
        date = timezone.now().date() - datetime.timedelta(days=1)
        future_trip = Trip(start_date=date)
        self.assertIs(future_trip.is_in_the_past(), True)

class TripLocationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create a valid instance of Trip '''
        cls.trip = Trip.objects.create(
            title='title',
            start_date=timezone.now().date(),
            number_nights=1
        )

    def test_date_default_is_unassigned(self):
        test = TripLocation.objects.create(trip=self.trip)
        self.assertEqual(test.date, 'Unassigned')

    def test_invalid_with_null_date(self):
        date = None
        location_type = 'CM'
        test = lambda: TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertRaises(IntegrityError, test)

    def test_invalid_with_blank_date(self):
        date = ''
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertRaises(ValidationError, lambda: test.full_clean())

    def test_invalid_without_location_type(self):
        date = 'fake'
        location_type = ''
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertRaises(ValidationError, lambda: test.full_clean())

    def test_valid_with_only_required_fields(self):
        '''
        No exception raised when TripLocation is created with only the required
        fields defined: date, trip_location, trip
        '''
        date = "Night 1 - " + str(self.trip.start_date)
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        try:
            test.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

    def test_class_attributes_for_location_types(self):
        """
        TripLocation defines class attributes for location_type:
            BEGIN = 'ST'
            END = 'EN'
            OBJECTIVE = 'OB'
            CAMP = 'CM'
        """
        test = TripLocation.objects.create(trip=self.trip)
        self.assertEqual(test.BEGIN, 'ST')
        self.assertEqual(test.END, 'EN')
        self.assertEqual(test.OBJECTIVE, 'OB')
        self.assertEqual(test.CAMP, 'CM')

    def test_verbose_name_for_location_types(self):
        """
        TripLocation defines a tuple of location_type choices:
                (BEGIN, 'Start Location')
                (END, 'End Location')
                (OBJECTIVE, 'Objective Location')
                (CAMP, 'Camp Location')
        """
        test = TripLocation.objects.create(trip=self.trip)
        self.assertEqual(len(test.LOCATION_TYPE_CHOICES), 4)
        self.assertEqual(test.LOCATION_TYPE_CHOICES[0],
            (test.BEGIN, 'Trailhead'))
        self.assertEqual(test.LOCATION_TYPE_CHOICES[1],
            (test.END, 'Endpoint'))
        self.assertEqual(test.LOCATION_TYPE_CHOICES[2],
            (test.OBJECTIVE, 'Objective'))
        self.assertEqual(test.LOCATION_TYPE_CHOICES[3],
            (test.CAMP, 'Camp'))

    def test_get_date_method_raises_exception(self):
        """
        The TripLocation.get_date() method will raise an exception if the
        date is not in expected format: "Day X - YYYY-MM-DD"
        """
        date = 'Unassigned'
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertRaises(ValueError, lambda: test.get_date())

    def test_get_date_method_returns_date(self):
        """
        The TripLocation.get_date() method will return the date in Date format
        if TripLocation.date = 'Day X - YY-MM-DD'
        """
        date = 'Day 1 - ' + str(self.trip.start_date)
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertEqual(test.get_date(), self.trip.start_date)

    def test_get_date_choices(self):
        """
        This method returns the same result as the Trip model method by
        the same name
        """
        date = 'Day 1 - ' + str(self.trip.start_date)
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertEqual(test.get_date_choices(), self.trip.get_date_choices())

    def test_validation_error_for_invalid_date(self):
        """
        Tests the TripLocation.clean_fields() method
        """
        date = 'Invalid date'
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertRaises(ValidationError, lambda: test.full_clean())

    def test_valid_for_valid_date_with_day(self):
        """
        Tests the TripLocation.clean_fields() method for location_type=objective
        """
        date = 'Day 1 - ' + str(self.trip.start_date)
        location_type = 'OB'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        try:
            test.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

    def test_valid_for_valid_date_with_night(self):
        """
        Tests the TripLocation.clean_fields() method for location_type=camp
        """
        date = 'Night 1 - ' + str(self.trip.start_date)
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        try:
            test.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

    def test_get_location_type_verbose_for_type_begin(self):
        date = 'fake'
        location_type = 'ST'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertEqual('trailhead', test.get_location_type_verbose)

    def test_get_location_type_verbose_for_type_end(self):
        date = 'fake'
        location_type = 'EN'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertEqual('endpoint', test.get_location_type_verbose)

    def test_get_location_type_verbose_for_type_objective(self):
        date = 'fake'
        location_type = 'OB'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertEqual('objective', test.get_location_type_verbose)

    def test_get_location_type_verbose_for_type_camp(self):
        date = 'fake'
        location_type = 'CM'
        test = TripLocation.objects.create(date=date,
            trip=self.trip, location_type=location_type)
        self.assertEqual('camp', test.get_location_type_verbose)

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
