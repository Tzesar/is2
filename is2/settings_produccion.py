from settings import *


DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.zarpm.org', '0.0.0.0', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zarbd',
        'USER': 'zar',
        'PASSWORD': 'zar',
        'HOST': '',
        'PORT': '',
    }
}

STATIC_URL = 'http://static-zarpm.org/'

# STATIC_ROOT is the directory where the collectstatic will put all the static files collected
# from the STATICFILES_DIRS
STATIC_ROOT = '/var/www/staticZarPm'