from django.db import models
from django.contrib.auth.models import User
from ..events.models import Event
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Team(models.Model):
    team_member = models.ManyToManyField(User)  # we can do it with profile also
    team_name = models.CharField(max_length=100)
    team_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team_size = models.IntegerField(validators=[MinValueValidator(1),
                                                MaxValueValidator(4)])  # team size between 1 and 4

    def __str__(self):
        return self.team_name

    def get_absolute_url(self):
        return reverse('', kwargs={})
