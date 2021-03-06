#encoding:utf-8
"""

*Archivo de configuración para el proyecto* ``ZARpm``

*Aquí se puede observar todas las configuraciones utilizadas para el desarrollo del proyecto.*

Configuraciones Generales:
    + Gestor de Base de Datos: Postgresql 9.1
    + Gestor de Documentación: Sphinx
    + Framework: Django 1.6
    + Entorno de Desarrollo: Pycharm 3.1.1
    + Servidor de Correos: smtp.gmail.com

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-3%ft-np-c7t7!d0@mwiy$n^^x2aor=&%2*wj133pp)x%fecnc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0"]

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_tables2',
    'floppyforms',
    'guardian',
    'reversion',
    'zar',
    'autenticacion',
    'administrarUsuarios',
    'administrarProyectos',
    'administrarFases',
    'administrarRolesPermisos',
    'administrarTipoItem',
    'administrarItems',
    'administrarLineaBase',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'is2.urls'

WSGI_APPLICATION = 'is2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

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

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-PY'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "is2/", "static/"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

# Establece el modelo de usuario que se usa
AUTH_USER_MODEL = "autenticacion.Usuario"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = '/main/'

# Configuracion necesaria para Django Guardian
ANONYMOUS_USER_ID = -1
GUARDIAN_RENDER_403 = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'is2/', 'static/media')
MEDIA_URL = '/media/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admitres03@gmail.com'
EMAIL_HOST_PASSWORD = 'administracion3'
DEFAULT_FROM_EMAIL = 'admitres03@gmail.com'

DATE_INPUT_FORMATS = (
    '%m/%d/%Y', '%m/%d/%y',             # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': "[%(asctime)s] %(levelname)s %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'proyecto': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'Proyectos.log',
#             'formatter': 'verbose'
#         },
#         'usuario': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'Usuarios.log',
#             'formatter': 'verbose'
#         },
#         'fase': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'Fases.log',
#             'formatter': 'verbose'
#         },
#         'rol': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'Roles.log',
#             'formatter': 'verbose'
#         },
#         'tipo_item': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'Tipo_Items.log',
#             'formatter': 'verbose'
#         },
#         'item': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'Items.log',
#             'formatter': 'verbose'
#         },
#         'linea_base': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'Linea_base.log',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'administrarProyectos': {
#             'handlers': ['proyecto'],
#             'level': 'INFO',
#         },
#         'administrarUsuarios': {
#             'handlers': ['usuario'],
#             'level': 'INFO',
#         },
#         'administrarFases': {
#             'handlers': ['fase'],
#             'level': 'INFO',
#         },
#         'administrarTipoItem': {
#             'handlers': ['tipo_item'],
#             'level': 'INFO',DATE_INPUT_FORMATS
#         },
#         'administrarRolesPermisos': {
#             'handlers': ['rol'],
#             'level': 'INFO',
#         },
#         'administrarItems': {
#             'handlers': ['item'],
#             'level': 'INFO',
#         },
#         'administrarLineaBase': {
#             'handlers': ['linea_base'],
#             'level': 'INFO',
#         },
#     }
# }
