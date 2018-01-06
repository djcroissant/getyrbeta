import datetime

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models.functions import Lower

from easy_pdf.views import PDFTemplateView

from trips.models import Trip, TripMember, TripLocation, Item

def hello_world(request):
    # Create HttpResponse object.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename='hello_world.pdf'"

    # Create pdf object with response object as its file.
    p = canvas.Canvas(response, pagesize=letter)

    # Define variables for dimensions
    width, height = letter

    # Draw on pdf.
    p.translate(inch, inch)
    p.setFont("Helvetica", 14)
    p.setStrokeColorRGB(0.2,0.5,0.3)
    p.setFillColorRGB(1,0,1)
    p.line(0,0,0,1.7*inch)
    p.line(0,0,1*inch,0)
    p.rect(0.2*inch,0.2*inch,1*inch,1.5*inch, fill=1)
    # p.rotate(90)
    p.setFillColorRGB(0,0,0.77)
    p.drawString(0, 0.2*inch, "Hello world")

    # Close pdf object cleanly
    p.showPage()
    p.save()
    return response

class TripPlanView(PDFTemplateView):
    template_name = "pdfgen/trip_plan.html"
    # base_url = settings.STATIC_ROOT
    # download_filename = "test.pdf"

    def get_context_data(self, **kwargs):
        context = super(TripPlanView, self).get_context_data(**kwargs)
        trip = get_object_or_404(Trip, pk=self.kwargs['trip_id'])
        context['trip'] = trip
        context['object_list'] = TripMember.objects.filter(
            trip_id = trip.id,
            accept_reqd = False
        )

        # Context for route overview
        context['detail_page_title'] = "Route Overview"
        if trip.number_nights > 0:
            context['end_date'] = trip.start_date + datetime.timedelta(
                days=trip.number_nights)

        context['trailhead'] = trip.get_trailhead()
        context['endpoint'] = trip.get_endpoint()

        context['objective_dict'] = trip.get_location_context(
            TripLocation.OBJECTIVE)
        context['camp_dict'] = trip.get_location_context(TripLocation.CAMP)

        # Context for gear list
        trip_items = Item.objects.filter(
                trip_id = self.kwargs['trip_id']
            ).prefetch_related(
                'item_owners'
            )
        context['trip_items'] = trip_items.order_by(Lower('description'))

        trip_members = TripMember.objects.filter(
                trip=trip
            ).select_related('member')
        context['trip_members'] = trip_members
        return context
