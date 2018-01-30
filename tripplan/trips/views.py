import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, ListView, \
    CreateView, DeleteView, DetailView, FormView, View, TemplateView
from django.utils import timezone
from django.contrib.auth import authenticate
from django.http import JsonResponse, Http404, HttpResponse
from django.core.mail import send_mail
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models.functions import Lower
from django.conf import settings


import pytz

from .models import Trip, TripLocation, TripMember, ItemNotification, \
    TripGuest, Item, ItemOwner
from account_info.models import EmergencyContact

from account_info.models import User

from .forms import TripForm, LocationForm, SearchForm, TripMemberForm, \
    TripGuestForm, ItemModelForm, ItemOwnerModelForm


class LoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(LoginRequiredMixin, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:login')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(LoginRequiredMixin, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:login')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

class FlattenTripMemberMixin:
    def flatten_tripmember_queryset(self, queryset):
        '''
        Input a TripMember queryset. Output a list in the form:
        if preferred_name exists:
            "<preferred_name> - <email>"
        else:
            "<email>"

        Used to pre-process data before adding to context to template.
        '''
        flat_list = []
        for tripmember in queryset:
            if tripmember.member.preferred_name:
                name = (tripmember.member.preferred_name + " - ")
            elif tripmember.member.full_name:
                name = (tripmember.member.full_name + " - ")
            else:
                name = ""
            flat_list.append(name + tripmember.member.email)
        return flat_list

class InviteEmailMixin:
    def email_invitation(self, status="registered"):
        trip = get_object_or_404(
            Trip,
            id=int(self.request.POST.get('trip_id'))
        )

        if status == "nonregistered":
            link_action =  reverse('authentication:signup')
            template = "trips/email/invite_nonregistered.txt"
        else:
            link_action =  reverse('authentication:login')
            template = "trips/email/invite_registered.txt"

        subject = ("Get Yr Beta - Invitation to %s" % trip.title)
        message = render_to_string(
            template,
            context = {
                'inviter_email': self.request.user.email,
                'trip_title': trip.title,
                'link': 'https://www.getyrbeta.com' + link_action +
                    '?next=' + reverse('trips:notifications'),
            }
        )
        from_email = 'noreply@getyrbeta.com'
        to_email = (self.request.POST.get('email'),)

        send_mail(
            subject,
            message,
            from_email,
            to_email,
            fail_silently=False,
        )

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
    form. The view will receive a location_type in the url (trailhead,
    objective, or camp). The view converts this to a two character code
    through a model method. The get_form_kwargs receives the two character code
    and calls another model method, passing the appropriate argument, and
    receives a list of date choices (prefixed with either 'Day' or 'Night'
    according to the location_type.)
    """
    model = TripLocation
    template_name = 'trips/location.html'
    form_class = LocationForm

    def get_form_kwargs(self):
        """
        Adds a tuple of choices for the date field to the form kwargs.
        """
        kwargs = super(LocationFormMixin, self).get_form_kwargs()
        kwargs['location_type'] = self.kwargs.get('location_type')
        if kwargs['location_type'] == TripLocation.CAMP:
            date_type = 'night'
        else:
            date_type = 'day'
        date_list = Trip.objects.get(pk=self.kwargs.get(
            'trip_id')).get_date_choices(date_type)
        choices = []
        for item in date_list:
            choices.append((item, item))
        kwargs['choices'] = tuple(choices)

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(LocationFormMixin, self).get_context_data(**kwargs)
        context['googleAPI'] = settings.GOOGLE_MAPS_API
        return context


class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/index.html'

    def get_queryset(self):
        queryset = self.request.user.trip_set.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TripListView, self).get_context_data(**kwargs)
        context['upcoming_trip_list'] = self.object_list.filter(
            start_date__gte=timezone.now()).order_by('start_date')
        context['past_trip_list'] = self.object_list.filter(
            start_date__lt=timezone.now()).order_by('start_date')
        return context

class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TripDetailView, self).get_context_data(**kwargs)
        trip = self.get_object()
        context['detail_page_title'] = trip.title
        if trip.number_nights > 0:
            context['end_date'] = trip.start_date + datetime.timedelta(
                days=trip.number_nights)

        trailhead = trip.get_trailhead()
        context['trailhead'] = trailhead
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

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request and
        on intended functionality
        """
        response = super(TripCreateView, self).form_valid(form)
        TripMember.objects.create(
            organizer=True,
            accept_reqd=False,
            trip=self.object,
            member=self.request.user,
        )
        return response

    def get_success_url(self):
        return reverse('trips:trip_detail', args=(self.object.id,))

class LocationCreateView(LoginRequiredMixin, LocationGeneralMixin,
    LocationFormMixin, CreateView):
    def set_instance_variables(self, **kwargs):
        url_location_type = self.kwargs.get('location_type').lower()
        try:
            self.kwargs['location_type'] = TripLocation.LOCATION_TYPE[
                url_location_type]
            self.page_title = 'Enter a new ' + url_location_type + ' location'
            self.submit_button_title = 'Save ' + url_location_type.capitalize()
        except KeyError:
            raise Http404('Invalid location type: ' + url_location_type)

    def get_initial(self):
        trip = get_object_or_404(Trip, pk=self.kwargs.get('trip_id'))
        location_type = self.kwargs.get('location_type')
        return {
            'trip': trip,
            'location_type': location_type,
            'date': trip.get_date_choices()[0]
        }

