import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, ListView, \
    CreateView, DeleteView, DetailView, FormView, View
from django.utils import timezone
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import Trip, TripLocation, TripMember, TripNotification, \
    ItemNotification

from account_info.models import User

from .forms import TripForm, LocationForm, SearchForm, TripMemberForm, \
    TripNotificationForm


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
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        context['trip'] = trip
        context['pending_members'] = self.queryset.filter(
            trip=trip, accept_reqd=True).order_by('email')
        context['current_members'] = self.queryset.filter(
            trip=trip, accept_reqd=False).order_by('email')
        return context

class CheckUserExistsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        trip = Trip.objects.get(pk=int(request.GET.get('trip_id')))
        if User.objects.filter(email__iexact=email).exists() and not \
        TripMember.objects.filter(email__iexact=email, trip=trip).exists():
            status = 'valid'
        elif TripMember.objects.filter(email__iexact=email).exists():
            status = 'current_member'
        else:
            status = 'non_user'

        data = {'status': status}
        return JsonResponse(data)

class AddTripMemberView(LoginRequiredMixin, CreateView):
    model = TripMember
    form_class = TripMemberForm
    success_url = "#"

    def post(self, request, *args, **kwargs):
        self.kwargs['trip_id'] = request.POST.get('trip_id')
        self.kwargs['email'] = request.POST.get('email')
        return super(AddTripMemberView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super(AddTripMemberView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request and
        on intended functionality
        """
        f = form.save(commit=False)
        f.trip_id = int(self.kwargs.get('trip_id'))
        f.member_id = get_object_or_404(
            User, email=self.kwargs.get('email')).id
        f.organizer = True
        f.accept_reqd = True
        f.email = self.kwargs.get('email')
        f.save()
        response = super(AddTripMemberView, self).form_valid(form)
        data = {
            'email': self.object.member.email
        }
        if self.object.member.preferred_name:
            data['preferred_name'] = self.object.member.preferred_name
        else:
            data['preferred_name'] = ''

        return JsonResponse(data)

class AddTripNotificationView(LoginRequiredMixin, CreateView):
    model = TripNotification
    form_class = TripNotificationForm
    success_url = "#"

    def post(self, request, *args, **kwargs):
        self.kwargs['trip_id'] = request.POST.get('trip_id')
        self.kwargs['email'] = request.POST.get('email')
        self.kwargs['created_by_id'] = request.user.id
        return super(AddTripNotificationView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super(AddTripNotificationView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request and
        on intended functionality
        """
        f = form.save(commit=False)
        f.trip_id = int(self.kwargs.get('trip_id'))
        f.member_id = get_object_or_404(
            User, email=self.kwargs.get('email')).id
        f.created_by = self.kwargs.get('created_by_id')
        f.save()
        response = super(AddTripNotificationView, self).form_valid(form)
        data = {
            'trip_notification_pk': self.object.id
        }
        return JsonResponse(data)

class NotificationListView(LoginRequiredMixin, ListView):
    model = TripNotification
    template_name = 'trips/notifications.html'
    context_object_name = 'trip_notifications'
    queryset = TripNotification.objects.all()

    def get(self, request, *args, **kwargs):
        self.kwargs['user'] = request.user
        return super(NotificationListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        # gets all trip notifications for logged in user
        queryset = super(NotificationListView, self).get_queryset()
        return queryset.filter(member=self.kwargs['user'])

    def get_context_data(self, **kwargs):
        # context already has 'trip_notifications' through standard ListView
        # add 'item_notifications' to context
        context = super(NotificationListView, self).get_context_data(**kwargs)
        context['item_notifications'] = ItemNotification.objects.filter(owner=self.kwargs['user'])
        context['user_id'] = self.kwargs['user'].id
        return context

class UpdateTripMemberView(LoginRequiredMixin, UpdateView):
    model = TripMember
    form_class = TripMemberForm
    success_url = "#"

    def post(self, request, *args, **kwargs):
        self.kwargs['trip_id'] = request.POST.get('trip_id')
        self.kwargs['user_id'] = request.POST.get('user_id')
        return super(UpdateTripMemberView, self).post(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(
            TripMember,
            member_id=int(self.kwargs.get('user_id')),
            trip_id=int(self.kwargs.get('trip_id'))
        )
        return obj

    def form_invalid(self, form):
        response = super(UpdateTripMemberView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request and
        on intended functionality
        """
        f = form.save(commit=False)
        f.accept_reqd = False
        f.save()
        super(UpdateTripMemberView, self).form_valid(form)
        data = {}
        return JsonResponse(data)

class DeleteTripMemberView(LoginRequiredMixin, DeleteView):
    pass

class DeleteTripNotificationView(LoginRequiredMixin, DeleteView):
    model = TripNotification
    success_url = "#"

    def post(self, request, *args, **kwargs):
        self.kwargs['trip_id'] = request.POST.get('trip_id')
        self.kwargs['user_id'] = request.POST.get('user_id')
        super(DeleteTripNotificationView, self).post(request, *args, **kwargs)
        data = {}
        return JsonResponse(data)

    def get_object(self):
        obj = get_object_or_404(
            TripNotification,
            member_id=int(self.kwargs.get('user_id')),
            trip_id=int(self.kwargs.get('trip_id'))
        )
        return obj

    def get_queryset(self):
        super(DeleteTripNotificationView, self).get_queryset()
