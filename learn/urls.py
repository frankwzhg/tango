from django.conf.urls import patterns, url
from learn import views
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging


urlpatterns = patterns('',
            url(r'^$', views.video, name='player'),
            )