from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
	return render(request, 'dashboard/dashboard.html')

@login_required
def about(request):
    return render(request, 'dashboard/about.html')

@login_required
def event(request):
    return render(request, 'dashboard/event.html')

# def profile(request):
#     return render(request, 'dashboard/profile.html')

# def login(request):
#   return render(request, 'dashboard/login.html')

# def logout(request):
#   return render(request, 'dashboard/logout.html')
