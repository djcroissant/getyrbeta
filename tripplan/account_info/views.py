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

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {self.context_object_name: self.form_class()})

    # def get(self, request, **kwargs):
    #     self.object
    #
    # def post(self, request, *args, **kwargs):
    #     bound_form = self.form_class(request.POST)
    #     if bound_form.is_valid():
    #         new_obj = bound_form.save()
    #         return redirect(new_obj)
    #     return render(request, self.template_name, {self.context_object_name: bound_form})

    # def get(self, request, *args, **kwargs):
    #     request_pk = kwargs.get('pk')
    #     user = get_object_or_404(User, pk=request_pk)
    #     return render(request, self.template_name, {'user': user})

    # def get_success_url(self):
    #     return reverse('account_info:account_profile', pk=user.id)
    #
    # def form_valid(self, form):
    #     '''
    #     Given an email address and password, create a new
    #     user account, login, and redirect to welcome page
    #     '''
    #     email = form.cleaned_data.get('email')
    #     password = form.cleaned_data.get('password')
    #     User.objects.create_user(email=email, password=password)
    #     user = authenticate(email=email, password=password)
    #     login(self.request, user)
    #     messages.add_message(self.request, messages.SUCCESS, 'Your account was successfully created.')
    #
    #     return super(SignUpView, self).form_valid(form)
