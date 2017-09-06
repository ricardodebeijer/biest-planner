from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from biest.filesaver import save_planning
from biest.parser import getbookings


def index(request):
    bookings = getbookings()
    context = {
        'bookings': bookings,
    }
    return render(request, 'index.html', context)


def upload_planning(request):
    if request.method == 'POST':
        try:
            planning = request.FILES['planning']
            save_planning(planning)
        except MultiValueDictKeyError:
            pass
    return redirect('index')
