from django.shortcuts import render

def login(request):
	return render(request, 'dashboard/login.html')

def logout(request):
	return render(request, 'dashboard/logout.html')

def home(request):
	return render(request, 'dashboard/dashboard.html')

def about(request):
    return render(request, 'dashboard/about.html')

def event(request):
    return render(request, 'dashboard/event.html')

def profile(request):
    return render(request, 'dashboard/profile.html')