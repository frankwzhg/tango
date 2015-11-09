from django.conf.urls import patterns, url
from autocoffe import views
from django.views.generic import TemplateView


# Create a new class that redirects the user to the index page, if successful at logging


urlpatterns = patterns('',
            url(r'^$', views.relaxtime, name='relaxtime'),
            url(r'^test/$', TemplateView.as_view(template_name='autocoffee/test.html'), name='test'),
            )