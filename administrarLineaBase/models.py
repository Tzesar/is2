#encoding:utf-8
from django.db import models

from administrarFases.models import Fase
from autenticacion.models import Usuario


class LineaBase(models.Model):
    """
    *Este es el modelo para la Linea Base. En el cual se encuentras todos los atributos de una Linea Base:*
        + *Codigo*: Identificador Único dentro del Sistema
        + *Fase*: Identificador de la fase
        + *Fecha de Creacion*: Fecha de creación de la Linea Base
        + *Fecha de Modificacion*: Fecha de modificación de la Linea Base
        + *Observaciones*: Notas importantes con respecto a los ítems que pertenecen a la Linea Base.

    """

    fase = models.ForeignKey(Fase)
    fecha_creacion = models.DateField(auto_now_add=True, help_text='Fecha de creacion de la Linea Base', null=True)
    fecha_modificacion = models.DateField(help_text='Fecha de Modificacion de la Linea Base', null=True)
    observaciones = models.TextField(max_length=140, null=True)


    def __unicode__(self):
        return self.fecha_creacion


class SolicitudCambios(models.Model):
    """
    *Modelo para la solicitud de cambios. En el cual se encuentras todos los atributos de una Solicitud:*
        + *Codigo*: Identificador Único dentro del Sistema
        + *Usuario*: Identificador del Usuario quien ha expedido la solicitud.
        + *Fase*: Identificador de la Fase a la cual se encuentra vinculada la Solicitud.
        + *Motivo*: Justificación de los cambios solicitados.
        + *Fecha de Creacion*: Fecha de creación de la Solicitud.
        + *Estado*: Estado en que se encuentra la Solicitud.
        + *Costo*: Costo estimado de las modificaciones de solicitadas.
        + *Tiempo*: Tiempo estimado de las modificaciones de solicitadas.

    """

    opciones_estado = (
        ('VOT', 'En votación'),
        ('ACP', 'Aceptado'),
        ('RCH', 'Rechazado'),
        ('CAN', 'Cancelado'),
        ('EJC', 'Ejecutado'), )

    usuario = models.ForeignKey(Usuario)
    fase = models.ForeignKey(Fase)
    motivo = models.TextField(null=False, blank=False, help_text='Favor introducir los motivos para realizar los '
                                                                   'cambios en forma clara y breve')
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text='Fecha de expedición de la solicitud de cambios',
                                          null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='VOT', help_text='Estado de la solicitud')
    costo = models.IntegerField(help_text='Costo total por realizar las modificaciones')
    tiempo = models.IntegerField(help_text='Tiempo total empleado en realizar las modificaciones')

    def __unicode__(self):
        return self.fase.nombre + '-' +self.usuario.username

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural = 'solicitudes'


class Votacion(models.Model):
    """
    *Modelo para almacenar las votaciones expedidas sobre una solictud de cambios.*
    * En el cual se encuentras todos los atributos de una Linea Base:*
        + *Codigo*: Identificador Único dentro del Sistema.
        + *Usuario*: Identificador del Usuario quien ha expedido el voto.
        + *Solicitud*: Identificador de la Solicitud de Cambios.
        + *Voto*: Voto a favor/contra de la Solicitud.
        + *Justificación*: Explicación de la postura tomada con respecto a la Solicitud de Cambios.
    """

    opciones_voto = (
        ('GOOD', 'A favor'),
        ('EVIL', 'En contra'), )

    usuario = models.ForeignKey(Usuario)
    solicitud = models.ForeignKey(SolicitudCambios)
    voto = models.CharField(max_length=4, choices=opciones_voto, help_text='Estado del item')
    justificacion = models.TextField(max_length=240, help_text='Favor justificar su decisión')

    def __unicode__(self):
        return self.usuario