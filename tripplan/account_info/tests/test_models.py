from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from account_info.models import User

def create_user(email='', password='', full_name='', preferred_name='',
    primary_phone='', secondary_phone='', street_address_line1='',
    street_address_line2='', city='', state='', zip_code=''):
    """
    Create a user with the given information
    """
    return User.objects.create(email=email, password=password,
        full_name=full_name, preferred_name=preferred_name,
        primary_phone=primary_phone, secondary_phone=secondary_phone,
        street_address_line1=street_address_line1,
        street_address_line2=street_address_line2, city=city, state=state,
        zip_code=zip_code)

class UserModelTests(TestCase):
    def test_invalid_user_without_email(self):
        '''
        An exception is raised when a user with blank email is validated
        '''
        user = User.objects.create(email='', password='ValidPassword')
        self.assertRaises(ValidationError, lambda: user.full_clean())

    def test_invalid_user_without_password(self):
        '''
        An exception is raised when a user with blank password is validated
        '''
        user = User.objects.create(email='valid@email.com', password='')
        self.assertRaises(ValidationError, lambda: user.full_clean())
