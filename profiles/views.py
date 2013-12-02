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
            print "> FORM IS VALID"
            profile = Profile.objects.get(user=request.user)
            profile.age            = form.cleaned_data['age']
            profile.zipcode        = form.cleaned_data['zipcode']
            profile.state          = form.cleaned_data['state']
            profile.gender         = form.cleaned_data['gender']
            profile.one_k          = form.cleaned_data['one_k']
            profile.five_k         = form.cleaned_data['five_k']
            profile.ten_k          = form.cleaned_data['ten_k']
            profile.one_mile       = form.cleaned_data['one_mile']
            profile.five_mile      = form.cleaned_data['five_mile']
            profile.ten_mile       = form.cleaned_data['ten_mile']
            profile.half_marathon  = form.cleaned_data['half_marathon']
            profile.full_marathon  = form.cleaned_data['full_marathon']
            profile.ultra_marathon = form.cleaned_data['ultra_marathon']
            profile.trail_run      = form.cleaned_data['trail_run']
            profile.cross_country  = form.cleaned_data['cross_country']
            profile.short_distance = form.cleaned_data['short_distance']
            profile.long_distance  = form.cleaned_data['long_distance']
            profile.competitive    = form.cleaned_data['competitive']
            profile.save()
            return HttpResponseRedirect('/profile')
        else:
            print form.errors
    # the user is just viewing the profile
    else:
        profile = Profile.objects.get(user=request.user)
        # user does not exist
        if profile == None:
            print "> PROFILE IS NONE"
        form = EditForm(initial={
            'age':profile.age,
            'zipcode':profile.zipcode,
            'state':profile.state,
            'gender':profile.gender,
            'one_k':profile.one_k,
            'five_k':profile.five_k,
            'ten_k':profile.ten_k,
            'one_mile':profile.one_mile,
            'five_mile':profile.five_mile,
            'ten_mile':profile.ten_mile,
            'half_marathon':profile.half_marathon,
            'full_marathon':profile.full_marathon,
            'ultra_marathon':profile.ultra_marathon,
            'trail_run':profile.trail_run,
            'cross_country':profile.cross_country,
            'short_distance':profile.short_distance,
            'long_distance':profile.long_distance,
            'competitive':profile.competitive})
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
            age = form.cleaned_data['age']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            gender = form.cleaned_data['gender']
            one_k = form.cleaned_data['one_k']
            five_k = form.cleaned_data['five_k']
            ten_k = form.cleaned_data['ten_k']
            one_mile = form.cleaned_data['one_mile']
            five_mile = form.cleaned_data['five_mile']
            ten_mile = form.cleaned_data['ten_mile']
            half_marathon = form.cleaned_data['half_marathon']
            full_marathon = form.cleaned_data['full_marathon']
            ultra_marathon = form.cleaned_data['ultra_marathon']
            trail_run = form.cleaned_data['trail_run']
            cross_country = form.cleaned_data['cross_country']
            short_distance = form.cleaned_data['short_distance']
            long_distance = form.cleaned_data['long_distance']
            competitive = form.cleaned_data['competitive']
            profile = Profile(
                user=user, age=age,zipcode=zipcode,state=state,
                gender=gender,one_k=one_k,five_k=five_k,
                ten_k=ten_k,one_mile=one_mile,five_mile=five_mile,
                ten_mile=ten_mile,half_marathon=half_marathon,
                full_marathon=full_marathon,ultra_marathon=ultra_marathon,
                trail_run=trail_run,cross_country=cross_country,
                short_distance=short_distance,long_distance=long_distance,
                competitive=competitive)
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