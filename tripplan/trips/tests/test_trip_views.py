from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import Http404

from trips.views import TripListView, TripDetailView, TripCreateView
from trips.models import Trip


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

def test_200_response_from_get_request(self):
    request = self.factory.get('/fake/')
    response = TripListView.as_view()(request)
    self.assertEqual(response.status_code, 200)


# class TripListViewTests(TestCase):
#     def test_no_trips(self):
#         """
#         If no trips exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('trips:trip_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "There is no trip information available")
#         self.assertQuerysetEqual(response.context['upcoming_trip_list'], [])
#
#     def test_past_trip(self):
#         """
#         Trips with a start_date in the past are not displayed on the trip_list
#         page
#         """
#         create_trip(title="Past trip", days = -1)
#         response = self.client.get(reverse('trips:trip_list'))
#         self.assertContains(response, "There is no trip information available")
#         self.assertQuerysetEqual(response.context['upcoming_trip_list'], [])
#
#     def test_future_trip(self):
#         """
#         Trips with a start_date today or in the future are displayed on the
#         trip_list page
#         """
#         create_trip(title="Future trip", days = 0)
#         response = self.client.get(reverse('trips:trip_list'))
#         self.assertQuerysetEqual(
#             response.context['upcoming_trip_list'],
#             ['<Trip: Future trip>']
#         )
#
#     def test_future_trip_and_past_trip(self):
#         """
#         When both past and future trips exist, only trips with start_date
#         today or in the future are displayed
#         """
#         create_trip(title="Past trip", days = -1)
#         create_trip(title="Future trip", days = 0)
#         response = self.client.get(reverse('trips:trip_list'))
#         self.assertQuerysetEqual(
#             response.context['upcoming_trip_list'],
#             ['<Trip: Future trip>']
#         )
#
#     def test_two_future_trips(self):
#         """
#         When thre are multiple future trips, both are displayed
#         """
#         create_trip(title="Today trip", days = 0)
#         create_trip(title="Future trip", days = 30)
#         response = self.client.get(reverse('trips:trip_list'))
#         self.assertQuerysetEqual(
#             response.context['upcoming_trip_list'],
#             ['<Trip: Today trip>', '<Trip: Future trip>']
#         )
#
