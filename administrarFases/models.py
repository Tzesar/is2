#encoding:utf-8
from django.db import models
from administrarProyectos.models import Proyecto


class Fase(models.Model):
    """
    Modelo para la clase proyecto, en el cual se encuentras todos los atributos de una fase:
        + Codigo: Identificador Único dentro del Sistema
        + Nombre: Nombre de la fase
        + Descripción: Breve reseña del proyecto
        + Estado: Los estados posibles del Proyecto. Por default: PEN(Pendiente)
    """
    opciones_estado = (
        ('PEN', 'Pendiente'),
        ('PAU', 'Pausado'),
        ('DES', 'Desarrollo'),
        ('FIN', 'Finalizado'),
        ('REV', 'En revision'), )

    codigo = models.CharField(max_length=2, default='PH')
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='PEN', help_text='Estado de la Fase')
    proyecto = models.ForeignKey(Proyecto)
    #lista de tipo de ítems

    def __unicode__(self):
        return self.nombre