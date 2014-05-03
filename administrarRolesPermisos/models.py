#encoding=utf-8
from django.db import models
from administrarFases.models import Fase
from administrarProyectos.models import Proyecto
from autenticacion.models import Usuario


class Permiso(models.Model):
    """
    *Modelo que implementa la estructura basica de la clase *``Permiso``*
    para los usuarios cuyo premiso no dependa de la fase del proyecto en la cual trabaja*
        + *code*: Identificador Único del permiso en el sistema
        + *nombre*: Nombre del Permiso a ser mostrado
        + *descripcion*: Breve descripción de las actividades que permite el permiso asociado

    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.
    """
    code = models.CharField('code', max_length=20)
    nombre = models.CharField('nombre', max_length=50)
    descripcion = models.CharField('descripción', max_length=100)

    class Meta:
        verbose_name = 'permisoGeneral'
        verbose_name_plural = 'permisosGenerales'

    def __unicode__(self):
        return self.nombre


class PermisoFase(models.Model):
    """
    *Modelo que implementa la estructura basica de la clase * ``Permiso`` * a ser provistos por el sistema.
    para aquellos usuarios cuyo rol se aplique solamente a ciertas fases de un proyecto.*
        + *code*:
        + *nombre*:
        + *descripcion*:
    """
    code = models.CharField('code', max_length=50)
    nombre = models.CharField('nombre', max_length=50)
    descripcion = models.CharField('descripción', max_length=200)
    fase = models.ForeignKey(Fase)

    class Meta:
        verbose_name = 'permisoFase'
        verbose_name_plural = 'permisosFase'

    def __unicode__(self):
        return self.nombre


class RolGeneral(models.Model):
    nombre = models.CharField('nombre', max_length=50)
    proyecto = models.ForeignKey(Proyecto, null=True)
    descripcion = models.CharField('descripción', max_length=100)
    permisos = models.ManyToManyField(Permiso)

    roles_usuarios = models.ManyToManyField(Usuario,
        related_name="usuarios_adm_lider_mcomite", related_query_name="user")

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        unique_together = (('proyecto', 'nombre'),)

    def __unicode__(self):
        return self.nombre


class RolFase(models.Model):
    nombre = models.CharField('nombre', max_length=50)
    proyecto = models.ForeignKey(Proyecto)
    descripcion = models.CharField('descripción', max_length=100)
    permisos = models.ManyToManyField(PermisoFase)

    roles_usuarios = models.ManyToManyField(Usuario,
        related_name="usuarios_participantes", related_query_name="user")

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        unique_together = (('proyecto', 'nombre'),)

    def __unicode__(self):
        return self.nombre