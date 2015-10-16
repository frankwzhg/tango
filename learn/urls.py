from django.conf.urls import patterns, url
from learn import views
from django.views.generic import TemplateView


# Create a new class that redirects the user to the index page, if successful at logging


urlpatterns = patterns('',
            url(r'^videodata/$', views.video, name='video_data'),
            url(r'^videoupload/$', views.video_upload_view, name='video_upload'),
            url(r'^$', TemplateView.as_view(template_name='learn/player.html'), name='video_player'),
            )