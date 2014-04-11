from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """ Extension de la clase User de Django. Agrega los campos telefono y otros.
    """
    telefono = models.CharField(max_length=20, blank=True)
