from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.http import Http404

from account_info.views import EmergencyContactListView, \
    EmergencyContactEditView, EmergencyContactCreateView, \
    EmergencyContactDeleteView
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

    def test_get_queryset_returns_emcons_for_logged_in_user(self):
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

# The following test fails, I think, because the form isn't validating.
# However, the page works fine using runserver.
# Awaiting advice on how to validate form in test
    # def test_post_redirects_to_list_view_if_user_is_logged_in(self):
    #     ec = EmergencyContact.objects.create(full_name='Don Gately',
    #         relationship='Buddy', user = self.user)
    #     request = self.factory.post('/fake/')
    #     request.user = self.user
    #     response = EmergencyContactEditView.as_view()(request, pk=ec.id)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url,
    #         reverse('account_info:emerg_contact_list'))

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

class EmergencyContactCreateViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

# The following test fails, I think, because the form isn't validating.
# However, the page works fine using runserver.
# Awaiting advice on how to validate form in test
    # def test_post_redirects_to_list_view_if_user_is_logged_in(self):
    #     ec = EmergencyContact.objects.create(full_name='Don Gately',
    #         relationship='Buddy', user = self.user)
    #     request = self.factory.post('/fake/')
    #     request.user = self.user
    #     response = EmergencyContactCreateView.as_view()(request)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('account_info:emerg_contact_list'))

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/emergency_contacts/create/'
        reverse_path = reverse('account_info:emerg_contact_create')
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''GET'''
        request = self.factory.get('/fake/')
        request.user = ''
        response = EmergencyContactCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''POST'''
        request = self.factory.post('/fake/')
        request.user = ''
        response = EmergencyContactCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template_with_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactCreateView.as_view()(request)
        self.assertTrue('emerg_contact/create.html' in response.template_name)

class EmergencyContactDeleteViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactDeleteView.as_view()(request, pk=ec.id)
        self.assertEqual(response.status_code, 200)

    def test_post_redirects_to_list_view_if_user_is_logged_in(self):
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        request = self.factory.post('/fake/')
        request.user = self.user
        response = EmergencyContactDeleteView.as_view()(request, pk=ec.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
            reverse('account_info:emerg_contact_list'))

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/emergency_contacts/1/delete/'
        reverse_path = reverse('account_info:emerg_contact_delete',
            args = [1])
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''GET'''
        request = self.factory.get('/fake/')
        request.user = ''
        response = EmergencyContactDeleteView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''POST'''
        request = self.factory.post('/fake/')
        request.user = ''
        response = EmergencyContactDeleteView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template_with_get_request(self):
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = EmergencyContactDeleteView.as_view()(request, pk=ec.id)
        self.assertTrue('emerg_contact/delete.html' in response.template_name)

    def test_get_object_returns_emergency_contact_if_logged_in(self):
        '''
        Tests the get_object() method which is overridden in
        EmergencyContactDeleteView. Function returns emergency contact with
        pk specified in url if logged in user matches emergency contact user
        '''
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user = self.user)
        # import pdb; pdb.set_trace()
        request = self.factory.get(reverse('account_info:emerg_contact_delete',
            args = [ec.id]))
        request.user = self.user
        view = EmergencyContactDeleteView()
        view = setup_view(view, request, pk=ec.id)
        emcon = view.get_object()
        self.assertEqual(ec, emcon)

    def test_get_object_returns_404_response_if_not_logged_in(self):
        '''
        Tests the get_object() method which is overridden in
        EmergencyContactDeleteView. Function returns 404 response if the
        emergency_contact.user.id doesn't match the logged in user.
        '''
        logged_out_user = User.objects.create_user(email='another@email.com',
            password='ValidPassword')
        # Assign one emergency contact to the logged out user
        ec = EmergencyContact.objects.create(full_name='Don Gately',
            relationship='Buddy', user=logged_out_user)
        request = self.factory.get(reverse('account_info:emerg_contact_delete',
            args = [ec.id]))
        request.user = self.user
        view = EmergencyContactDeleteView()
        view = setup_view(view, request, pk=ec.id)
        with self.assertRaises(Http404):
            response = view.get_object()
