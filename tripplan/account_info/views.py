from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView, ListView, \
    CreateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.http import Http404

from .models import EmergencyContact, Vehicle

from .forms import ProfileForm, EmergencyContactForm, VehicleForm

User = get_user_model()

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

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account_info/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account_info:account_profile')

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

class EmergencyContactListView(LoginRequiredMixin, ListView):
    model = EmergencyContact
    template_name = 'emerg_contact/list.html'

    def get_queryset(self):
        queryset = super(EmergencyContactListView, self).get_queryset()
        return queryset.filter(user=self.request.user)

class EmergencyContactEditView(LoginRequiredMixin, UpdateView):
    model = EmergencyContact
    template_name = 'account_info/form.html'
    form_class = EmergencyContactForm
    success_url = reverse_lazy('account_info:emerg_contact_list')

    def get_object(self):
        emerg_contact = super(EmergencyContactEditView, self).get_object()
        if not emerg_contact.user.id == self.request.user.id:
            raise Http404('The requested emergency contact does not exist')
        else:
            return emerg_contact

    def get_context_data(self, **kwargs):
        context = super(EmergencyContactEditView, self).get_context_data(**kwargs)
        context['page_title'] = 'Edit Emergency Contact'
        context['save_button_title'] = 'Update'
        context['cancel_button_path'] = 'account_info:emerg_contact_list'
        return context

class EmergencyContactCreateView(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    template_name = 'account_info/form.html'
    form_class = EmergencyContactForm
    success_url = reverse_lazy('account_info:emerg_contact_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EmergencyContactCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EmergencyContactCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Add new emergency contact'
        context['save_button_title'] = 'Save Profile'
        context['cancel_button_path'] = 'account_info:emerg_contact_list'
        return context

class EmergencyContactDeleteView(LoginRequiredMixin, DeleteView):
    model = EmergencyContact
    template_name = 'emerg_contact/delete.html'
    success_url = reverse_lazy('account_info:emerg_contact_list')

    def get_object(self):
        emerg_contact = super(EmergencyContactDeleteView, self).get_object()
        if not emerg_contact.user.id == self.request.user.id:
            raise Http404('The requested emergency contact does not exist')
        else:
            return emerg_contact

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicle/list.html'

    def get_queryset(self):
        queryset = super(VehicleListView, self).get_queryset()
        return queryset.filter(owner=self.request.user)

class VehicleEditView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    template_name = 'account_info/form.html'
    form_class = VehicleForm
    success_url = reverse_lazy('account_info:vehicle_list')

    def get_object(self):
        vehicle = super(VehicleEditView, self).get_object()
        if not vehicle.owner.id == self.request.user.id:
            raise Http404('The requested vehicle does not exist')
        else:
            return vehicle

    def get_context_data(self, **kwargs):
        context = super(VehicleEditView, self).get_context_data(**kwargs)
        context['page_title'] = 'Edit Vehicle Information'
        context['save_button_title'] = 'Update'
        context['cancel_button_path'] = 'account_info:vehicle_list'
        return context

class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    template_name = 'account_info/form.html'
    form_class = VehicleForm
    success_url = reverse_lazy('account_info:vehicle_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(VehicleCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VehicleCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Add new vehicle'
        context['save_button_title'] = 'Save Vehicle'
        context['cancel_button_path'] = 'account_info:vehicle_list'
        return context

class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'vehicle/delete.html'
    success_url = reverse_lazy('account_info:vehicle_list')

    def get_object(self):
        vehicle = super(VehicleDeleteView, self).get_object()
        if not vehicle.owner.id == self.request.user.id:
            raise Http404('The requested vehicle does not exist')
        else:
            return vehicle
