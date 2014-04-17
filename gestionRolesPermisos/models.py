#encoding=utf-8
from django.db import models


class Permiso(models.Model):
    code = models.CharField('code', max_length=20)
    nombre = models.CharField('nombre', max_length=50)
    descripcion = models.CharField('descripción', max_length=100)

    class Meta:
        verbose_name = 'permiso'
        verbose_name_plural = 'permisos'


class ROL_FASE(models.Model):
    #fase = models.ManyToManyField(Fase, blank=True)
    perm_list = models.ManyToManyField(Permiso, blank=True)


class Rol(models.Model):
    nombre = models.CharField('nombre', max_length=50)
    #proyecto = models.ForeignKey(Proyecto)
    descripcion = models.CharField('descripción', max_length=100)
    permisos = models.ManyToManyField(ROL_FASE)

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        #unique_together = (('proyecto', 'nombre'),)