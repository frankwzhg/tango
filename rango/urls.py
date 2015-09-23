from django.conf.urls import patterns, url
from rango import views
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging


urlpatterns = patterns('',
            url(r'^$', views.index, name='index'),
            url(r'^about/$', views.about, name='about'),
            url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
            url(r'^add_category/$', views.add_category, name='add_category'),
            url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
            url(r'^goto/$', views.track_url, name='goto'),
            url(r'^user_profile_update/$', views.user_profile_update, name='user_profile_update'),
            url(r'^restricted/$', views.restricted, name='restricted'),
            url(r'^user_profile_add/$', views.user_profile_add, name='user_profile_add'),
            url(r'^login/$', views.user_login, name='user_login'),
            url(r'^registrate/$', views.user_registration, name='user_registrate'),
            url(r'logout/$', views.user_logout, name='user_logout'),
            url(r'reset_password/$', views.reset_password, name='reset_password'),
            url(r'change_pic', views.changepic, name='change_pic'),
            url(r'change_password', views.changepasswd, name='change_password'),
            )