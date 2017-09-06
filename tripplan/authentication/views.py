from django.shortcuts import render#, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'There was a problem while creating your account. Please review your information and resubmit')
            return render(request, 'auth/signup.html', { 'form': form })
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Your account was successfully created.')
            return HttpResponseRedirect('welcome')
    else:
        return render(request, 'auth/signup.html', { 'form': SignUpForm() })

def signin(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(reverse('trips:trip_list'))
    # else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                ##
                ## The code below came from Parsif.al. Not sure if it is recommended
                ## but it doesn't currently apply, so I'm commenting it out. Might
                ## want to revisit later
                ##
                # if user.is_active:
                #     login(request, user)
                #     if 'next' in request.GET:
                #         return HttpResponseRedirect(request.GET['next'])
                #     else:
                #         return HttpResponseRedirect('/')
                # else:
                #     messages.add_message(request, messages.ERROR, 'Your account is desactivated.')
                #     return render(request, 'auth/signin.html')

                login(request, user)
                return HttpResponseRedirect(reverse('trips:trip_list'))
            else:
                messages.add_message(request, messages.ERROR, 'Username or password invalid.')
                return render(request, 'auth/signin.html')
        else:
            return render(request, 'auth/signin.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))
