from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage


from account_info.views import ProfileView

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

        # Django bug with messages. Work around provided here:
        # https://stackoverflow.com/questions/11938164/why-dont-my-django-unittests-know-that-messagemiddleware-is-installed
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

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
        redirect_url = reverse('authentication:login') + '?next=' + '/fake/'
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
        redirect_url = reverse('authentication:login') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get(reverse('account_info:account_profile'))
        request.user = self.user
        response = ProfileView.as_view()(request)
        self.assertTrue('account_info/form.html' in response.template_name)

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
