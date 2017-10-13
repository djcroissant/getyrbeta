import datetime

from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import Http404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.generic import DetailView

from trips.views import LocationCreateView, LocationEditView, \
    LocationDeleteView
from trips.models import Trip, TripLocation


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

class LocationCreateViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        cls.trip = Trip.objects.create(title='title',
            start_date=timezone.now().date(), number_nights=2)

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = LocationCreateView.as_view()(request, trip_id=1,
            location_type='trailhead')
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/trips/1/create/location_type/'
        reverse_path = reverse('trips:location_create', args=(1, 'location_type'))
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.get('/fake/')
        request.user = ''
        response = LocationCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.post('/fake/')
        request.user = ''
        response = LocationCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = LocationCreateView.as_view()(request, trip_id=1,
            location_type='trailhead')
        self.assertTrue('trips/location.html' in response.template_name)

    def test_view_sets_instance_variables_through_get_request(self):
        """
        When a get request is sent, the view will set instance variables
        to be used later in the context
        """
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'trailhead'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        self.assertIsNotNone(view.location_type)
        self.assertIsNotNone(view.page_title)
        self.assertIsNotNone(view.submit_button_title)

    def test_view_sets_instance_variables_through_post_request(self):
        """
        When a post request is sent, the view will set instance variables
        to be used later in the context
        """
        request = self.factory.post('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'trailhead'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        self.assertIsNotNone(view.location_type)
        self.assertIsNotNone(view.page_title)
        self.assertIsNotNone(view.submit_button_title)

    def test_value_of_instance_variables_set_through_get_trailhead(self):
        """
        When a get request is sent with location_type=trailhead in the url,
        the view will set instance variables
        """
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'trailhead'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        self.assertEqual(view.location_type, TripLocation.BEGIN)
        self.assertEqual(view.page_title, 'Enter a new trailhead location')
        self.assertEqual(view.submit_button_title, 'Save Trailhead')

    def test_value_of_instance_variables_set_through_get_endpoint(self):
        """
        When a get request is sent with location_type=endpoint in the url,
        the view will set instance variables
        """
        # FUTURE FUNCTIONALITY
        pass

    def test_value_of_instance_variables_set_through_get_objective(self):
        """
        When a get request is sent with location_type=objective in the url,
        the view will set instance variables
        """
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'objective'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        self.assertEqual(view.location_type, TripLocation.OBJECTIVE)
        self.assertEqual(view.page_title, 'Enter a new objective')
        self.assertEqual(view.submit_button_title, 'Save Objective')

    def test_value_of_instance_variables_set_through_get_camp(self):
        """
        When a get request is sent with location_type=camp in the url,
        the view will set instance variables
        """
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        self.assertEqual(view.location_type, TripLocation.CAMP)
        self.assertEqual(view.page_title, 'Enter a new camp location')
        self.assertEqual(view.submit_button_title, 'Save Camp')

    def test_get_request_raises_exception_with_invalid_location_type(self):
        """
        When a get request is sent with an invalid location_type, a
        ValueError will be raised
        """
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'invalid'}
        view = setup_view(view, request, **kwargs)
        test = lambda: view.get(request, **kwargs)
        self.assertRaises(ValueError, test)

    def test_get_context_data_includes_key_page_title(self):
        '''
        The get_context_data includes key 'page_title'
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        context = view.get_context_data()
        self.assertIn('page_title', context)

    def test_get_context_data_includes_key_submit_button_title(self):
        '''
        The get_context_data includes key 'submit_button_title'
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        context = view.get_context_data()
        self.assertIn('submit_button_title', context)

    def test_get_context_data_includes_key_cancel_button_path(self):
        '''
        The get_context_data includes key 'cancel_button_path'
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        context = view.get_context_data()
        self.assertIn('cancel_button_path', context)

    def test_get_context_data_includes_key_trip_id(self):
        '''
        The get_context_data includes key 'trip_id'
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        context = view.get_context_data()
        self.assertIn('trip_id', context)

    def test_get_form_kwargs_returns_tuple_of_choices(self):
        '''
        The get_form_kwargs method will add key 'choices' to the
        form kwargs with value set to a tuple of tuples
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        date_list = self.trip.get_date_choices()
        choices = []
        for item in date_list:
            choices.append((item, item))
        choices_tuple = tuple(choices)
        form_kwargs = view.get_form_kwargs()
        self.assertIn('choices', form_kwargs)
        self.assertEqual(form_kwargs['choices'], choices_tuple)

    def test_get_success_url_redirects_to_trip_detail(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationCreateView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
        view = setup_view(view, request, **kwargs)
        success_url = view.get_success_url()
        intended_url = reverse('trips:trip_detail', args=(self.trip.id,))
        self.assertEqual(success_url, intended_url)

class LocationEditViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        cls.trip = Trip.objects.create(title='title',
            start_date=timezone.now().date(), number_nights=2)
        cls.triplocation = TripLocation.objects.create(
            location_type=TripLocation.CAMP, trip=cls.trip)

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = LocationEditView.as_view()(request, trip_id=self.trip.id,
            location_type='camp', pk=self.triplocation.id)
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/trips/1/edit/location_type/2'
        reverse_path = reverse('trips:location_create', args=(
            1, 'location_type', 2))
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.get('/fake/')
        request.user = ''
        response = LocationEditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.post('/fake/')
        request.user = ''
        response = LocationEditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = LocationEditView.as_view()(request, trip_id=1,
            location_type='trailhead', pk=1)
        self.assertTrue('trips/location.html' in response.template_name)

    def test_view_sets_instance_variables_through_get_request(self):
        """
        When a get request is sent, the view will set instance variables
        to be used later in the context
        """
        request = self.factory.get('/fake/')
        request.user = self.user
        view = LocationEditView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'trailhead',
            'pk': self.triplocation.id}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        self.assertIsNotNone(view.location_type)
        self.assertIsNotNone(view.page_title)
        self.assertIsNotNone(view.submit_button_title)

    def test_view_sets_instance_variables_through_post_request(self):
        """
        When a post request is sent, the view will set instance variables
        to be used later in the context
        """
        request = self.factory.post('/fake/')
        request.user = self.user
        view = LocationEditView()
        kwargs={'trip_id': self.trip.id, 'location_type': 'trailhead',
            'pk': self.triplocation.id}
        view = setup_view(view, request, **kwargs)
        view.get(request, **kwargs)
        self.assertIsNotNone(view.location_type)
        self.assertIsNotNone(view.page_title)
        self.assertIsNotNone(view.submit_button_title)

    # def test_value_of_instance_variables_set_through_get_trailhead(self):
    #     """
    #     When a get request is sent with location_type=trailhead in the url,
    #     the view will set instance variables
    #     """
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'trailhead'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     self.assertEqual(view.location_type, TripLocation.BEGIN)
    #     self.assertEqual(view.page_title, 'Enter a new trailhead location')
    #     self.assertEqual(view.submit_button_title, 'Save Trailhead')
    #
    # def test_value_of_instance_variables_set_through_get_endpoint(self):
    #     """
    #     When a get request is sent with location_type=endpoint in the url,
    #     the view will set instance variables
    #     """
    #     # FUTURE FUNCTIONALITY
    #     pass
    #
    # def test_value_of_instance_variables_set_through_get_objective(self):
    #     """
    #     When a get request is sent with location_type=objective in the url,
    #     the view will set instance variables
    #     """
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'objective'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     self.assertEqual(view.location_type, TripLocation.OBJECTIVE)
    #     self.assertEqual(view.page_title, 'Enter a new objective')
    #     self.assertEqual(view.submit_button_title, 'Save Objective')
    #
    # def test_value_of_instance_variables_set_through_get_camp(self):
    #     """
    #     When a get request is sent with location_type=camp in the url,
    #     the view will set instance variables
    #     """
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     self.assertEqual(view.location_type, TripLocation.CAMP)
    #     self.assertEqual(view.page_title, 'Enter a new camp location')
    #     self.assertEqual(view.submit_button_title, 'Save Camp')
    #
    # def test_get_request_raises_exception_with_invalid_location_type(self):
    #     """
    #     When a get request is sent with an invalid location_type, a
    #     ValueError will be raised
    #     """
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'invalid'}
    #     view = setup_view(view, request, **kwargs)
    #     test = lambda: view.get(request, **kwargs)
    #     self.assertRaises(ValueError, test)
    #
    # def test_get_context_data_includes_key_page_title(self):
    #     '''
    #     The get_context_data includes key 'page_title'
    #     '''
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     context = view.get_context_data()
    #     self.assertIn('page_title', context)
    #
    # def test_get_context_data_includes_key_submit_button_title(self):
    #     '''
    #     The get_context_data includes key 'submit_button_title'
    #     '''
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     context = view.get_context_data()
    #     self.assertIn('submit_button_title', context)
    #
    # def test_get_context_data_includes_key_cancel_button_path(self):
    #     '''
    #     The get_context_data includes key 'cancel_button_path'
    #     '''
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     context = view.get_context_data()
    #     self.assertIn('cancel_button_path', context)
    #
    # def test_get_context_data_includes_key_trip_id(self):
    #     '''
    #     The get_context_data includes key 'trip_id'
    #     '''
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     context = view.get_context_data()
    #     self.assertIn('trip_id', context)
    #
    # def test_get_form_kwargs_returns_tuple_of_choices(self):
    #     '''
    #     The get_form_kwargs method will add key 'choices' to the
    #     form kwargs with value set to a tuple of tuples
    #     '''
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
    #     view = setup_view(view, request, **kwargs)
    #     view.get(request, **kwargs)
    #     date_list = self.trip.get_date_choices()
    #     choices = []
    #     for item in date_list:
    #         choices.append((item, item))
    #     choices_tuple = tuple(choices)
    #     form_kwargs = view.get_form_kwargs()
    #     self.assertIn('choices', form_kwargs)
    #     self.assertEqual(form_kwargs['choices'], choices_tuple)
    #
    # def test_get_success_url_redirects_to_trip_detail(self):
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = LocationEditView()
    #     kwargs={'trip_id': self.trip.id, 'location_type': 'camp'}
    #     view = setup_view(view, request, **kwargs)
    #     success_url = view.get_success_url()
    #     intended_url = reverse('trips:trip_detail', args=(self.trip.id,))
    #     self.assertEqual(success_url, intended_url)
