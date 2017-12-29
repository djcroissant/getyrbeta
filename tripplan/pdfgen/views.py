from django.shortcuts import render
from django.http import HttpResponse

from reportlab.pdfgen import canvas


def hello_world(request):
    # Create HttpResponse object.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename='hello_world.pdf'"

    # Create pdf object with response object as its file.
    p = canvas.Canvas(response)

    # Draw on pdf.
    p.drawString(100, 100, "Hello world")

    # Close pdf object cleanly
    p.showPage()
    p.save()
    return response
