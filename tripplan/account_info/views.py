from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from .forms import ProfileForm

User = get_user_model()

class ProfileView(UpdateView):
    model = User
    template_name = 'account_info/profile.html'
    form_class = ProfileForm
    success_url = "."

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    #
    # def form_valid(self, form):
    #     messages.add_message(self.request, messages.SUCCESS, 'Your account was successfully created.')
