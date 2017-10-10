import datetime

from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, ListView, \
    CreateView, DeleteView, DetailView
from django.utils import timezone
from django.contrib.auth import authenticate

from .models import Trip, TripLocation

from account_info.models import User

from .forms import TripForm, LocationForm


class LoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(LoginRequiredMixin, self).get(self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(LoginRequiredMixin, self).post(self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

class LocationFormMixin:
    model = TripLocation
    template_name = 'trips/location.html'
    form_class = LocationForm

    def get(self, request, *args, **kwargs):
        self.set_instance_variables(**kwargs)
        return super(LocationFormMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_instance_variables(**kwargs)
        return super(LocationFormMixin, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.trip = get_object_or_404(Trip, pk=self.kwargs.get('trip_id'))
        form.instance.location_type = self.location_type
        return super(LocationFormMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LocationFormMixin, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['submit_button_title'] = self.submit_button_title
        context['cancel_button_path'] = 'trips:trip_detail'
        context['trip_id'] = self.kwargs.get('trip_id')
        return context

    def get_form_kwargs(self):
        """
        Adds a tuple of choices for the date field to the form kwargs.
        """
        kwargs = super(LocationFormMixin, self).get_form_kwargs()
        date_list = Trip.objects.get(pk=self.kwargs.get('trip_id')).get_date_choices()
        choices = []
        for item in date_list:
            choices.append((item, item))
        kwargs['choices'] = tuple(choices)
        return kwargs

    def get_success_url(self):
        return reverse('trips:trip_detail', args=self.kwargs.get('trip_id'))

class DeleteLocationMixin:
    model = TripLocation
    template_name = 'trips/delete.html'
    context_object_name = 'triplocation'

    def get_context_data(self, **kwargs):
        context = super(DeleteLocationMixin, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['submit_button_title'] = self.submit_button_title
        context['cancel_button_path'] = 'trips:trip_detail'
        context['trip_id'] = self.kwargs.get('trip_id')
        return context

    def get_success_url(self):
        return reverse('trips:trip_detail', args=self.kwargs.get('trip_id'))

class TripList(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/index.html'

    def get_context_data(self, **kwargs):
        context = super(TripList, self).get_context_data(**kwargs)
        context['upcoming_trip_list'] = Trip.objects.filter(
            start_date__gte=timezone.now()).order_by('start_date')
        context['past_trip_list'] = Trip.objects.filter(
            start_date__lt=timezone.now()).order_by('start_date')
        return context

class TripView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TripView, self).get_context_data(**kwargs)
        trip = self.get_object()
        context['page_title'] = trip.title
        if trip.number_nights > 0:
            context['end_date'] = trip.start_date + datetime.timedelta(days=trip.number_nights)

        context['trailhead'] = trip.get_trailhead()
        context['endpoint'] = trip.get_endpoint()

        context['objective_dict'] = trip.get_location_context(TripLocation.OBJECTIVE)
        context['camp_dict'] = trip.get_location_context(TripLocation.CAMP)
        return context

class TrailheadCreateView(LoginRequiredMixin, LocationFormMixin, CreateView):
    location_type = TripLocation.BEGIN
    page_title = 'Enter a new trailhead location'
    submit_button_title = 'Save Trailhead'

class ObjectiveCreateView(LoginRequiredMixin, LocationFormMixin, CreateView):
    location_type = TripLocation.OBJECTIVE
    page_title = 'Enter a new objective'
    submit_button_title = 'Save Objective'

class CampCreateView(LoginRequiredMixin, LocationFormMixin, CreateView):
    location_type = TripLocation.CAMP
    page_title = 'Enter a new camp location'
    submit_button_title = 'Save Camp'

class LocationEditView(LoginRequiredMixin, LocationFormMixin, UpdateView):
    def set_instance_variables(self, **kwargs):
        self.location_type = self.kwargs.get('location_type')
        if self.location_type == TripLocation.BEGIN:
            self.page_title = 'Edit trailhead details'
            self.submit_button_title = 'Save Trailhead'
        elif self.location_type == TripLocation.OBJECTIVE:
            self.page_title = 'Edit objective details'
            self.submit_button_title = 'Save Objective'
        elif self.location_type == TripLocation.CAMP:
            self.page_title = 'Edit camp details'
            self.submit_button_title = 'Save Camp'
        else:
            raise ValueError('Invalid location type: ' + self.location_type)

# class TrailheadEditView(LoginRequiredMixin, LocationFormMixin, UpdateView):
#     location_type = TripLocation.BEGIN
#     page_title = 'Edit trailhead details'
#     submit_button_title = 'Save Trailhead'
#
# class ObjectiveEditView(LoginRequiredMixin, LocationFormMixin, UpdateView):
#     location_type = TripLocation.OBJECTIVE
#     page_title = 'Edit objective details'
#     submit_button_title = 'Save Objective'
#
# class CampEditView(LoginRequiredMixin, LocationFormMixin, UpdateView):
#     location_type = TripLocation.CAMP
#     page_title = 'Edit camp details'
#     submit_button_title = 'Save Camp'

class TrailheadDeleteView(DeleteLocationMixin, DeleteView):
    page_title = 'Delete trailhead'
    submit_button_title = 'Delete Trailhead'

class ObjectiveDeleteView(DeleteLocationMixin, DeleteView):
    page_title = 'Delete objective'
    submit_button_title = 'Delete Objective'

class CampDeleteView(DeleteLocationMixin, DeleteView):
    page_title = 'Delete camp'
    submit_button_title = 'Delete Camp'

# class LocationDeleteView(LoginRequiredMixin, DeleteView):



# class TripEditView(LoginRequiredMixin, UpdateView):
#     model = Trip
#     template_name = 'trips/edit.html'
#     form_class = TripLocationForm
#
#     def get_context_data(self, **kwargs):
#         context = super(TripEditView, self).get_context_data(**kwargs)
#         trip = self.get_object()
#         context['page_title'] = trip.title
#         context['submit_button_title'] = 'Save Trip'
#         context['cancel_button_path'] = 'trips:trip_list'
#         if trip.number_nights > 0:
#             context['end_date'] = trip.start_date + datetime.timedelta(days=trip.number_nights)
#         return context

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


# # class UserView(generic.DetailView):
# #     model = User
# #     template_name = 'users/detail.html'
# #
# #     def get_context_data(self, **kwargs):
# #         context = super(UserView, self).get_context_data(**kwargs)
# #         context['vehicle_list'] = self.object.vehicle_set.all()
# #         return context
#
# class VehicleView(generic.DetailView):
#     model = Vehicle
#     template_name = 'vehicles/detail.html'
#
# class VehicleCreateView(generic.CreateView):
#     model = Vehicle
#     template_name = 'vehicles/create.html'
#     fields = ['year', 'make', 'model', 'lic_plate_num',
#               'lic_plate_st']
#
#     # def get_success_url(self, **kwargs):
#     #     return reverse('trips:user_detail', args=(self.kwargs['user_id'],))
#
#     def get_context_data(self, **kwargs):
#         context = super(VehicleCreateView, self).get_context_data(**kwargs)
#         context['user'] = User.objects.get(pk=self.kwargs['user_id'])
#         return context
#
#     def form_valid(self, form):
#         form.instance.user = User.objects.get(pk=self.kwargs['user_id'])
#         return super(VehicleCreateView, self).form_valid(form)

def notifications(request):
    return render(request, 'trips/notifications.html')
