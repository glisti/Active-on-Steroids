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

    _events = info_recommender(profile.state, str(profile.zipcode), attrs)
    events = [v for k,v in _events.iteritems()]
    
    request.session['events'] = events
    context = { 'events': events }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def event(request, event_id):
    eid = int(event_id)
    event = request.session['events'][eid]
    events = [e for idx, e in enumerate(request.session['events']) if idx != eid]
    context = { 'event': event, 'events': events}
    return render(request, 'dashboard/event.html', context)

@login_required
def about(request):
    return render(request, 'dashboard/about.html')