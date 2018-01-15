from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'site_info/home.html'

class AboutView(TemplateView):
    template_name = 'site_info/about.html'

class ContactView(FormView):
    template_name = 'site_info/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)
