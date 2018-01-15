from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'site_info/home.html'

class AboutView(TemplateView):
    template_name = 'site_info/about.html'

class ContactView(TemplateView):
    template_name = 'site_info/contact.html'
