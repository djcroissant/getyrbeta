from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView, ListView, \
    CreateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.http import Http404

from account_info.models import EmergencyContact, Vehicle

from .forms import ProfileForm, EmergencyContactForm, VehicleForm

User = get_user_model()

class ProfileView(UpdateView):
    model = User
    template_name = 'account_info/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account_info:account_profile')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(ProfileView, self).get(self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(ProfileView, self).post(self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

class EmergencyContactListView(ListView):
    model = EmergencyContact
    template_name = 'emerg_contact/list.html'

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactListView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

# Removing this code. No reason why a post request should come to this view
    # def post(self, request, *args, **kwargs):
    #     if request.user and request.user.is_authenticated():
    #         return super(EmergencyContactListView, self).post(
    #             self, request, *args, **kwargs)
    #     else:
    #         redirect_path = reverse('authentication:signin')
    #         redirect_next = '?next=' + request.path
    #         return redirect(redirect_path + redirect_next)

    def get_queryset(self):
        queryset = super(EmergencyContactListView, self).get_queryset()
        return queryset.filter(user=self.request.user)

class EmergencyContactEditView(UpdateView):
    model = EmergencyContact
    template_name = 'account_info/edit.html'
    form_class = EmergencyContactForm
    success_url = reverse_lazy('account_info:emerg_contact_list')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactEditView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactEditView, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def get_object(self):
        emerg_contact = super(EmergencyContactEditView, self).get_object()
        if not emerg_contact.user.id == self.request.user.id:
            raise Http404('The requested emergency contact does not exist')
        else:
            return emerg_contact

    def get_context_data(self, **kwargs):
        context = super(EmergencyContactEditView, self).get_context_data(**kwargs)
        context['reverse_path'] = 'account_info:emerg_contact_edit'
        context['reverse_pk'] = self.kwargs.get('pk')
        return context

class EmergencyContactCreateView(CreateView):
    model = EmergencyContact
    template_name = 'account_info/create.html'
    form_class = EmergencyContactForm
    success_url = reverse_lazy('account_info:emerg_contact_list')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactCreateView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactCreateView, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EmergencyContactCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EmergencyContactCreateView, self).get_context_data(**kwargs)
        context['reverse_path'] = 'account_info:emerg_contact_create'
        context['page_title'] = 'Add new emergency contact'
        context['save_button_title'] = 'Save Profile'
        return context

class EmergencyContactDeleteView(DeleteView):
    model = EmergencyContact
    template_name = 'emerg_contact/delete.html'
    success_url = reverse_lazy('account_info:emerg_contact_list')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactDeleteView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactDeleteView, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def get_object(self):
        emerg_contact = super(EmergencyContactDeleteView, self).get_object()
        if not emerg_contact.user.id == self.request.user.id:
            raise Http404('The requested emergency contact does not exist')
        else:
            return emerg_contact

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicle/list.html'

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(VehicleListView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

# Removing this code. No reason why a post request should come to this view
    # def post(self, request, *args, **kwargs):
    #     if request.user and request.user.is_authenticated():
    #         return super(VehicleListView, self).post(
    #             self, request, *args, **kwargs)
    #     else:
    #         redirect_path = reverse('authentication:signin')
    #         redirect_next = '?next=' + request.path
    #         return redirect(redirect_path + redirect_next)

    def get_queryset(self):
        queryset = super(VehicleListView, self).get_queryset()
        return queryset.filter(owner=self.request.user)

class VehicleEditView(UpdateView):
    model = Vehicle
    template_name = 'account_info/edit.html'
    form_class = VehicleForm
    success_url = reverse_lazy('account_info:vehicle_list')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(VehicleEditView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(VehicleEditView, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def get_object(self):
        vehicle = super(VehicleEditView, self).get_object()
        if not vehicle.owner.id == self.request.user.id:
            raise Http404('The requested vehicle does not exist')
        else:
            return vehicle

    def get_context_data(self, **kwargs):
        context = super(VehicleEditView, self).get_context_data(**kwargs)
        context['reverse_path'] = 'account_info:vehicle_edit'
        context['reverse_pk'] = self.kwargs.get('pk')
        return context

class VehicleCreateView(CreateView):
    model = Vehicle
    template_name = 'account_info/create.html'
    form_class = VehicleForm
    success_url = reverse_lazy('account_info:vehicle_list')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(VehicleCreateView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(VehicleCreateView, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(VehicleCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VehicleCreateView, self).get_context_data(**kwargs)
        context['reverse_path'] = 'account_info:vehicle_create'
        context['page_title'] = 'Add new vehicle'
        context['save_button_title'] = 'Save Vehicle'
        return context

class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'vehicle/delete.html'
    success_url = reverse_lazy('account_info:vehicle_list')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(VehicleDeleteView, self).get(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(VehicleDeleteView, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def get_object(self):
        vehicle = super(VehicleDeleteView, self).get_object()
        if not vehicle.owner.id == self.request.user.id:
            raise Http404('The requested vehicle does not exist')
        else:
            return vehicle
