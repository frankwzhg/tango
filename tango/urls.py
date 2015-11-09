from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from rango import views
from django.conf.urls.static import static
import registration
from django.views.generic import TemplateView
class MyregistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    # url(r'^$',  views.default, name='default'),
    url(r'^$', TemplateView.as_view(template_name='rango/index.html'), name='default'),
    # url(r'^$', TemplateView.as_view(template_name='rango/registration_success.html'), name='registrate_success'),
    url(r'^accounts/register/$', MyregistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^learn/', include('learn.urls')),
    url(r'coffeebreak/', include('autocoffe.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root':settings.MEDIA_ROOT}),
        )