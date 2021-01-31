from events.models import Event
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

from users.models import Profile
from .models import Team
from users import views as userViews
# Create your views here.

# need to optimise
def registerTeam(request,event):

    if not request.user.is_authenticated:
        return redirect(reverse('users:usersignin'))
    event = Event.objects.get(event_name = event)
    # makes sure not more than one team for one event
    profile = Profile.objects.get(user=request.user)
    if userViews.isRegisteredForEvent(profile,event):
        team_registered = userViews.isRegisteredForEvent(profile,event)
        return HttpResponse("<h2>You have already registered for the event {0} under the team {1}.</h2>".format(event,team_registered)) #validation error to raise here
    if request.method == 'POST':
        team_name = request.POST['team_name']
        team_members = []
        team_size = int(request.POST['team_size'])
        self_register = False
        for i in range(1, team_size + 1):
            email = 'email' + str(i)
            email_id = request.POST[email]
            try:
                user = User.objects.get(email=email_id)
                member_profile = Profile.objects.get(user = user)
            except User.DoesNotExist:
                return HttpResponse("<h2>Enter a Valid Email Id. {} has not registered on this site.</h2>".format(email_id))
            if userViews.isRegisteredForEvent(member_profile,event):
                team_registered = userViews.isRegisteredForEvent(member_profile,event)
                return HttpResponse("<h2>{2} has already registered for the event {0} under the team {1}.</h2>".format(event,team_registered,member_profile))
            if member_profile == profile:
                self_register = True
            # make sure one registers himself
            if not self_register:
                return HttpResponse("<h2>You need to register yourself for the event.</h2>")
            team_members.append(member_profile)
        # if deemed fit
        team_size = len(team_members)
        team = Team(team_name=team_name,team_size=team_size,team_event=event)
        team.save()
        for mem in team_members:
            team.team_member.add(mem)
        team.save()
        #sucessfull, so return a sign
        return userViews.userProfile(request,request.user.email)
    else:
        mx_team_sz = event.team_size_mx
        mn_team_sz = event.team_size_mn
        allowed_team_size = []
        for i in range(mn_team_sz, mx_team_sz + 1):
            allowed_team_size.append(i)
        return render(request,'register/registration.html',{'allowed_team_sizes':allowed_team_size,'event':event})