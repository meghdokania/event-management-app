from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from . import models

CustomUser = get_user_model()

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'email','institute', 'year', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class PasswordResetForm(forms.Form):
    error_messages = {
        'email_error': _('User does not exists'),
    }
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError(
                self.error_messages['email_error'],
                code='email_error',
            )
        return email


class PasswordUpdateForm(forms.Form):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2
    
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user 


class UserUpdateForm(forms.Form):
    error_messages = {
        'name_error': _('Length of name must be greater than zero'),
        'password_mismatch': _('The two password fields didn’t match.'),
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    name = forms.CharField(label=_("Name"), max_length=255)
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) == 0:
            raise ValidationError(
                self.error_messages['name_error'],
                code='name_error',
            )
        return name

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        # print('hello sir')
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        name = self.cleaned_data['name']
        self.user.set_password(password)
        self.user.name = name
        if commit:
            self.user.save()
        return self.user   
