from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from biest.filesaver import save_planning
from biest.parser import get_bookings, get_instructors


@login_required
def index(request):
    context = {
        'bookings': get_bookings(),
        'instructors': get_instructors(),
    }
    return render(request, 'index.html', context)


@login_required
def upload_planning(request):
    if request.method == 'POST':
        try:
            planning = request.FILES['planning']
            save_planning(planning)
        except MultiValueDictKeyError:
            pass
        return redirect('index')
    else:
        return render(request, 'import.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {
                'message': 'invalid login'
            }
        return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'login.html')
