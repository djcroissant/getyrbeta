from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


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

def TripPlanView(TemplateView)
    template_name = "pdfgen/trip_plan.html"
