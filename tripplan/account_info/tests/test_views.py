from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from account_info.views import ProfileView, EmergencyContactListView, \
    EmergencyContactEditView
from account_info.models import EmergencyContact

User = get_user_model()

def setup_view(view, request, *args, **kwargs):
    '''
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to `reverse()`
    '''
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

class ProfileViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword', full_name='Hugh Steeply')

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/profile/'
        reverse_path = reverse('account_info:account_profile')
        self.assertEqual(reverse_path, url_path)

    def test_post_redirects_to_profile_page_if_user_is_logged_in(self):
        request = self.factory.post('/fake/')
        request.user = self.user
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('account_info:account_profile'))

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''
        A GET request will be redirected to login screen if user accesses
        /account_info/profile/ without being logged in.
        '''
        request = self.factory.get('/fake/')
        request.user = ''
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''
        A POST request will be redirected to login screen if user accesses
        /account_info/profile/ without being logged in.
        '''
        request = self.factory.post('/fake/')
        request.user = ''
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get(reverse('account_info:account_profile'))
        request.user = self.user
        response = ProfileView.as_view()(request)
        self.assertTrue('account_info/profile.html' in response.template_name)

    def test_get_object_returns_logged_in_user(self):
        '''
        Tests the get_object() method which is overridden in ProfileView.
        Function returns currently logged in user
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = ProfileView()
        view = setup_view(view, request)
        obj = view.get_object()
        self.assertEqual(obj, self.user)

class EmergencyContactListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/emergency_contacts/'
        reverse_path = reverse('account_info:emerg_contact_list')
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.get('/fake/')
        request.user = ''
        response = EmergencyContactListView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactListView.as_view()(request)
        self.assertTrue('emerg_contact/list.html' in response.template_name)

    def test_get_queryset_returns_emcons_for_logged_in_userr(self):
        '''
        Tests the get_queryset() method which is overridden in EmergencyContactListView.
        Function returns emergency contacts for currently logged in user only
        '''
        # create a user that will not login
        logged_out_user = User.objects.create_user(email='another@email.com',
            password='ValidPassword')
        # Assign three emergency contacts to the logged in user
        number_of_emerg_contacts = 3
        for i in range(number_of_emerg_contacts):
            EmergencyContact.objects.create(full_name='Michael Pemulis %s' % i,
                relationship='Buddy', user = self.user)
        # And assign one emergency contact to the logged out user
        EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = logged_out_user)
        request = self.factory.get('/fake/')
        request.user = self.user
        view = EmergencyContactListView()
        view = setup_view(view, request)
        # Invoke the get_queryset method for view
        emcons = view.get_queryset()
        # Confirm that it returns three emergency contacts
        self.assertEqual(len(emcons), 3)
        # And check that each emerg contact is associated with logged in user
        for ec in emcons:
            self.assertEqual(ec.user, self.user)

class EmergencyContactEditViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactEditView.as_view()(request, pk=ec.id)
        self.assertEqual(response.status_code, 200)

    # def test_post_redirects_to_list_view_if_user_is_logged_in(self):
    #     ec = EmergencyContact.objects.create(full_name='Don Gately',
    #         relationship='Buddy', user = self.user)
    #     request = self.factory.post('/fake/')
    #     request.user = self.user
    #     response = EmergencyContactEditView.as_view()(request, pk=ec.id)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('account_info:emerg_contact_list'))

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/emergency_contacts/1/edit/'
        reverse_path = reverse('account_info:emerg_contact_edit', args=[1])
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''GET'''
        request = self.factory.get('/fake/')
        request.user = ''
        response = EmergencyContactEditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''POST'''
        request = self.factory.post('/fake/')
        request.user = ''
        response = EmergencyContactEditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template_with_get_request(self):
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactEditView.as_view()(request, pk=ec.id)
        self.assertTrue('emerg_contact/edit.html' in response.template_name)

    def test_view_uses_correct_template_with_post_request(self):
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        request = self.factory.post('/fake/')
        request.user = self.user
        response = EmergencyContactEditView.as_view()(request, pk=ec.id)
        self.assertTrue('emerg_contact/edit.html' in response.template_name)
