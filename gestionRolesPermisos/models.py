#encoding=utf-8
from django.db import models
from administrarFases.models import Fase
from administrarProyectos.models import Proyecto
from autenticacion.models import Usuario


class Permiso(models.Model):
    """
    Modelo que implementa la estructura basica de los permisos a ser provistos por el sistema
    """
    code = models.CharField('code', max_length=20)
    nombre = models.CharField('nombre', max_length=50)
    descripcion = models.CharField('descripción', max_length=100)

    class Meta:
        verbose_name = 'permiso'
        verbose_name_plural = 'permisos'

    def __unicode__(self):
        return self.nombre


class ROL_FASE(models.Model):
    fase = models.ForeignKey(Fase, blank=True)
    perm_list = models.ManyToManyField(Permiso, blank=True)

    def __unicode__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField('nombre', max_length=50)
    proyecto = models.ForeignKey(Proyecto, blank=True)
    descripcion = models.CharField('descripción', max_length=100)
    permisos = models.ManyToManyField(ROL_FASE)

    usuarios = models.ManyToManyField(Usuario,
        related_name="user_set", related_query_name="user")

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        unique_together = (('proyecto', 'nombre'),)

    def __unicode__(self):
        return self.nombre