class LocationEditView(LoginRequiredMixin, LocationGeneralMixin,
    LocationFormMixin, UpdateView):
    def set_instance_variables(self, **kwargs):
        url_location_type = self.kwargs.get('location_type').lower()
        try:
            self.kwargs['location_type'] = TripLocation.LOCATION_TYPE[
                url_location_type]
            self.page_title = 'Edit ' + url_location_type + ' details'
            self.submit_button_title = 'Save ' + url_location_type.capitalize()
        except KeyError:
            raise Http404('Invalid location type: ' + url_location_type)

class LocationDeleteView(LoginRequiredMixin, LocationGeneralMixin, DeleteView):
    template_name = 'trips/delete.html'
    context_object_name = 'triplocation'

    def set_instance_variables(self, **kwargs):
        url_location_type = self.kwargs.get('location_type').lower()
        try:
            # setting 'location_type' ensures a valid URL is entered
            self.kwargs['location_type'] = TripLocation.LOCATION_TYPE[
                url_location_type]
            self.page_title = 'Delete ' + url_location_type
            self.submit_button_title = 'Delete ' + url_location_type.capitalize()
        except KeyError:
            raise Http404('Invalid location type: ' + url_location_type)

class TripMemberListView(LoginRequiredMixin, FlattenTripMemberMixin, FormView):
    model = TripMember
    template_name = 'trips/members.html'
    queryset = TripMember.objects.all()
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(TripMemberListView, self).get_context_data(**kwargs)
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        context['trip'] = trip

        # Check for registered users that still need to accept trip invite
        # Then flatten queryset into a list
        pending_member_query = self.queryset.filter(
            trip=trip,
            accept_reqd=True
        )
        pending_user_list = self.flatten_tripmember_queryset(
            pending_member_query)

        # Check for non-registered users that still need to accept trip invite.
        # Output as a list with form: "<email>"
        pending_guest_list = list(TripGuest.objects.filter(
            trip=trip
        ).values_list(
            'email',
            flat=True
        ))

        # Combine lists of registered and non-registered users that need to
        # accept invite
        context['pending_members'] = sorted(
            (pending_user_list + pending_guest_list),
            key=lambda s: s.lower()
        )

        # Find users that are registered and have accepted trip invitation.
        # Then flatten queryset into a list and add to context
        current_member_query = self.queryset.filter(
            trip=trip,
            accept_reqd=False
        )
        current_member_list = self.flatten_tripmember_queryset(
            current_member_query)
        context['current_members'] = sorted(
            current_member_list,
            key=lambda s: s.lower()
        )

        return context

class CheckUserExistsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        trip = Trip.objects.get(pk=int(request.GET.get('trip_id')))

        if TripMember.objects.filter(
            member__email__iexact=email,
            trip=trip
        ).exists() or TripGuest.objects.filter(
            email__iexact=email,
            trip=trip
        ).exists():
            status = 'current_member'
        elif User.objects.filter(email__iexact=email).exists():
            status = 'nonmember_user'
        else:
            status = 'nonmember_guest'

        data = {'status': status}
        return JsonResponse(data)

