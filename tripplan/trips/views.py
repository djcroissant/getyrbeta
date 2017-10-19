import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, ListView, \
    CreateView, DeleteView, DetailView, FormView
from django.utils import timezone
from django.contrib.auth import authenticate

from .models import Trip, TripLocation, TripMember

from account_info.models import User

from .forms import TripForm, LocationForm, SearchForm


class LoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(LoginRequiredMixin, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(LoginRequiredMixin, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)


class LocationGeneralMixin:
    """
    This mixin is used by all views for the Location model.
    """
    model = TripLocation

    # set_instance_variables() is a callable located in the primary class
    # description. The output is used by get_context_data()
    def get(self, request, *args, **kwargs):
        self.set_instance_variables(**kwargs)
        return super(LocationGeneralMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_instance_variables(**kwargs)
        return super(LocationGeneralMixin, self).post(request, *args, **kwargs)

    # The context data is used by the template
    def get_context_data(self, **kwargs):
        context = super(LocationGeneralMixin, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['submit_button_title'] = self.submit_button_title
        context['cancel_button_path'] = 'trips:trip_detail'
        context['trip_id'] = self.kwargs.get('trip_id')
        return context

    def get_success_url(self):
        return reverse('trips:trip_detail', args=(self.kwargs.get('trip_id'),))

class LocationFormMixin:
    """
    This mixin is used by all views for the Location model that include a
    form.
    """
    model = TripLocation
    template_name = 'trips/location.html'
    form_class = LocationForm

    def get_form_kwargs(self):
        """
        Adds a tuple of choices for the date field to the form kwargs.
        """
        kwargs = super(LocationFormMixin, self).get_form_kwargs()
        date_list = Trip.objects.get(pk=self.kwargs.get(
            'trip_id')).get_date_choices()
        choices = []
        for item in date_list:
            choices.append((item, item))
        kwargs['choices'] = tuple(choices)
        return kwargs

class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/index.html'

    def get_context_data(self, **kwargs):
        context = super(TripListView, self).get_context_data(**kwargs)
        context['upcoming_trip_list'] = Trip.objects.filter(
            start_date__gte=timezone.now()).order_by('start_date')
        context['past_trip_list'] = Trip.objects.filter(
            start_date__lt=timezone.now()).order_by('start_date')
        return context

class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TripDetailView, self).get_context_data(**kwargs)
        trip = self.get_object()
        context['page_title'] = trip.title
        if trip.number_nights > 0:
            context['end_date'] = trip.start_date + datetime.timedelta(
                days=trip.number_nights)

        context['trailhead'] = trip.get_trailhead()
        context['endpoint'] = trip.get_endpoint()

        context['objective_dict'] = trip.get_location_context(
            TripLocation.OBJECTIVE)
        context['camp_dict'] = trip.get_location_context(TripLocation.CAMP)
        return context

class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    template_name = 'trips/create.html'
    form_class = TripForm

    def get_context_data(self, **kwargs):
        context = super(TripCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Start a new trip'
        context['submit_button_title'] = 'Save Trip'
        context['cancel_button_path'] = 'trips:trip_list'
        return context

    def get_success_url(self):
        return reverse('trips:trip_detail', args=(self.object.id,))

class LocationCreateView(LoginRequiredMixin, LocationGeneralMixin,
    LocationFormMixin, CreateView):
    model = TripLocation
    def set_instance_variables(self, **kwargs):
        url_location_type = self.kwargs.get('location_type')
        if url_location_type == 'trailhead':
            self.kwargs['location_type'] = TripLocation.BEGIN
            self.page_title = 'Enter a new trailhead location'
            self.submit_button_title = 'Save Trailhead'
        elif url_location_type == 'objective':
            self.kwargs['location_type'] = TripLocation.OBJECTIVE
            self.page_title = 'Enter a new objective'
            self.submit_button_title = 'Save Objective'
        elif url_location_type == 'camp':
            self.kwargs['location_type'] = TripLocation.CAMP
            self.page_title = 'Enter a new camp location'
            self.submit_button_title = 'Save Camp'
        else:
            raise ValueError('Invalid location type: ' + url_location_type)

    def get_initial(self):
        trip = get_object_or_404(Trip, pk=self.kwargs.get('trip_id'))
        location_type = self.kwargs.get('location_type')
        return {
            'trip': trip,
            'location_type': location_type
        }

class LocationEditView(LoginRequiredMixin, LocationGeneralMixin,
    LocationFormMixin, UpdateView):
    def set_instance_variables(self, **kwargs):
        url_location_type = self.kwargs.get('location_type')
        if url_location_type == 'trailhead':
            self.page_title = 'Edit trailhead details'
            self.submit_button_title = 'Save Trailhead'
        elif url_location_type == 'objective':
            self.page_title = 'Edit objective details'
            self.submit_button_title = 'Save Objective'
        elif url_location_type == 'camp':
            self.page_title = 'Edit camp details'
            self.submit_button_title = 'Save Camp'
        else:
            raise ValueError('Invalid location type: ' + url_location_type)

class LocationDeleteView(LoginRequiredMixin, LocationGeneralMixin, DeleteView):
    template_name = 'trips/delete.html'
    context_object_name = 'triplocation'

    def set_instance_variables(self, **kwargs):
        url_location_type = self.kwargs.get('location_type')
        if url_location_type == 'trailhead':
            self.page_title = 'Delete trailhead'
            self.submit_button_title = 'Delete Trailhead'
        elif url_location_type == 'objective':
            self.page_title = 'Delete objective'
            self.submit_button_title = 'Delete Objective'
        elif url_location_type == 'camp':
            self.page_title = 'Delete camp'
            self.submit_button_title = 'Delete Camp'
        else:
            raise ValueError('Invalid location type: ' + url_location_type)

class TripMemberListView(LoginRequiredMixin, FormView):
    model = TripMember
    template_name = 'trips/members.html'
    queryset = TripMember.objects.all()
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(TripMemberListView, self).get_context_data(**kwargs)
        context['trip'] = Trip.objects.get(pk=self.kwargs['pk'])
        context['pending_members'] = self.queryset.filter(
            accept_reqd=True).order_by('email')
        context['current_members'] = self.queryset.filter(
            accept_reqd=False).order_by('email')
        return context

    # def post(self, request, *args, **kwargs):
    #
    #     return super(LoginRequiredMixin, self).post(
    #             self, request, *args, **kwargs)

def notifications(request):
    #placeholder
    return render(request, 'trips/notifications.html')
