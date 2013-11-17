from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login

from profiles.models import Profile
from profiles.forms import RegistrationForm, LoginForm, EditForm

@login_required
def profile(request):
    # user is submitting a change to their profile
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            race_type = form.cleaned_data['race_type']
            profile = Profile.objects.get(user=request.user)
            profile.race_type = race_type
            profile.save()
            return HttpResponseRedirect('/profile')
    # the user is just viewing the profile
    else:
        profile = Profile.objects.get(user=request.user)
        # user does not exist
        if profile == None:
            pass
        race_type = profile.race_type
        form = EditForm(initial={'race_type':race_type})
        context = {'form': form}
        return render(request,'profiles/profile.html',context)

def register(request):
    ''' Registration for new users and new profiles '''
    # if the user is already logged in, send them to their profile 
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    # form was submitted 
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username,password=password)
            user.save()
            race_type = form.cleaned_data['race_type']
            profile = Profile(user=user, race_type=race_type)
            profile.save()
            user = authenticate(username=username,password=password)
            auth_login(request,user)
            return HttpResponseRedirect('/profile/')
        # form was not valid
        else:
            context = {'form': form}
            return render(request,'profiles/register.html', context)
    # user is not submitting the form
    else:      
        form = RegistrationForm()
        context = { 'form': form }
        return render(request,'profiles/register.html', context)

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            profile = authenticate(username=username,password=password)
            if profile is not None:
                auth_login(request, profile)
                return HttpResponseRedirect('/profile/')
            else:
                context = {'form':form}
                return render(request,'profiles/login.html', context)
        else:
            context = {'form':form}
            return render(request,'profiles/login.html', context)
    else:
        # user is not submitting the form
        form = LoginForm()
        context = {'form':form}
        return render(request,'profiles/login.html', context)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')