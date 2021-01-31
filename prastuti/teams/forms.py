from django import forms
from django.core.exceptions import ValidationError
from .models import Team
from django.core import validators
from users import views as userViews 

class TeamForm(forms.ModelForm):
    pass
    
    # def clean_team_member(self):
    #     team_member = self.cleaned_data['team_member']
    #     event = self.cleaned_data['team_event']
    #     for member in team_member:
    #         if userViews.isRegisteredForEvent(member,):
    #             raise ValidationError(str(member) + " has already registered for event " + str(event))