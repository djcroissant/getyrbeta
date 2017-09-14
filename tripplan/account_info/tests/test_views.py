from django.test import TestCase
from django.urls import reverse
from django.test import Client

from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from account_info.models import User, EmergencyContact, Vehicle

from account_info.forms import ProfileForm, EmergencyContactForm, VehicleForm

class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        '''
        Create a valid instance of User
        '''
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword', full_name='Bob Hope')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='valid@email.com', password='ValidPassword')
        response = self.client.get('/account_info/profile/')
        # check that 200 response is given
        self.assertEqual(response.status_code, 200)
        # check that url name reverses correctly
        self.assertEqual(reverse('account_info:account_profile'),
            '/account_info/profile/')
        # check that response includes context for logged in user
        self.assertEqual(response.context['user'].email, 'valid@email.com')

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''
        A GET request will be redirected to login screen if user accesses
        /account_info/profile/ without being logged in. The re-direct will
        include next = profile.
        '''
        response = self.client.get(reverse('account_info:account_profile'))
        redirect_url = reverse('authentication:signin') + '?next=' + \
            reverse('account_info:account_profile')
        self.assertRedirects(response, redirect_url, status_code=302,
            target_status_code=200)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''
        A POST request will be redirected to login screen if user accesses
        /account_info/profile/ without being logged in. The re-direct will
        include next = profile.
        '''
        response = self.client.post(reverse('account_info:account_profile'))
        redirect_url = reverse('authentication:signin') + '?next=' + \
            reverse('account_info:account_profile')
        self.assertRedirects(response, redirect_url, status_code=302,
            target_status_code=200)

    def test_view_uses_correct_template(self):
        self.client.login(username='valid@email.com', password='ValidPassword')
        response = self.client.get(reverse('account_info:account_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_info/profile.html')

    def test_form_prefilled_with_existing_user_info(self):
        '''
        When user is logged in, the profile page will be pre-filled with the
        information that already exists in the db for that user
        '''
        self.client.login(username='valid@email.com', password='ValidPassword')
        response = self.client.get(reverse('account_info:account_profile'))
        self.assertEqual(response.context['form'].initial['full_name'],
            'Bob Hope')
        self.assertEqual(response.context['form'].initial['preferred_name'], '')

    def test_post_will_update_user_and_stay_on_profile_page(self):
        '''
        When the user updates profile info and saves, the database will be
        updated and the profile page will be refreshed and the form with
        updated info will be displayed
        '''
        self.client.login(username='valid@email.com', password='ValidPassword')
        preferred_name = 'Hope springs eternal'
         #pass the new 'preferred_name' to the post request
        response = self.client.post(reverse('account_info:account_profile'), \
            {'preferred_name':preferred_name})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_info:account_profile'))
        # fetch the logged in user from the database
        updated_user=User.objects.get(email='valid@email.com')
        # confirm the new preferred_name is set correctly
        self.assertEqual(updated_user.preferred_name, 'Hope springs eternal')
        # ensure the form is displaying the new data after a new get request
        response = self.client.get(reverse('account_info:account_profile'))
        self.assertEqual(response.context['form'].initial['preferred_name'],
            'Hope springs eternal')

class EmergencyContactListViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        '''
        Create a valid instance of User
        '''
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword', full_name='Bob Hope')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='valid@email.com', password='ValidPassword')
        response = self.client.get('/account_info/emergency_contacts/')
        # check that 200 response is given
        self.assertEqual(response.status_code, 200)
        # check that url name reverses correctly
        self.assertEqual(reverse('account_info:emerg_contact_list'),
            '/account_info/emergency_contacts/')
        # check that response includes context for logged in user
        self.assertEqual(response.context['user'].email, 'valid@email.com')

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''
        A GET request will be redirected to login screen if user accesses
        /account_info/emergency_contacts/ without being logged in. The
        re-direct will pass next = emergency_contacts.
        '''
        response = self.client.get(reverse('account_info:emerg_contact_list'))
        redirect_url = reverse('authentication:signin') + '?next=' + \
            reverse('account_info:emerg_contact_list')
        self.assertRedirects(response, redirect_url, status_code=302,
            target_status_code=200)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''
        A POST request will be redirected to login screen if user accesses
        /account_info/emergency_contacts/ without being logged in. The
        re-direct will pass next = emergency_contacts.
        '''
        response = self.client.post(reverse('account_info:emerg_contact_list'))
        redirect_url = reverse('authentication:signin') + '?next=' + \
            reverse('account_info:emerg_contact_list')
        self.assertRedirects(response, redirect_url, status_code=302,
            target_status_code=200)

    def test_view_uses_correct_template(self):
        self.client.login(username='valid@email.com', password='ValidPassword')
        response = self.client.get(reverse('account_info:emerg_contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'emerg_contact/list.html')

    def test_lists_all_emerg_contacts_for_logged_in_user(self):
        # create another user
        logged_out_user = User.objects.create_user(email='another@email.com',
            password='ValidPassword', full_name='Logged Out User')
        # login user created in setup
        self.client.login(username='valid@email.com', password='ValidPassword')
        # Create 3 emergency contacts
        number_of_emerg_contacts = 3
        for i in range(number_of_emerg_contacts):
            EmergencyContact.objects.create(full_name='Michael Pemulis %s' % i,
                relationship='Buddy', user = self.user)
        # Create 1 more emergency contact assigned to logged out user
        EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = logged_out_user)
        # send get request to emergecny contact list url
        response = self.client.get(reverse('account_info:emerg_contact_list'))
        # response context has emergency contacts for logged in user only
        self.assertEqual(len(response.context['emergencycontact_list']), 3)
        # check that each emerg contact is associated with logged in user
        for emerg_contact in response.context['emergencycontact_list']:
            self.assertEqual(response.context['user'], emerg_contact.user)


    '''
    Additional tests required:
    -all emergency contacts are listed
    -if there is only one, it is shown as primary
    -if there is more than one, the correct one is shown as primary
    '''

    # def test_form_prefilled_with_existing_user_info(self):
    #     '''
    #     When user is logged in, the profile page will be pre-filled with the
    #     information that already exists in the db for that user
    #     '''
    #     self.client.login(username='valid@email.com', password='ValidPassword')
    #     response = self.client.get(reverse('account_info:account_profile'))
    #     self.assertEqual(response.context['form'].initial['full_name'],
    #         'Bob Hope')
    #     self.assertEqual(response.context['form'].initial['preferred_name'], '')

    # def test_post_will_update_user_and_stay_on_profile_page(self):
    #     '''
    #     When the user updates profile info and saves, the database will be
    #     updated and the profile page will be refreshed and the form with
    #     updated info will be displayed
    #     '''
    #     self.client.login(username='valid@email.com', password='ValidPassword')
    #     preferred_name = 'Hope springs eternal'
    #      #pass the new 'preferred_name' to the post request
    #     response = self.client.post(reverse('account_info:account_profile'), \
    #         {'preferred_name':preferred_name})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('account_info:account_profile'))
    #     # fetch the logged in user from the database
    #     updated_user=User.objects.get(email='valid@email.com')
    #     # confirm the new preferred_name is set correctly
    #     self.assertEqual(updated_user.preferred_name, 'Hope springs eternal')
    #     # ensure the form is displaying the new data after a new get request
    #     response = self.client.get(reverse('account_info:account_profile'))
    #     self.assertEqual(response.context['form'].initial['preferred_name'],
    #         'Hope springs eternal')
