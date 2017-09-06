from django.shortcuts import render#, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Vehicle, Trip #, User


class TripList(generic.ListView):
    model = Trip
    template_name = 'trips/index.html'
    context_object_name = 'upcoming_trip_list'

    def get_queryset(self):
        """
        Return trips with a start date today or in the future
        """
        return Trip.objects.filter(start_date__gte=timezone.now()
               ).order_by('start_date')

class TripView(generic.DetailView):
    model = Trip
    template_name = 'trips/detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # data['user_list'] = self.object.user_set.all()
        return data

class TripCreateView(generic.CreateView):
    model = Trip
    template_name = 'trips/create.html'
    fields = ['title', 'start_date', 'trailhead_latitude', 'trailhead_longitude']

    def get_success_url(self, **kwargs):
        return reverse('trips:trip_list')

# class UserView(generic.DetailView):
#     model = User
#     template_name = 'users/detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserView, self).get_context_data(**kwargs)
#         context['vehicle_list'] = self.object.vehicle_set.all()
#         return context

class VehicleView(generic.DetailView):
    model = Vehicle
    template_name = 'vehicles/detail.html'

class VehicleCreateView(generic.CreateView):
    model = Vehicle
    template_name = 'vehicles/create.html'
    fields = ['year', 'make', 'model', 'lic_plate_num',
              'lic_plate_st']

    # def get_success_url(self, **kwargs):
    #     return reverse('trips:user_detail', args=(self.kwargs['user_id'],))

    def get_context_data(self, **kwargs):
        context = super(VehicleCreateView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['user_id'])
        return context

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_id'])
        return super(VehicleCreateView, self).form_valid(form)

# class NotificationView(generic.View):
#     template_name = 'trips/notifications.html'

def notifications(request):
    return render(request, 'trips/notifications.html')
