from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import forms
from .models import Profile


# Create your views here.

def usersList(request):
    return render(request,'base.html')

def userSignin(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)#... not good practice

        if(form.is_valid()):
            user = form.get_user()
            login(request, user)
            # user = User.objects.get(user.username)
            profile = Profile.objects.get(user=user)
            teams = profile.team_set.all()
            return render(request, 'users/profile.html', {'profile':profile,'teams':teams})
        # need to add else here
    else:
        form = AuthenticationForm()
    return render(request, "users/signin.html", {'form': form})

def userSignup(request):
    if request.method == "POST":
        user_form = forms.UserForm(request.POST)
        profile_form = forms.ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            user.save()
            profile.save()
            login(request, user)
            # messages.success(request, "You Signup successfully")
            return userProfile(request,user.email)
    else :
        user_form = forms.UserForm()
        profile_form = forms.ProfileForm()
    return render(request, 'users/signup.html',
          {
             'user_form' : user_form,
             'profile_form' : profile_form
          })

@login_required
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:userslist'))

def userProfile(request, email):
    user = User.objects.get(email=email)
    profile = Profile.objects.get(user=user)
    return render(request, 'users/profile.html', {'profile':profile,'teams':profile.team_set.all()})

def isRegisteredForEvent(profile, event):
    for team in profile.team_set.all():
        if team.team_event == event:
            return team
    return None