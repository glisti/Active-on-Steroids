from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^profile/', include('profiles.urls', namespace='profile')),
    url(r'^', include('dashboard.urls', namespace='dashboard')),
    url(r'^admin/', include(admin.site.urls)),
)
