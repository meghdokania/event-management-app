from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from . import forms
from .models import Profile


# Create your views here.

def usersList(request):
    html = "<html><body>Hello %s.</body></html>" %'Aman'
    return HttpResponse(html)

def userSignin(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if(form.is_valid()):
            user = form.get_user()
            login(request, user)
            # user = User.objects.get(user.username)
            profile = Profile.objects.get(user=user)
            return render(request, 'users/profile.html', {'profile':profile})
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
            return render(request, 'users/profile.html', {'profile':profile})
    else :
        user_form = forms.UserForm()
        profile_form = forms.ProfileForm()
    return render(request, 'users/signup.html',
          {
             'user_form' : user_form,
             'profile_form' : profile_form
          })

def userLogout(request):
    prev = request.META.get('HTTP_REFERER')
    logout(request)
    messages.success(request, "You logged out")
    return redirect(prev)

def userProfile(request, email):
    user = User.objects.get(username=email)
    profile = Profile.objects.get(user=user)
    return render(request, 'users/profile.html', {'profile':profile})

