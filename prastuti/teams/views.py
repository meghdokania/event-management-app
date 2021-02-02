from django.http import HttpResponse
from events.models import Event
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from users.models import CustomUser
from .models import Team
from users import views as userViews


# Create your views here.
def registerTeam(request, event):
    if not request.user.is_authenticated:
        return redirect(reverse('users:usersignin'))

    event = Event.objects.get(event_name=event)
    # makes sure not more than one team for one event

    profile = request.user
    if userViews.isRegisteredForEvent(profile, event):
        team_registered = userViews.isRegisteredForEvent(profile, event)
        return HttpResponse("<h2>You have already registered for the event {0} under the team {1}.</h2>".format(event,
                                                                                                                team_registered))  # validation error to raise here
    if request.method == 'POST':
        error = {}
        emails = {}
        team_name = request.POST['team_name']
        try:
            team = Team.objects.get(team_name=team_name, team_event=event)
            error[team.team_name] = "The teamname has already taken"
        except Team.DoesNotExist:
            pass

        team_size = int(request.POST['team_size'])

        team_members = []
        for i in range(1, team_size + 1):
            email = 'email' + str(i)
            email_id = request.POST[email]
            emails[email] = email_id
            try:
                user = CustomUser.objects.get(email=email_id)
            except CustomUser.DoesNotExist:
                # return HttpResponse(
                #     "<h2>Enter a Valid Email Id. {} has not registered on this site.</h2>".format(email_id))
                error[email] = "The user has not registered"
            # if userViews.isRegisteredForEvent(member_profile, event):
            #     team_registered = userViews.isRegisteredForEvent(member_profile, event)
            # return HttpResponse(
            #     "<h2>{2} has already registered for the event {0} under the team {1}.</h2>".format(event,

            #                                                                                      team_registered,
        self_register = False
        # try:
        #     team = Team.objects.get(team_name=team_name)
        #     error[team.team_name] = "The teamname has already taken"
        # except Team.DoesNotExist:
        #     pass
        for i in range(1, team_size + 1):
            email = 'email' + str(i)
            email_id = request.POST[email]
            emails[email] = email_id
            member_profile = None
            try:
                user = CustomUser.objects.get(email=email_id)
                member_profile = CustomUser.objects.get(email=email_id)
            except CustomUser.DoesNotExist:
                error[email] = "The user has not registered"
            if member_profile is None:
                continue
            if userViews.isRegisteredForEvent(member_profile, event):
                team_registered = userViews.isRegisteredForEvent(
                    member_profile, event)
                error[email] = 'The user has already registered for the event'

            if member_profile == profile:
                self_register = True
            # make sure one registers himself
            team_members.append(member_profile)
        member_profile = request.user
        # if there is any error
        if not self_register:
            error['notregister'] = 'You must be in the team'
        if len(error) > 0:
            mx_team_sz = event.team_size_mx
            mn_team_sz = event.team_size_mn
            allowed_team_size = []
            team_id = 'xyz'
            if event.event_name == 'Codigo' or event.event_name == 'Recognizance':
                team_id = request.POST['team_id']
            for i in range(mn_team_sz, mx_team_sz + 1):
                allowed_team_size.append(i)
            return render(request, 'register/registration.html',
                          {'allowed_team_sizes': allowed_team_size, 'event': event, 'error': error,
                           'teamsize': team_size, 'emailids': emails, "teamname": team_name, 'team_id': team_id})

        member_profile = request.user
        team_size = len(team_members)
        team = Team(team_name=team_name, team_size=team_size, team_event=event)
        if event.event_name == 'Codigo' or event.event_name == 'Recognizance':
            team.team_id = request.POST['team_id']
        team.save()
        for mem in team_members:
            team.team_not_accepted.add(mem)
            team.team_member.add(mem)
        team.team_not_accepted.remove(member_profile)
        if team.team_not_accepted.count() == 0:
            team.team_active = True
        team.save()
        return redirect(request.user.get_absolute_url())

    else:
        mx_team_sz = event.team_size_mx
        mn_team_sz = event.team_size_mn
        allowed_team_size = []
        error = {}
        emails = {'email1': request.user.email}
        # teamsize = 0
        # teamname = ""
        team_id = 'xyz'
        for i in range(mn_team_sz, mx_team_sz + 1):
            allowed_team_size.append(i)
        return render(request, 'register/registration.html',
                      {'allowed_team_sizes': allowed_team_size, 'event': event, 'teamsize': 0, 'error': error,
                       'emailids': emails})


def delete_team(request, team):
    if request.method == "POST":
        team = Team.objects.get(team_name=team)
        team.delete()

    return redirect(request.user.get_absolute_url())
