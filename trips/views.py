from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import User, Vehicle, Trip


class TripList(generic.ListView):
    model = Trip
    template_name = 'trips/index.html'
    # context_object_name = 'trip_list'
    #
    # def get_queryset(self):
    #     return Trip.objects.order_by('-title')

class UserView(generic.DetailView):
    model = User
    template_name = 'users/detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['vehicle_list'] = self.object.vehicle_set.all()
        return context

class VehicleView(generic.DetailView):
    model = Vehicle
    template_name = 'vehicles/detail.html'

class VehicleCreateView(generic.CreateView):
    model = Vehicle
    template_name = 'vehicles/create.html'
    fields = ['year', 'make', 'model', 'lic_plate_num',
              'lic_plate_st']

    def get_success_url(self, **kwargs):
        return reverse('trips:user_detail', args=(self.kwargs['user_id'],))

    def get_context_data(self, **kwargs):
        context = super(VehicleCreateView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['user_id'])
        return context

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_id'])
        return super(VehicleCreateView, self).form_valid(form)


class TripView(generic.DetailView):
    model = Trip
    template_name = 'trips/detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user_list'] = self.object.user_set.all()
        return data
