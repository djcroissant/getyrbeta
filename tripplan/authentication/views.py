from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from allauth.account import views
from allauth.socialaccount import views as socialviews

from .forms import LoginForm, SignupForm

from trips.models import TripGuest, TripMember

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

class SocialSignupView(LoginView):
    '''
    This view interrupts a request to /social/signup. This url is requested
    when a social log in is attempted with an email address that already
    exists. This view overrides the allauth default, posts a message, and
    maintains focus on the login page. It inherits from LoginView, which
    inherits from allauth's LoginView.
    '''
    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
            '''A user with your email address already exists. To link
            Facebook with your existing account, please log in,
            then click "Profile" -> "Login Info".''')
        return super(SocialSignupView, self).get(request, *args, **kwargs)

class SocialConnectionsView(socialviews.ConnectionsView):
    template_name = 'authentication/social_connections.html'

class PasswordResetView(views.PasswordResetView):
    template_name = 'authentication/password_reset.html'

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'

class PasswordResetFromKeyView(views.PasswordResetFromKeyView):
    template_name = 'authentication/password_reset_from_key.html'

class PasswordResetFromKeyDoneView(views.PasswordResetFromKeyDoneView):
    template_name = 'authentication/password_reset_from_key_done.html'

class ConfirmEmailView(views.ConfirmEmailView):
    template_name = 'authentication/email_confirm.html'
