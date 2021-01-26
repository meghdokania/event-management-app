from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from ..users.models import Profile
from ..teams.models import Team
# Create your models here.

class Event(models.Model):
    event_name = models.CharField(max_length=20)
    team_event = models.BooleanField()
    #event_info = models.TextField()

events_map = {
    'lorem' : Event(event_name ='lorem'),
    'ipsum': Event(event_name ='ipsum'),
    'dolor': Event(event_name ='dolor'),
    'set' : Event(event_name ='set'),
    'amet' : Event(event_name ='amet'),
}

class EventRegistration(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)