from django.shortcuts import render

from events import models as eventModel


def Home(request, nouse=None):
    events = eventModel.Event.objects.all()
    return render(request, 'prastuti/home.html', {'events': events})
