#encoding:utf-8
from django.db import models
from administrarProyectos.models import Proyecto


class Fase(models.Model):
    """
    *Modelo para la clase proyecto, en el cual se encuentras todos los atributos de una fase:*
        + *Codigo*: Identificador Único dentro del Sistema
        + *Nombre*: Nombre de la fase
        + *Descripción*: Breve reseña del proyecto
        + *Estado*: Los estados posibles del Proyecto. Por default: PEN(Pendiente)
        + *Proyecto*: Instancia del proyecto a la cual pertenece la fase

    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.

    """
    opciones_estado = (
        ('PEN', 'Pendiente'),
        ('PAU', 'Pausado'),
        ('DES', 'Desarrollo'),
        ('FIN', 'Finalizado'),
        ('REV', 'En revision'), )

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='PEN', help_text='Estado de la Fase')
    proyecto = models.ForeignKey(Proyecto)
    nro_orden = models.IntegerField(help_text='Nurmero de orden de ejecuccion de la fase')

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'fase'
        verbose_name_plural = 'fases'
        unique_together = (('proyecto', 'nombre'),)
        permissions = (
            ('crear_Item', 'Puede crear items'),
            ('modificar_Item', 'Puede modificar items'),
            ('dar_de_baja_Item', 'Puede dar de baja items'),
            ('restaurar_Item', 'Puede restaurar items'),
            ('revertir_Item', 'Puede revertir items'),
            ('consultar_Item', 'Puede consultar items'),
            ('consultar_Fase', 'Puede consultar fases'),
            ('consultar_Tipo_Item', 'Puede consultar tipos de item'),
            ('consultar_Lineas_Base', 'Puede consultar lineas base'),
            ('crear_Solicitud_Cambio', 'Puede crear solicitudes de cambio'),
            ('crear_Linea_Base', 'Puede crear lineas base'),
        )
