from django.test import TestCase
from django.urls import reverse
from django.test import Client

from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from account_info.models import User, Vehicle, EmergencyContact

class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_404_response_if_user_not_logged_in(self):
        '''
        Request to ProfileView provides a 404 response if no user is logged in
        '''
        response = self.client.get('/account_info/profile/')
        self.assertEqual(response.status_code, 404)

    def test_form_prefilled_with_existing_user_info(self):
        '''
        Request to ProfileView provides a 200 response if user is logged in
        '''
        user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        self.client.login(username='valid@email.com', password='ValidPassword')
        response = self.client.get('/account_info/profile/')
        self.assertEqual(response.status_code, 200)
