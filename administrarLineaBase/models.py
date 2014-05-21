#encoding:utf-8
from django.db import models
from administrarFases.models import Fase


class LineaBase(models.Model):
    """
    Este es el modelo para la Linea Base
    """

    fase = models.ForeignKey(Fase)
    fecha_creacion = models.DateField(auto_now_add=True, help_text='Fecha de creacion de la Linea Base', null=True)
    fecha_modificacion = models.DateField(help_text='Fecha de Modificacion de la Linea Base', null=True)
    observaciones = models.TextField(max_length=140, null=True)


    def retornaID(self):
        return self.id

    def __unicode__(self):
        return self.fecha_creacion