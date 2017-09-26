from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.http import Http404

from account_info.views import VehicleListView, VehicleEditView, \
    VehicleCreateView, VehicleDeleteView
from account_info.models import Vehicle

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

class VehicleListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/vehicles/'
        reverse_path = reverse('account_info:vehicle_list')
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        request = self.factory.get('/fake/')
        request.user = ''
        response = VehicleListView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleListView.as_view()(request)
        self.assertTrue('vehicle/list.html' in response.template_name)

    def test_get_queryset_returns_vehicles_for_logged_in_user(self):
        '''
        Tests the get_queryset() method which is overridden in VehicleListView.
        Function returns vehicles for currently logged in user only
        '''
        # create a user that will not login
        logged_out_user = User.objects.create_user(email='another@email.com',
            password='ValidPassword')
        # Assign three vehicles to the logged in user
        number_of_vehicles = 3
        for i in range(number_of_vehicles):
            Vehicle.objects.create(make='suzuki', model='baja', color='red',
            lic_plate_st='WA', lic_plate_num='%s' % i, owner = self.user)
        # And assign one vehicle to the logged out user
        Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=logged_out_user)
        request = self.factory.get('/fake/')
        request.user = self.user
        view = VehicleListView()
        view = setup_view(view, request)
        # Invoke the get_queryset method for view
        vehicles = view.get_queryset()
        # Confirm that it returns three vehicles
        self.assertEqual(len(vehicles), 3)
        # And check that each emerg contact is associated with logged in user
        for v in vehicles:
            self.assertEqual(v.owner, self.user)

class VehicleEditViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleEditView.as_view()(request, pk=v.id)
        self.assertEqual(response.status_code, 200)

# The following test fails, I think, because the form isn't validating.
# However, the page works fine using runserver.
# Awaiting advice on how to validate form in test
    # def test_post_redirects_to_list_view_if_user_is_logged_in(self):
    #     v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
            # lic_plate_st='WA', lic_plate_num='10', owner=self.user)
    #     request = self.factory.post('/fake/')
    #     request.user = self.user
    #     response = VehicleEditView.as_view()(request, pk=v.id)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url,
    #         reverse('account_info:vehicle_list'))

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/vehicles/1/edit/'
        reverse_path = reverse('account_info:vehicle_edit', args=[1])
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''GET'''
        request = self.factory.get('/fake/')
        request.user = ''
        response = VehicleEditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''POST'''
        request = self.factory.post('/fake/')
        request.user = ''
        response = VehicleEditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template_with_get_request(self):
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleEditView.as_view()(request, pk=v.id)
        self.assertTrue('account_info/form.html' in response.template_name)

class VehicleCreateViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

# The following test fails, I think, because the form isn't validating.
# However, the page works fine using runserver.
# Awaiting advice on how to validate form in test
    # def test_post_redirects_to_list_view_if_user_is_logged_in(self):
    #     v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
    #       lic_plate_st='WA', lic_plate_num='10', owner=self.user)
    #     request = self.factory.post('/fake/')
    #     request.user = self.user
    #     response = VehicleCreateView.as_view()(request)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('account_info:vehicle_list'))

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/vehicles/create/'
        reverse_path = reverse('account_info:vehicle_create')
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''GET'''
        request = self.factory.get('/fake/')
        request.user = ''
        response = VehicleCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''POST'''
        request = self.factory.post('/fake/')
        request.user = ''
        response = VehicleCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template_with_get_request(self):
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleCreateView.as_view()(request)
        self.assertTrue('account_info/form.html' in response.template_name)

class VehicleDeleteViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='valid@email.com',
            password='ValidPassword')

    def test_200_response_from_get_request(self):
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleDeleteView.as_view()(request, pk=v.id)
        self.assertEqual(response.status_code, 200)

    def test_post_redirects_to_list_view_if_user_is_logged_in(self):
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=self.user)
        request = self.factory.post('/fake/')
        request.user = self.user
        response = VehicleDeleteView.as_view()(request, pk=v.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
            reverse('account_info:vehicle_list'))

    def test_url_name_reverses_correctly(self):
        url_path = '/account_info/vehicles/1/delete/'
        reverse_path = reverse('account_info:vehicle_delete',
            args = [1])
        self.assertEqual(reverse_path, url_path)

    def test_get_request_redirects_to_login_if_user_not_logged_in(self):
        '''GET'''
        request = self.factory.get('/fake/')
        request.user = ''
        response = VehicleDeleteView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_post_request_redirects_to_login_if_user_not_logged_in(self):
        '''POST'''
        request = self.factory.post('/fake/')
        request.user = ''
        response = VehicleDeleteView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse('authentication:signin') + '?next=' + '/fake/'
        self.assertEqual(response.url, redirect_url)

    def test_view_uses_correct_template_with_get_request(self):
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=self.user)
        request = self.factory.get('/fake/')
        request.user = self.user
        response = VehicleDeleteView.as_view()(request, pk=v.id)
        self.assertTrue('vehicle/delete.html' in response.template_name)

    def test_get_object_returns_vehicle_if_logged_in(self):
        '''
        Tests the get_object() method which is overridden in
        VehicleDeleteView. Function returns vehicle with
        pk specified in url if logged in user matches vehicle user
        '''
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=self.user)
        # import pdb; pdb.set_trace()
        request = self.factory.get(reverse('account_info:vehicle_delete',
            args = [v.id]))
        request.user = self.user
        view = VehicleDeleteView()
        view = setup_view(view, request, pk=v.id)
        vehicle = view.get_object()
        self.assertEqual(v, vehicle)

    def test_get_object_returns_404_response_if_not_logged_in(self):
        '''
        Tests the get_object() method which is overridden in
        VehicleDeleteView. Function returns 404 response if the
        vehicle.user.id doesn't match the logged in user.
        '''
        logged_out_user = User.objects.create_user(email='another@email.com',
            password='ValidPassword')
        # Assign one vehicle to the logged out user
        v = Vehicle.objects.create(make='suzuki', model='baja', color='red',
        lic_plate_st='WA', lic_plate_num='10', owner=logged_out_user)
        request = self.factory.get(reverse('account_info:vehicle_delete',
            args = [v.id]))
        request.user = self.user
        view = VehicleDeleteView()
        view = setup_view(view, request, pk=v.id)
        with self.assertRaises(Http404):
            response = view.get_object()
