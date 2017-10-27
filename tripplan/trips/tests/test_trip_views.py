import datetime

from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import Http404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.generic import DetailView

from trips.views import TripListView, TripDetailView, TripCreateView
from trips.models import Trip, TripMember


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


class TripListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = TripListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/trips/'
        reverse_path = reverse('trips:trip_list')
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.get('/fake/')
        request.user = ''
        response = TripListView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = TripListView.as_view()(request)
        self.assertTrue('trips/index.html' in response.template_name)

    def test_no_trips(self):
        """
        If no trips exist, an appropriate message is displayed.
        """
        request = self.factory.get('/fake/')
        request.user = self.user
        response = TripListView.as_view()(request)
        self.assertContains(response, "You don't have any upcoming trips planned")
        self.assertContains(response, "You haven't completed any trips yet")

    def test_get_queryset_returns_trips_for_logged_in_user(self):
        '''
        Tests the get_queryset() method which is overridden in TripListView.
        Function returns only trips for which the currently logged in user
        is a member (and has accepted membership).
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripListView()
        kwargs={}
        view = setup_view(view, request, **kwargs)
        trip = Trip.objects.create(
            title='title',
            start_date=timezone.now().date()
        )
        trip_nonmember = Trip.objects.create(
            title='title',
            start_date=timezone.now().date()
        )
        TripMember.objects.create(
            member=self.user,
            trip=trip,
            email="fake@fake.fake"
        )
        queryset = view.get_queryset()
        self.assertEqual(list(self.user.trip_set.all()), list(queryset))

    def test_get_context_data_returns_upcoming_trips(self):
        '''
        The get_context_data returns an 'upcoming_trip_list', including
        only trips for which the logged in user is a member
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripListView()
        kwargs={}
        view = setup_view(view, request, **kwargs)
        trip_past = Trip.objects.create(
            title='title',
            start_date=timezone.now().date() + datetime.timedelta(days=-1)
        )
        trip_future = Trip.objects.create(
            title='title',
            start_date=timezone.now().date() + datetime.timedelta(days=1)
        )
        TripMember.objects.create(
            member=self.user,
            trip=trip_past,
            email="fake@fake.fake"
        )
        TripMember.objects.create(
            member=self.user,
            trip=trip_future,
            email="fake@fake.fake"
        )
        view.object_list = self.user.trip_set.all()
        context = view.get_context_data()
        self.assertEqual(
            list(view.object_list.filter(start_date__gte=timezone.now())),
            list(context['upcoming_trip_list'])
        )

    def test_get_context_data_returns_past_trips(self):
        '''
        The get_context_data returns an 'past_trip_list', including
        only trips for which the logged in user is a member
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripListView()
        kwargs={}
        view = setup_view(view, request, **kwargs)
        trip_past = Trip.objects.create(
            title='title',
            start_date=timezone.now().date() + datetime.timedelta(days=-1)
        )
        trip_future = Trip.objects.create(
            title='title',
            start_date=timezone.now().date() + datetime.timedelta(days=1)
        )
        TripMember.objects.create(
            member=self.user,
            trip=trip_past,
            email="fake@fake.fake"
        )
        TripMember.objects.create(
            member=self.user,
            trip=trip_future,
            email="fake@fake.fake"
        )
        view.object_list = self.user.trip_set.all()
        context = view.get_context_data()
        self.assertEqual(
            list(view.object_list.filter(start_date__lt=timezone.now())),
            list(context['past_trip_list'])
        )


class TripDetailViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')
        cls.trip = Trip.objects.create(title='title',
            start_date=timezone.now().date())

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = TripDetailView.as_view()(request, pk=self.trip.id)
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/trips/1/'
        reverse_path = reverse('trips:trip_detail', args=[1])
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.get('/fake/')
        request.user = ''
        response = TripDetailView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = TripDetailView.as_view()(request, pk=self.trip.id)
        self.assertTrue('trips/detail.html' in response.template_name)

    def test_get_context_data_includes_key_page_title(self):
        '''
        The get_context_data includes key 'page_title'
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripDetailView()
        kwargs={'pk': self.trip.id}
        view = setup_view(view, request, **kwargs)
        view.object = self.trip
        context = view.get_context_data()
        self.assertIn('page_title', context)

    def test_get_context_data_includes_end_date_multi_night(self):
        '''
        The get_context_data includes a key 'end_date' if the trip has
        number_nights > 0
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripDetailView()
        kwargs={'pk': self.trip.id}
        self.trip.number_nights = 1
        self.trip.save()
        view = setup_view(view, request, **kwargs)
        view.object = self.trip
        context = view.get_context_data()
        self.assertIn('end_date', context)

    def test_get_context_data_returns_end_date_zero_night(self):
        '''
        The get_context_data does not return 'end_date' if the trip has
        number_nights==0
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripDetailView()
        kwargs={'pk': self.trip.id}
        view = setup_view(view, request, **kwargs)
        view.object = self.trip
        context = view.get_context_data()
        self.assertNotIn('end_date', context)

    def test_get_context_data_includes_key_trailhead(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripDetailView()
        kwargs={'pk': self.trip.id}
        view = setup_view(view, request, **kwargs)
        view.object = self.trip
        context = view.get_context_data()
        self.assertIn('trailhead', context)

    def test_get_context_data_includes_key_endpoint(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripDetailView()
        kwargs={'pk': self.trip.id}
        view = setup_view(view, request, **kwargs)
        view.object = self.trip
        context = view.get_context_data()
        self.assertIn('endpoint', context)

    def test_get_context_data_includes_key_objective_dict(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripDetailView()
        kwargs={'pk': self.trip.id}
        view = setup_view(view, request, **kwargs)
        view.object = self.trip
        context = view.get_context_data()
        self.assertIn('objective_dict', context)

    def test_get_context_data_includes_key_camp_dict(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripDetailView()
        kwargs={'pk': self.trip.id}
        view = setup_view(view, request, **kwargs)
        view.object = self.trip
        context = view.get_context_data()
        self.assertIn('camp_dict', context)


class TripCreateViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = TripCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/trips/create/'
        reverse_path = reverse('trips:trip_create')
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.get('/fake/')
        request.user = ''
        response = TripCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.post('/fake/')
        request.user = ''
        response = TripCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = TripCreateView.as_view()(request)
        self.assertTrue('trips/create.html' in response.template_name)

    def test_get_context_data_includes_key_page_title(self):
        '''
        The get_context_data includes key 'page_title'
        '''
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripCreateView()
        kwargs={}
        view = setup_view(view, request, **kwargs)
        view.object = Trip()
        context = view.get_context_data()
        self.assertIn('page_title', context)

    def test_get_context_data_includes_key_submit_button_title(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripCreateView()
        kwargs={}
        view = setup_view(view, request, **kwargs)
        view.object = Trip()
        context = view.get_context_data()
        self.assertIn('submit_button_title', context)

    def test_get_context_data_includes_key_cancel_button_path(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripCreateView()
        kwargs={}
        view = setup_view(view, request, **kwargs)
        view.object = Trip()
        context = view.get_context_data()
        self.assertIn('cancel_button_path', context)

    def test_get_success_url_redirects_to_trip_detail(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        view = TripCreateView()
        kwargs={}
        view = setup_view(view, request, **kwargs)
        trip = Trip.objects.create(title='title',
            start_date=timezone.now().date())
        view.object = trip
        success_url = view.get_success_url()
        intended_url = reverse('trips:trip_detail', args=(trip.id,))
        self.assertEqual(success_url, intended_url)
