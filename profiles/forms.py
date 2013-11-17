from django import forms
from django.contrib.auth.models import User

from profiles.models import Profile

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'required':'required'
    }))
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'required':'required'
    }))
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'required':'required'
    }))
    race_type = forms.CharField(
        label='Race Preference', 
        widget=forms.Select(
            choices=Profile.RACE_TYPES,
            attrs = {
                'class': 'form-control',
                'required':'required'
    }))

    class Meta:
        model = Profile
        exclude = ('user',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('That username is already taken, select another')

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('The passwords did not match, try again')
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Username',
                'required':'required', 'autofocus':'autofocus'
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control','placeholder':'Password',
                'required':'required'})
    )

class EditForm(forms.ModelForm):
    race_type = forms.CharField(
        label='Race Preference', 
        widget=forms.Select(
            choices=Profile.RACE_TYPES,
            attrs = {
                'class': 'form-control',
                'required':'required'
    }))

    class Meta:
        model = Profile
        exclude = ('user',)
    
