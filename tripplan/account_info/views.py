from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import UpdateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.http import Http404

from account_info.models import EmergencyContact, Vehicle

from .forms import ProfileForm, EmergencyContactForm

User = get_user_model()

class ProfileView(UpdateView):
    model = User
    template_name = 'account_info/profile.html'
    form_class = ProfileForm
    success_url = "."

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

    #
    # def form_valid(self, form):
    #     messages.add_message(self.request, messages.SUCCESS, 'Your account was successfully created.')

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

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return super(EmergencyContactListView, self).post(
                self, request, *args, **kwargs)
        else:
            redirect_path = reverse('authentication:signin')
            redirect_next = '?next=' + request.path
            return redirect(redirect_path + redirect_next)

    def get_queryset(self):
        queryset = super(EmergencyContactListView, self).get_queryset()
        return queryset.filter(user=self.request.user)

class EmergencyContactEditView(UpdateView):
    model = EmergencyContact
    template_name = 'emerg_contact/edit.html'
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
        context['emergency_contact_id'] = self.kwargs.get('pk')
        return context
