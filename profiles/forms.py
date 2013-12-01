from django import forms
from django.contrib.auth.models import User

from profiles.models import Profile

ATTRS = {
    'class': 'form-control',
    'required':'required'
}

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs=ATTRS
        )
    )
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(
            attrs = ATTRS
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs = ATTRS
        )
    )
    gender = forms.CharField(
        label='Gender',
        required=True,
        widget=forms.RadioSelect(
            choices=Profile.GENDERS
        )
    )
    age = forms.IntegerField(
        label='Age',
        min_value=5,
        max_value=120,
        widget=forms.NumberInput(
            attrs=ATTRS
        )
    )
    zipcode = forms.IntegerField(
        label='Zip Code',
        widget=forms.NumberInput(
            attrs=ATTRS
        )
    )
    one_k = forms.BooleanField(
        label='1k',
        required=False
    )
    five_k = forms.BooleanField(
        label='5k',
        required=False
    )
    ten_k = forms.BooleanField(
        label='10k',
        required=False
    )
    one_mile = forms.BooleanField(
        label='1 mile',
        required=False
    )
    five_mile = forms.BooleanField(
        label='5 mile',
        required=False
    )
    ten_mile = forms.BooleanField(
        label='10 mile',
        required=False
    )
    half_marathon = forms.BooleanField(
        label='Half Marathon',
        required=False
    )
    full_marathon = forms.BooleanField(
        label='Full Marathon',
        required=False
    )
    ultra_marathon = forms.BooleanField(
        label='Ultra Marathon',
        required=False
    )
    trail_run = forms.BooleanField(
        label='Trail Run',
        required=False
    )
    cross_country = forms.BooleanField(
        label='Cross Country',
        required=False
    )
    short_distance = forms.BooleanField(
        label='Short Distance',
        required=False
    )
    long_distance = forms.BooleanField(
        label='Long Distance',
        required=False
    )
    competitive = forms.BooleanField(
        label='Competitve',
        required=False
    )


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
    gender = forms.CharField(
        label='Gender',
        required=True,
        widget=forms.RadioSelect(
            choices=Profile.GENDERS
        )
    )
    age = forms.IntegerField(
        label='Age',
        min_value=5,
        max_value=120,
        widget=forms.NumberInput(
            attrs=ATTRS
        )
    )
    zipcode = forms.IntegerField(
        label='Zip Code',
        widget=forms.NumberInput(
            attrs=ATTRS
        )
    )
    one_k = forms.BooleanField(
        label='1k',
        required=False
    )
    five_k = forms.BooleanField(
        label='5k',
        required=False
    )
    ten_k = forms.BooleanField(
        label='10k',
        required=False
    )
    one_mile = forms.BooleanField(
        label='1 mile',
        required=False
    )
    five_mile = forms.BooleanField(
        label='5 mile',
        required=False
    )
    ten_mile = forms.BooleanField(
        label='10 mile',
        required=False
    )
    half_marathon = forms.BooleanField(
        label='Half Marathon',
        required=False
    )
    full_marathon = forms.BooleanField(
        label='Full Marathon',
        required=False
    )
    ultra_marathon = forms.BooleanField(
        label='Ultra Marathon',
        required=False
    )
    trail_run = forms.BooleanField(
        label='Trail Run',
        required=False
    )
    cross_country = forms.BooleanField(
        label='Cross Country',
        required=False
    )
    short_distance = forms.BooleanField(
        label='Short Distance',
        required=False
    )
    long_distance = forms.BooleanField(
        label='Long Distance',
        required=False
    )
    competitive = forms.BooleanField(
        label='Competitve',
        required=False
    )

    class Meta:
        model = Profile
        exclude = ('user',)
    