class AddTripMemberView(LoginRequiredMixin, FlattenTripMemberMixin,
    InviteEmailMixin, CreateView):
    model = TripMember
    form_class = TripMemberForm
    success_url = "#"

    def form_invalid(self, form):
        response = super(AddTripMemberView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request and
        on intended functionality
        Person being invited = self.request.POST.get('email')
        """
        f = form.save(commit=False)
        f.trip_id = int(self.request.POST.get('trip_id'))
        f.member_id = get_object_or_404(
            User, email=self.request.POST.get('email')).id
        f.organizer = True
        f.accept_reqd = True
        f.save()
        response = super(AddTripMemberView, self).form_valid(form)
        self.email_invitation('registered')

        # The flatten_tripmember_queryset requires input to be an iterable
        # and outputs a list.
        data = {
            'new_member': self.flatten_tripmember_queryset((self.object,))[0]
        }
        # Send text for success message to template
        msg = ("An invitation has been sent to %s to join the trip." %
            self.request.POST.get('email'))
        data['msg'] = msg

        return JsonResponse(data)

class AddTripGuestView(LoginRequiredMixin, InviteEmailMixin, CreateView):
    model = TripGuest
    form_class = TripGuestForm
    success_url = "#"

    def form_invalid(self, form):
        response = super(AddTripGuestView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request and
        on intended functionality
        Person being invited = self.request.POST.get('email')
        Person sending the invitation = self.request.user.email
        """
        f = form.save(commit=False)
        f.trip_id = int(self.request.POST.get('trip_id'))
        f.email = self.request.POST.get('email')
        f.save()
        response = super(AddTripGuestView, self).form_valid(form)
        self.email_invitation('nonregistered')
        data = {
            'new_member': self.object.email
        }

        # Send text for success message to template
        msg = ("An invitation has been sent to %s to join the trip." %
            self.request.POST.get('email'))
        data['msg'] = msg

        return JsonResponse(data)

class NotificationListView(LoginRequiredMixin, ListView):
    model = TripMember
    template_name = 'trips/notifications.html'
    context_object_name = 'trip_notifications'

    def get_queryset(self):
        # gets all trip notifications for logged in user
        queryset = super(NotificationListView, self).get_queryset()
        return queryset.filter(member=self.request.user, accept_reqd=True)

    def get_context_data(self, **kwargs):
        # context already has 'trip_notifications' through standard ListView
        # add 'item_notifications' to context
        context = super(NotificationListView, self).get_context_data(**kwargs)
        context['item_notifications'] = ItemNotification.objects.filter(
            owner=self.request.user)
        context['user_id'] = self.request.user
        return context

class UpdateTripMemberView(LoginRequiredMixin, UpdateView):
    model = TripMember
    form_class = TripMemberForm
    success_url = "#"

    def post(self, request, *args, **kwargs):
        self.kwargs['trip_id'] = request.POST.get('trip_id')
        return super(UpdateTripMemberView, self).post(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(
            TripMember,
            member_id=self.request.user.id,
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
    model = TripMember
    success_url = "#"

    def post(self, request, *args, **kwargs):
        self.kwargs['trip_id'] = request.POST.get('trip_id')
        super(DeleteTripMemberView, self).post(request, *args, **kwargs)
        data = {}
        return JsonResponse(data)

    def get_object(self):
        obj = get_object_or_404(
            TripMember,
            member_id=self.request.user.id,
            trip_id=int(self.kwargs.get('trip_id'))
        )
        return obj

class EmergencyInfoListView(LoginRequiredMixin, ListView):
    model = TripMember
    template_name = 'trips/emergency_info.html'
    queryset = TripMember.objects.all()

    def get_queryset(self):
        # Returns TripMembers for current trip with accept_reqd = False
        queryset = super(EmergencyInfoListView, self).get_queryset()
        return queryset.filter(
            trip_id = self.kwargs['trip_id'],
            accept_reqd = False
        )

    def get_context_data(self, **kwargs):
        context = super(EmergencyInfoListView, self).get_context_data(**kwargs)
        context['trip'] = Trip.objects.get(pk=self.kwargs['trip_id'])
        return context

class GearListView(LoginRequiredMixin, TemplateView):
    template_name = 'trips/gear.html'

    def get_context_data(self, **kwargs):
        context = super(GearListView, self).get_context_data(**kwargs)

        trip = Trip.objects.get(pk=self.kwargs['trip_id'])
        context['trip'] = trip

        trip_items = Item.objects.filter(
                trip_id = self.kwargs['trip_id']
            ).prefetch_related(
                'item_owners'
            )
        context['trip_items'] = trip_items.order_by(Lower('description'))

        trip_members = TripMember.objects.filter(
                trip=trip
            ).select_related('member')
        context['trip_members'] = trip_members
        return context

class AddItemView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemModelForm
    success_url = "#"
    template_name = 'trips/ajax/item.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(AddItemView, self).get_context_data(**kwargs)
        context['form'].fields['trip_id'].initial = self.request.GET.get('trip_id')
        return context

    def form_invalid(self, form):
        response = super(AddItemView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request
        """
        f = form.save(commit=False)
        f.trip_id = self.request.POST.get('trip_id')
        f.save()
        response = super(AddItemView, self).form_valid(form)
        msg = ("Successfully added %s to the gear list." % self.object.description)
        data = {
            'item_id': self.object.id,
            'msg': msg
        }
        return JsonResponse(data)

class AddItemOwnerView(LoginRequiredMixin, CreateView):
    model = ItemOwner
    form_class = ItemOwnerModelForm
    success_url = "#"
    template_name = 'trips/ajax/itemowner.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(AddItemOwnerView, self).get_context_data(**kwargs)
        context['form'].fields['owner_id'].initial = self.request.GET.get('owner_id')
        # accept_reqd funtionality to be activated in future release
        # setting all to False for now
        context['form'].fields['accept_reqd'].initial = False
        return context

    def form_invalid(self, form):
        response = super(AddItemOwnerView, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        """
        Set values for the form based on data passed by AJAX request
        """
        f = form.save(commit=False)
        f.item_id = self.request.POST.get('item_id')
        f.owner_id = self.request.POST.get('owner_id')
        f.save()
        response = super(AddItemOwnerView, self).form_valid(form)
        data = {}
        return JsonResponse(data)

class PreviewView(LoginRequiredMixin, TemplateView):
    template_name = 'trips/preview.html'

    def get_context_data(self, **kwargs):
        context = super(PreviewView, self).get_context_data(**kwargs)
        trip = Trip.objects.get(pk=self.kwargs['trip_id'])
        context['trip'] = trip
        return context
