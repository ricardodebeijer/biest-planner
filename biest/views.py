from django.shortcuts import render

from biest.parser import getbookings


def index(request):
    bookings = getbookings()
    context = {
        'bookings': bookings,
    }
    return render(request, 'index.html', context)
