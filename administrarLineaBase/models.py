#encoding:utf-8
from django.db import models

from administrarFases.models import Fase
from autenticacion.models import Usuario


class LineaBase(models.Model):
    """
    *Modelo para la* ``Linea Base`` * en el cual se especifican los atributos propios de una Linea Base dentro del sistema:
        + **Fase**: Es el identificador de la fase a la cual pertenece la Linea Base.
        + **Fecha de Creación**: Es la fecha de creación de la Linea Base.
        + **Fecha de Modificacion**: Es la fecha de la última modificación en la Linea Base.
        + **Observaciones**: Es una lista de aspectos relevantes propios de la Linea Base.

    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.
    """

    fase = models.ForeignKey(Fase)
    fecha_creacion = models.DateField(auto_now_add=True, help_text='Fecha de creacion de la Linea Base', null=True)
    fecha_modificacion = models.DateField(help_text='Fecha de Modificacion de la Linea Base', null=True)
    observaciones = models.TextField(max_length=140, null=True)

    def __unicode__(self):
        return self.fecha_creacion


class SolicitudCambios(models.Model):
    """
    *Modelo para la* ``Solicitud de Cambios`` * en el cual se especifican los atributos propios de una Solicitud dentro del sistema:
        + **Usuario**: Usuario que ha emitido la Solicitud de Cambios.
        + **Fase**: Es la fase a la cual se encuentra ligada la Solicitud de Cambios.
        + **Motivo**: Es la justificación por la cual se ha emitido la Solicitud de Cambios.
        + **Fecha de Creación**: Es la fecha de emisión de la Solicitud de Cambio.
        + **Estado**: Es el estado que se encuentra la Solicitud. Esta puede estar "En votación", "Aceptada", "Rechazada" o "Cancelada"
        + **Costo**: Es el costo total de recursos necesarios para realizar los cambios solicitados.
        + **Tiempo**: Es el tiempo estimado necesario para culminar los cambios solicicatados.

    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.
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
    estado = models.CharField(max_length=3, choices=opciones_estado, default='VOT', help_text='Estado de la solicitud')
    costo = models.IntegerField(help_text='Costo total por realizar las modificaciones')
    tiempo = models.IntegerField(help_text='Tiempo total empleado en realizar las modificaciones')


    def __unicode__(self):
        return self.fecha_creacion


class Votacion(models.Model):
    """
    *Modelo para almacenar las votaciones expedidas sobre una solictud de cambios*
        + **Usuario**: Usuario que ha emitido un voto.
        + **Solicitud**: Identificador de la Solicitud que ha sido votada.
        + **Voto**: Es la decisión tomada sobre una solicitud por el Usuario. (Puede ser "A favor" o "En contra")
        + **Justificación**: Es la justificación de la decisión tomada por el Usuario.

    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.
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