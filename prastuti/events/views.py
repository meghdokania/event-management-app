from django.shortcuts import render
from .models import Event

# Create your views here.
def index(request):
    events = Event.objects.all()
    return render(request,'events/index.html',{'events':events})

def event(request,event):
    return render(request,'events/'+event+'.html')