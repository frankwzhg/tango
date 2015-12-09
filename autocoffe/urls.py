from django.conf.urls import patterns, url
from autocoffe import views
from django.views.generic import TemplateView


# Create a new class that redirects the user to the index page, if successful at logging


urlpatterns = patterns('',
            url(r'^$', views.relaxtime, name='relaxtime'),
            url(r'^test/$', TemplateView.as_view(template_name='autocoffee/test.html'), name='test'),
            url(r'auth_ip/$', views.auth_ipaddress, name='auth_ip'),
            url(r'ip_add/$', views.add_ipaddress, name='ip_add'),
            url(r'ip_delete/$', views.delete, name='ip_delete'),
            # url(r'send_dis/$', views.get_serial_value, name='send_dis'),
            )