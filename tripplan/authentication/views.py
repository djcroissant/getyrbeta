from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
# from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from allauth.account import views

# from authtools import views

# from .forms import SignupForm

User = get_user_model()

class SignupView(views.SignupView):
    # template_name = 'auth/signup.html'
    # form_class = SignupForm
    # model = User
    success_url = reverse_lazy('trips:trip_list')

    # def form_valid(self, form):
    #     '''
    #     Given an email address and password, create a new
    #     user account, login, and redirect to welcome page
    #     '''
    #     email = form.cleaned_data.get('email')
    #     password = form.cleaned_data.get('password')
    #     User.objects.create_user(email=email, password=password)
    #     user = authenticate(email=email, password=password)
    #     if user is not None:
    #         login(self.request, user)
    #         messages.add_message(self.request, messages.SUCCESS, 'Your account was successfully created.')
    #         return super(SignUpView, self).form_valid(form)
    #     else:
    #         messages.add_message(self.request, messages.ERROR, 'There was a problem creating your account.')
    #         return super(SignUpView, self).form_valid(form)

class SignInView(views.LoginView):
    disallow_authenticated = True
    template_name = 'auth/signin.html'

class SignOutView(views.LogoutView):
    template_name = 'core/welcome.html'
