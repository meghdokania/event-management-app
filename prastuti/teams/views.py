from events.models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect

from users.models import Profile
from .models import Team
from .forms import TeamForm
from users import views as userViews
# Create your views here.

# need to optimise
def registerTeam(request,event):

    if not request.user.is_authenticated:
        return redirect(reverse('users:usersignin'))
    event = Event.objects.get(event_name = event)
    # amkes sure not more than one team for one event
    profile = Profile.objects.get(user=request.user)
    for team in profile.team_set.all():
        if team.team_event == event:
            return userViews.userProfile(request,request.user.email) #validation error to raise here
    if request.method == 'POST':
        team_name = request.POST['team_name']
        team_members = []
        team_size = int(request.POST['team_size'])
        for i in range(1, team_size + 1):
            email = 'email' + str(i)
            try:
                email_id = request.POST[email]
                user = User.objects.get(email=email_id)
                profile = Profile.objects.get(user = user)
            except User.DoesNotExist:
                continue #raise forms.ValidationError("User with Email id {email} does not exist".format(email=email_id)) #currently not adding into team, change later
            team_members.append(profile)
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
        return render(request,'register/registration.html',{'allowed_team_sizes':allowed_team_size,'event':event,'form':form})