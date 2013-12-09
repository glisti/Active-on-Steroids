from django.conf.urls import patterns, include, url

from dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^event/(?P<event_id>\d+)/$', views.event, name='event'),
    url(r'^about', views.about, name='about'),
)
