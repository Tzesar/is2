#encoding:utf-8
from django.db import models
from administrarFases.models import Fase


class TipoItem(models.Model):
    """
    Modelo para la clase fase, en el cual se encuentras todos los atributos de un tipo de ítem:
        + Codigo: Identificador Único dentro del Sistema
        + Nombre: Nombre del tipo de ítem
        + perteneceFase: Identificador de la fase a la cual se encuentra asociada
    """

    codigo = models.CharField(max_length=2, default='TI')
    nombre = models.CharField(max_length=100)
    pertenece_fase = models.ForeignKey(Fase)

    class Meta:
        verbose_name = 'TipoItem'
        verbose_name_plural = 'TipoItems'
        unique_together = (('pertenece_fase', 'nombre'),)

    def __unicode__(self):
        return self.nombre

"""
class AtributosItemInteger(models.Model):
    Modelo para la clase fase, en el cual se encuentras todos los atributos de un tipo de ítem:
        + Codigo: Identificador Único dentro del Sistema
        + Nombre: Nombre del tipo de ítem
        + Valor: Valor asociado al atributo del tipo Integer
        + perteneceFase: Identificador de la fase a la cual se encuentra asociada

    codigo = models.CharField(max_length=2, default='AT')
    nombre = models.CharField(max_length=100, help_text='Nombre del Atributo')
    valor = models.IntegerField(help_text='Valor del Atributo')
    perteneceTipoItem = models.ForeignKey(TipoItem)


class AtributosItemChar(models.Model):

    Modelo para la clase fase, en el cual se encuentras todos los atributos de un tipo de ítem:
        + Codigo: Identificador Único dentro del Sistema
        + Nombre: Nombre del tipo de ítem
        + Valor: Valor asociado al atributo del tipo Char
        + perteneceFase: Identificador de la fase a la cual se encuentra asociada


    codigo = models.CharField(max_length=2, default='AT')
    nombre = models.CharField(max_length=100, help_text='Nombre del Atributo')
    valor = models.CharField(max_length=140, help_text='Valor del Atributo')
    perteneceTipoItem = models.ForeignKey(TipoItem)


class AtributosItemFile(models.Model):

    Modelo para la clase fase, en el cual se encuentras todos los atributos de un tipo de ítem:
        + Codigo: Identificador Único dentro del Sistema
        + Nombre: Nombre del tipo de ítem
        + Valor: Valor asociado al atributo del tipo File
        + perteneceFase: Identificador de la fase a la cual se encuentra asociada


    codigo = models.CharField(max_length=2, default='AT')
    nombre = models.CharField(max_length=100, help_text='Nombre del Atributo')
    valor = models.FileField(verbose_name='Añada el nuevo archivo',upload_to=)
    perteneceTipoItem = models.ForeignKey(TipoItem)
"""