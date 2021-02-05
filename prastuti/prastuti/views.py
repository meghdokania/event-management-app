from django.shortcuts import render

from events import models as eventModel


def Home(request, nouse=None):
    events = eventModel.Event.objects.all()
    currentHome = 1
    return render(request, 'prastuti/home.html', {'events':events, 'currentHome':currentHome})

def Schedule(request):
    return render(request, 'prastuti/schedule.html', {'currentSchedule':1})