from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileView(generic.DetailView):
    model = User
    template_name = 'account_info/profile.html'

# def profile(request):
#     return render(request, 'account_info/profile.html')
