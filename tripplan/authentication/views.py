from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from allauth.account import views

from .forms import LoginForm, SignupForm

User = get_user_model()

class SignupView(views.SignupView):
    template_name = 'authentication/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('trips:trip_list')

class LoginView(views.LoginView):
    template_name = 'authentication/login.html'
    form_class = LoginForm

class LogoutView(views.LogoutView):
    template_name = 'authentication/logout.html'

    def get_redirect_url(self):
        return reverse_lazy('authentication:login')
