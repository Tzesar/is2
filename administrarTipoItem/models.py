#encoding:utf-8
from django.db import models
from administrarFases.models import Fase


class TipoItem(models.Model):
    """
    *Modelo para la representación de la entidad* ``Tipo de ítem`` *asociada a una fase* :
        + **Nombre**: Nombre del tipo de ítem
        + **Fase**: Identificador de la fase a la cual se encuentra asociada
        + **Descripción**: Breve descripción del propósito del tipo de ítem

    :param args: Argumentos para el modelo base ``Model``.
    :param kwargs: Keyword Arguments para la función ``Model``.

    """

    nombre = models.CharField(max_length=100)
    fase = models.ForeignKey(Fase)
    descripcion = models.TextField(max_length=140)

    class Meta:
        verbose_name = 'TipoItem'
        verbose_name_plural = 'TipoItems'
        unique_together = (('fase', 'nombre'),)

    def __unicode__(self):
        return self.nombre


class Atributo(models.Model):
    """
    *Modelo para representar a los* ``Atributos``  de un ``Tipo de Ítem`` :
        + **Nombre**: Nombre descriptivo para el atributo
        + **Tipo**: Tipo de dato al que corresponde el atributo
        + **Tipo de Ítem**: Tipo de ítem al cual se encuentra asociado el atributo
        + **Descripción**: Breve descripción del propósito del atributo

    :param args: Argumentos para el modelo base ``Model``.
    :param kwargs: Keyword Arguments para la función ``Model``.

    """

    opciones_tipo = (
        ('TXT', 'Texto Largo'),
        ('STR', 'Texto Corto'),
        ('NUM', 'Numero'),
        ('FIL', 'Archivo Externo'),
        ('IMG', 'Imagen'), )

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=opciones_tipo, help_text='Tipo', default='TXT')
    tipoDeItem = models.ForeignKey(TipoItem)
    descripcion = models.TextField(max_length=140)

    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'
        unique_together = (('tipoDeItem', 'nombre'),)

    def __unicode__(self):
        return self.nombre
