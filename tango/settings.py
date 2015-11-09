"""
Django settings for tango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
ip_address = socket.gethostbyname(socket.gethostname())
if ip_address[8:11] != '199':
    host = 'frankub.frankdata.com.cn'
else:
    host = 'frankr.jios.org'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '52x+upycj=-niyuw*nbw4xf(690=x+u5pn2i2$(#mgz8ba#%*v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #'rango.templatertags.rango_extras',
    'rango',
    'learn',
    'autocoffe',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tango.urls'

WSGI_APPLICATION = 'tango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tango',
        'USER': 'root',
        'PASSWORD': 'Dadi4747',
        'HOST': host,
        'PORT': 3306,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (STATIC_PATH, )

# add templates folder

TEMPLATE_DIRS = (TEMPLATE_PATH,)


#add media URL

MEDIA_URL = '/media/'

# add password hashers

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

LOGIN_URL = '/rango/login/'

# configure cookie session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600

# blowing is some configration for user registration
REGISTRATION_OPEN = True  # if True, user can register
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation windows; you may, of course, use a different value
REGISTRATION_AUTO_LOGIN = True # If True,  the user will be automatically logged in
LOGIN_REDIRECT_URL = '/rango/' #The page you want users to arrive at after they successful log in
# LOGIN_URL = '/accounts/login/' #he page users are directed to if they are not logged in,
                     # and are trying to access pages requiring authentication

SITE_ID = 1

# mail server configure
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.live.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'frankwzhg@hotmail.com'
EMAIL_HOST_PASSWORD = 'Frank009216'
DEFAULT_FROM_EMAIL = 'frankwzhg@hotmail.com'
SERVER_EMAIL = 'frankwzhg@hotmail.com'