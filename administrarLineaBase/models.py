#encoding:utf-8
from django.db import models

from administrarFases.models import Fase
from autenticacion.models import Usuario


class LineaBase(models.Model):
    """
    Este es el modelo para la Linea Base
    """

    fase = models.ForeignKey(Fase)
    fecha_creacion = models.DateField(auto_now_add=True, help_text='Fecha de creacion de la Linea Base', null=True)
    fecha_modificacion = models.DateField(help_text='Fecha de Modificacion de la Linea Base', null=True)
    observaciones = models.TextField(max_length=140, null=True)

    def __unicode__(self):
        return self.fecha_creacion


class SolicitudCambios(models.Model):
    """
    Modelo para la solicitud de cambios
    """

    opciones_estado = (
        ('VOT', 'En votación'),
        ('ACP', 'Aceptado'),
        ('RCH', 'Rechazado'),
        ('CAN', 'Cancelado'), )

    usuario = models.ForeignKey(Usuario)
    fase = models.ForeignKey(Fase)
    motivo = models.TextField(null=False, blank=False, help_text='Favor introducir los motivos para realizar los '
                                                                   'cambios en forma clara y breve')
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text='Fecha de expedición de la solicitud de cambios',
                                          null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='VOT', help_text='Estado del item')
    costo = models.IntegerField(help_text='Costo total por realizar las modificaciones')
    tiempo = models.IntegerField(help_text='Tiempo total empleado en realizar las modificaciones')


    def __unicode__(self):
        return self.fecha_creacion