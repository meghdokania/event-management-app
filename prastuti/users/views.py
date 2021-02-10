from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from . import forms
from prastuti.settings import EMAIL_HOST_USER
from .tokens import account_activation_token
from teams.models import Team

CustomUser = get_user_model()

# Views start from here




@login_required(login_url='users:usersignin')
def userUpdate(request, pk):
    template = 'users/update.html'
    user = CustomUser.objects.get(pk=pk)
    if user != request.user:
        return HttpResponse("You can update only your profile")
    if request.method == "POST":
        form = forms.UserUpdateForm(data=request.POST, user=user)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(user.get_absolute_url())
    else:
        form = forms.UserUpdateForm(user=user)
    return render(request, template, {'form': form})


def userSignin(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)  # ... not good practice

        if(form.is_valid()):
            user = form.get_user()
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect(user.get_absolute_url())
    else:
        form = AuthenticationForm()
    return render(request, "users/signin.html", {'form': form})


def userSignup(request):
    if request.method == "POST":
        user_form = forms.UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.is_active = False
            user.save()

            # verification mailing
            current_site = get_current_site(request)
            mail_subject = "Activate you prastuti account"
            message = render_to_string('users/activate.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            from_email = EMAIL_HOST_USER
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('<h1>Please confirm your email address to complete the registration.Please check your spam folder also.If you did not recieve mail please contact <a href="mailto:prastuti@iitbhu.ac.in">prastuti@iitbhu.ac.in</a></h1>')
    else:
        user_form = forms.UserForm()
    return render(request, 'users/signup.html',
                  {
                      'user_form': user_form,
                  })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(user.get_absolute_url())
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='users:usersignin')
def userLogout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='users:usersignin')
def userProfile(request, email):
    user = CustomUser.objects.get(email=email)
    if request.user != user:
        return redirect('home')
    team_cnt = 0
    inv_cnt = 0
    for team in user.team_set.all():
        team_cnt += 1
        for prof in team.team_not_accepted.all():
            if prof == user:
                inv_cnt += 1
    # user.email_user('View CustomUser', "Hii you viewed your profile", EMAIL_HOST_USER)
    update = True
    if user != request.user:
        update = False
    return render(request, 'users/profile.html', {'profile': user, 'update': update, 'teams': user.team_set.all(), 'team_cnt': team_cnt, 'inv_cnt': inv_cnt})


def userRecovery(request):
    if request.method == "POST":
        form = forms.PasswordResetForm(data=request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['email']
            current_site = get_current_site(request)
            mail_subject = "Change your prastuti password"
            user = CustomUser.objects.get(email=to_email)
            message = render_to_string('users/activate.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'recovery': True,
            })
            from_email = EMAIL_HOST_USER
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('We have sent recovery letter to your registered email')

    else:
        form = forms.PasswordResetForm()
    return render(request, 'users/recovery.html', {'form': form})


def userNewpassword(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = forms.PasswordUpdateForm(data=request.POST, user=user)
            if form.is_valid():
                user = form.save()
                user.save()
                login(request, user)
                return redirect(user.get_absolute_url())
        else:
            form = forms.PasswordUpdateForm(data=request.POST, user=user)
        return render(request, 'users/newpassword.html', {'form': form})

    else:
        return HttpResponse('Recovery link is invalid!')


def isRegisteredForEvent(profile, event):
    for team in profile.team_set.all():
        if team.team_event == event and not profile in team.team_not_accepted.all():
            return team
    return None


def eventAcceptance(request, team):
    id = int(team)
    if(request.method == "POST"):
        accept = request.POST['accepted']

        if(accept == "Yes"):
            team = Team.objects.get(id=id)
            custom = CustomUser.objects.get(email=request.user.email)
            team.team_not_accepted.remove(custom)
            team.save()
            for option_team in custom.pending.filter(team_event=team.team_event):
                option_team.delete()
            if(team.team_not_accepted.count() == 0):
                team.team_active = True
                team.save()
            return redirect(request.user.get_absolute_url())
        else:
            team = Team.objects.get(id=id)
            team.delete()
        return userProfile(request, request.user.email)
