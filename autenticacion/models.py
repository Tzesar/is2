#encoding=utf-8
import re
import warnings

from django.db import models

from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils import timezone
from django.core import validators

from django.contrib.auth.models import AbstractBaseUser, UserManager, SiteProfileNotAvailable, ImproperlyConfigured

class AbstractUser(AbstractBaseUser):
    """
    *Clase Abstracta que posse todas las funciones a ser implementadas por el modelo Usuario,*
    *sin los permisos de administrador. El cual tiene como base el modelo* ``AbstractBaseUser``.


    :param args: Argumentos para el modelo ``AbstractBaseUser``.
    :param kwargs: Keyword Arguments para el modelo ``AbstractBaseUser``.
    ::

        class Meta:
            verbose_name = 'user'
            verbose_name_plural = 'users'
            abstract = True

    """
    username = models.CharField('username', max_length=30, unique=True,
        help_text='Requerido: Como máximo 30 caracteres. Letras, números y '
                    'caracteres especiales @/./+/-/_',
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), 'Ingrese un nombre de usuario válido.', 'inválido')
        ])
    first_name = models.CharField('nombre', max_length=30, blank=True, default='Desco')
    last_name = models.CharField('apellido', max_length=30, blank=True, default='Nocido')
    email = models.EmailField('email', blank=True)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Retorna el nombre completo del usuario.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """"
        Retorna el primer nombre del usuario.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Envia un email al usuario.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Retorna el perfil del usuario.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
            DeprecationWarning, stacklevel=2)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache


class Usuario(AbstractUser):
    """
    *Extension de la clase User de Django. Extiende del modelo definido* ``AbstractUser``
    *Agrega los campos telefono y otros.*

    :param args: Argumentos para el modelo ``AbstractUser``.
    :param kwargs: Keyword Arguments para el modelo ``AbstractUser``.
    """
    telefono = models.CharField(max_length=20, blank=True)

    is_superuser = models.BooleanField('superuser status', default=False,
        help_text='Designates that this user has all permissions without '
                    'explicitly assigning them.')