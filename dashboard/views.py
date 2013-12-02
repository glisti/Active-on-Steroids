from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from profiles.models import Profile 
from backend.util import info_recommender

@login_required
def home(request):

    profile = Profile.objects.get(user=request.user)

    attrs = ""

    if profile.one_k == True:
        attrs += "1k "
    if profile.five_k == True:
        attrs += '5k '
    if profile.ten_k == True:
        attrs += '10k '
    if profile.one_mile == True:
        attrs += '1 mile '
    if profile.five_mile == True:
        attrs += '5 mile '
    if profile.ten_mile == True:
        attrs += '10 mile '
    if profile.half_marathon == True:
        attrs += 'half marathon '
    if profile.full_marathon == True:
        attrs += 'marathon '
    if profile.ultra_marathon == True:
        attrs += 'ultra marathon '
    if profile.trail_run == True:
        attrs += 'trail run '
    if profile.cross_country == True:
        attrs += 'cross country '
    if profile.short_distance == True:
        attrs += 'short distance '
    if profile.long_distance == True:
        attrs += 'long distance '
    if profile.competitive == True:
        attrs += 'competitive '

    es = info_recommender(profile.state, str(profile.zipcode), attrs)

    events = [{"endDate": "2013-12-08T13:00:00", "description": "Join us at 7:00am on December 8, 2013 for year 3 of what is currently the highest rated marathon in the state of Texas (marathonguide.com). You?ll have the opportunity to explore the Bryan/College Station community as well as experience the Aggie spirit while you run throughout the Texas A&M campus. ", "title": "Scott & White BCS Marathon + Half Marathon", "zipCode": "77840", "phone": "9795748879", "addressLine2": "College Station", "location": "Wolf Pen Creek Park", "homePage": "http://www.bcsmarathon.com"}, {"endDate": "2013-12-07T14:00:00", "description": "All races start at Wolf Pen Creek, next to Post Oak Mall, and the entry fee is $12 per child. Start times for the Kid?s Marathon are as follows. We will start on time, so please plan to arrive early to your child?s race start.8:30   3-4 year olds (parents required to run with their children)9:00   5-6 year olds9:30   7-8 year olds10:00   9-10 year olds10:15   11-12 year olds", "title": "Scott & White Health Plan BCS Kid's Marathon", "zipCode": "77840", "phone": "9795748879", "addressLine2": "College Station", "location": "Wolf Pen Creek Park", "homePage": "http://bcsmarathon.com/kids/"}]
    print type(es)

    for k,v in es:
        events.append(v)

    print events

    context = { 'events': events }

    return render(request, 'dashboard/dashboard.html', context)

	

@login_required
def event(request):
    return render(request, 'dashboard/event.html')

@login_required
def about(request):
    return render(request, 'dashboard/about.html')