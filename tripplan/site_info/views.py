from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'site_info/about.html'
