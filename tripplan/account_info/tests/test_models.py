from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from account_info.models import User, Vehicle, EmergencyContact

class UserModelTests(TestCase):
    def test_invalid_user_without_email(self):
        '''
        An exception is raised when a user with blank email is validated
        '''
        user = User.objects.create_user(email='', password='ValidPassword')
        self.assertRaises(ValidationError, lambda: user.full_clean())

    # def test_invalid_user_without_password(self):
    #     '''
    #     An exception is raised when a user with blank password is validated
    #     '''
    #     invaliduser = User.objects.create_user(email='new@email.com', password='')
    #     self.assertRaises(ValidationError, lambda: invaliduser.full_clean())

    def test_valid_user_with_only_email_and_password(self):
        '''
        No exception is raised when only email and password are defined and all
        other user fields are blank
        '''
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        try:
            user.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

    def test_get_full_name_returns_full_name(self):
        '''
        If the get_full_name method is called on a user with a full_name
        defined, the user's full_name is returned
        '''
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword', full_name='Bob Hope')
        self.assertEqual(user.get_full_name(), user.full_name)

    def test_get_full_name_with_blank_full_name_gives_email(self):
        '''
        If the get_full_name method is called on a user with a blank
        full_name, the user's email is returned
        '''
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        self.assertEqual(user.get_full_name(), user.email)

    def test_get_short_name_returns_preferred_name(self):
        '''
        If the get_short_name method is called on a user with a preferred_name
        defined, the user's preferred_name is returned
        '''
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword', preferred_name='BobO')
        self.assertEqual(user.get_short_name(), user.preferred_name)

    def test_get_short_name_with_blank_short_name_gives_full_name(self):
        '''
        If the get_short_name method is called on a user with a blank
        short_name, the user's full_name is returned
        '''
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword', full_name='Bob Hope')
        self.assertEqual(user.get_short_name(), user.full_name)

    def test_get_full_name_with_blank_short_and_full_name_gives_email(self):
        '''
        If the get_short_name method is called on a user with a blank
        short_name and full_name, the user's email is returned
        '''
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        self.assertEqual(user.get_short_name(), user.email)



    '''
    NOTE: Add tests to verify that max length of User fields are correct
    '''

class VehicleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        Create a valid instance of User
        '''
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_invalid_vehicle_without_make(self):
        '''
        An exception is raised when a vehicle with blank 'make' is validated
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        self.assertRaises(ValidationError, lambda: vehicle.full_clean())

    def test_invalid_vehicle_without_model(self):
        '''
        An exception is raised when a vehicle with blank 'model' is validated
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        self.assertRaises(ValidationError, lambda: vehicle.full_clean())

    def test_invalid_vehicle_without_color(self):
        '''
        An exception is raised when a vehicle with blank 'color' is validated
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="", lic_plate_num="123",
            lic_plate_st="WA")
        self.assertRaises(ValidationError, lambda: vehicle.full_clean())

    def test_invalid_vehicle_without_lic_plate_num(self):
        '''
        An exception is raised when a vehicle with blank 'lic_plate_num' is
        validated
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="",
            lic_plate_st="WA")
        self.assertRaises(ValidationError, lambda: vehicle.full_clean())

    def test_invalid_vehicle_without_lic_plate_st(self):
        '''
        An exception is raised when a vehicle with blank 'lic_plate_st' is
        validated
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="")
        self.assertRaises(ValidationError, lambda: vehicle.full_clean())

    def test_valid_vehicle_with_only_required_fields(self):
        '''
        No exception is raised when a vehicle is created with only the
        required fields defined: make, model, color, lic_plate_num,
        lic_plate_st
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        try:
            vehicle.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

    def test_vehicle_invalid_without_owner(self):
        '''
        A ValidationError is raised if an instance of Vehicle without a
        defined owner is validated
        '''
        vehicle = Vehicle(make="Make", model="Model", color="Color",
            lic_plate_num="123", lic_plate_st="WA")
        with self.assertRaises(ValidationError):
            vehicle.full_clean()
            vehicle.save()
        self.assertEqual(Vehicle.objects.all().count(), 0)

    def test_vehicle_string_returns_year_make_model(self):
        '''
        The string method on Vehicle will return
        "year make model" if "year" is defined
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA", year="1999")
        self.assertEqual(str(vehicle), "1999 Make Model")

    def test_vehicle_string_returns_make_model(self):
        '''
        The string method on Vehicle will return
        "make model" if "year" is not defined
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        self.assertEqual(str(vehicle), "Make Model")

    def test_get_owner_method_returns_associated_user(self):
        '''
        The get_owner method will return the user specified via
        ForeignKey
        '''
        vehicle = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        self.assertEqual(vehicle.get_owner(), self.user)

    def test_vehicle_is_deleted_when_owner_is_deleted(self):
        '''
        When a user is deleted fromt the database, all vehicles associated
        with that user are also deleted
        '''
        temp_user = User.objects.create_user(email='temp@email.com',
            password='ValidPassword')
        vehicle = Vehicle.objects.create(owner = temp_user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        self.assertEqual(Vehicle.objects.all().count(), 1)
        temp_user.delete()
        self.assertEqual(Vehicle.objects.all().count(), 0)

    def test_single_user_can_have_multiple_vehicles(self):
        '''
        It is possible for a single user to be associated with multiple
        vehicles
        '''
        v_one = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        v_two = Vehicle.objects.create(owner = self.user, make="Make",
            model="Model", color="Color", lic_plate_num="123",
            lic_plate_st="WA")
        self.assertEqual(Vehicle.objects.filter(owner=self.user).count(), 2)

class EmergencyContactModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        Create a valid instance of User
        '''
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_invalid_emcon_without_full_name(self):
        '''
        An exception is raised when an emcon with blank 'full_name' is
        validated
        '''
        emcon = EmergencyContact.objects.create(user = self.user, full_name="",
            relationship="Cousin's brother's friend")
        self.assertRaises(ValidationError, lambda: emcon.full_clean())

    def test_invalid_emcon_without_relationship(self):
        '''
        An exception is raised when an emcon with blank 'relationship' is
        validated
        '''
        emcon = EmergencyContact.objects.create(user = self.user,
            full_name="Bob Hope", relationship="")
        self.assertRaises(ValidationError, lambda: emcon.full_clean())

    def test_valid_emcon_with_only_required_fields(self):
        '''
        No exception is raised when an emcon is created with only the
        required fields defined: full_name, relationship
        '''
        emcon = EmergencyContact.objects.create(user = self.user,
            full_name="Bob Hope", relationship="Cousin's brother's friend")
        try:
            emcon.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

    def test_emcon_invalid_without_user(self):
        '''
        A ValidationError is raised if an instance of EmergencyContact without
        a defined user is validated
        '''
        emcon = EmergencyContact(full_name="Bob Hope",
            relationship="Cousin's brother's friend")
        with self.assertRaises(ValidationError):
            emcon.full_clean()
            emcon.save()
        self.assertEqual(EmergencyContact.objects.all().count(), 0)

    def test_emcon_string_returns_preferred_name_if_defined(self):
        '''
        The string method on EmergencyContact will return
        "relationship: preferred_name" if preferred_name is defined
        '''
        emcon = EmergencyContact.objects.create(user = self.user,
            full_name="Bob Hope", relationship="Relation",
            preferred_name="BobO")
        self.assertEqual(str(emcon), "Relation: BobO")

    def test_emcon_string_returns_full_name(self):
        '''
        The string method on EmergencyContact will return
        "relationship: full_name" if preferred_name is not defined
        '''
        emcon = EmergencyContact.objects.create(user = self.user,
            full_name="Bob Hope", relationship="Relation",
            preferred_name="")
        self.assertEqual(str(emcon), "Relation: Bob Hope")

    def test_get_user_method_returns_associated_user(self):
        '''
        The get_user method will return the user specified via
        ForeignKey
        '''
        emcon = EmergencyContact.objects.create(user = self.user,
            full_name="Bob Hope", relationship="Cousin's brother's friend")
        self.assertEqual(emcon.get_user(), self.user)

    def test_emcon_is_deleted_when_user_is_deleted(self):
        '''
        When a user is deleted fromt the database, all emcons associated
        with that user are also deleted
        '''
        temp_user = User.objects.create_user(email='temp@email.com',
            password='ValidPassword')
        emcon = EmergencyContact.objects.create(user = temp_user,
            full_name="Bob Hope", relationship="Relation")
        self.assertEqual(EmergencyContact.objects.all().count(), 1)
        temp_user.delete()
        self.assertEqual(EmergencyContact.objects.all().count(), 0)

    def test_single_user_can_have_multiple_emcons(self):
        '''
        It is possible for a single user to be associated with multiple
        emcons
        '''
        e_one = EmergencyContact.objects.create(user = self.user,
            full_name="Bob Hope", relationship="Relation")
        e_two = EmergencyContact.objects.create(user = self.user,
            full_name="Bob Hope", relationship="Relation")
        self.assertEqual(EmergencyContact.objects.filter(
            user=self.user).count(), 2)
