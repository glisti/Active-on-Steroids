from django.conf.urls import patterns, include, url

from dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^event', views.event, name='event'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^about', views.about, name='about'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
)
