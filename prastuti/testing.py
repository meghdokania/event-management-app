import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','prastuti.settings')

import django
django.setup()

from users.models import CustomUser
from teams.models import Team
from events.models import Event
from django.contrib.auth.models import User

# User.objects.all().delete()
# Team.objects.all().delete()
# for event in Event.objects.all():
#     event.delete()
# Team.objects.all().delete()
# profiles = CustomUser.objects.all()
# pr = profiles[0]
# print(profiles.filter())
# Event.objects.get_or_create(event_name = 'Simulim', team_size_mn = 1, team_size_mx = 3,discription = "This is a MATLAB event.")
# Event.objects.get_or_create(event_name = 'Consilium',team_size_mn = 1, team_size_mx = 3, discription = "This is a digital Electronics event.")
# event = Event.objects.get(event_name = "Cryptx")
# event.event_name = "CryptX"
# event.save()
# Event.objects.get_or_create(event_name = 'cryptex')
# Event.objects.get_or_create(event_name = 'cognizance')
# event1.save()
# event2.save()
# event3.save()


# team1 = Team(team_name = 'team1',team_event= event1)
# team2 = Team(team_name = 'team2',team_event= event2)
# team3 = Team(team_name = 'team3',team_event= event3)
#team1.save()
# team2.save()
# team3.save()

# print(team1.team_member.all())

# team2.save()
# print(Event.objects.all())
# # print(tr1.event)
# team3 = Team.objects.all()[2]