import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','prastuti.settings')

import django
django.setup()

from users.models import Profile
from teams.models import Team
from events.models import Event

Team.objects.all().delete()
for event in Event.objects.all():
    event.delete()
# Team.objects.all().delete()

Event.objects.get_or_create(event_name = 'codigo')
Event.objects.get_or_create(event_name = 'cryptex')
Event.objects.get_or_create(event_name = 'cognizance')
# event1.save()
# event2.save()
# event3.save()

profiles = Profile.objects.all()
p1 = profiles[0]
p2 = profiles[1]
p3 = profiles[2]

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
p4 = Profile.objects.all().get(name = "himanshu_bala")
# team3.team_member.add(p4)
for tems in p4.team_set.all():
    print(tems)
