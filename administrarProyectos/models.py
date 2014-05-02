#encoding:utf-8
from django.db import models
from autenticacion.models import Usuario


class Proyecto(models.Model):
    """
    *Modelo para la clase* ``Proyecto`` *, en el cual se encuentras todos los atributos de un proyecto:*
        + *Codigo*: Identificador Único dentro del Sistema
        + *Nombre*: Nombre del Proyecto
        + *Líder de Proyecto*: Usuario responsable del Proyecto
        + *Descripción*: Breve reseña del proyecto
        + *Fecha de Creación*: Fecha de creación del proyecto
        + *Fecha de Inicio*: Fecha de inicio del proyecto
        + *Fecha de Fin*: Fecha estimada de finalización del proyecto
        + *Estado*: Los estados posibles del Proyecto. Por default: PEN(Pendiente)
        + *Observaciones*: Notas relevantes acerca del proyecto

    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.
    """
    opciones_estado = (
        ('PEN', 'Pendiente'),
        ('ANU', 'Anulado'),
        ('ACT', 'Activo'),
        ('FIN', 'Finalizado'), )

    nombre = models.CharField(max_length=100, unique=True)
    lider_proyecto = models.ForeignKey(Usuario, related_name='Lider')
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    fecha_creacion = models.DateField(auto_now_add=True, help_text='Fecha de creacion del Proyecto', null=True)
    fecha_inicio = models.DateField(help_text='Fecha de inicio del Proyecto', null=True)
    fecha_fin = models.DateField(help_text='Fecha estimada de finalizacion', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='PEN', help_text='Estado del proyecto')
    observaciones = models.TextField(max_length=140, null=True)

    def __unicode__(self):
        return self.nombre

class UsuariosVinculadosProyectos(models.Model):
    """
    *Modelo para los usuarios vinculados a algún proyecto dentro del sistema.*
        + *Cod_Proyecto*: Identificador del proyecto al cual se encuentra vinculado el usuario
        + *Cod_Usuario*: Identificador del usuario que se encuentra vinculado a un proyecto
        + *Habilitado*: Define si el usuario se encuentra habilitado para realizar cambios en el proyecto

    *La unión entre un usuario y el proyecto debe ser única en el sistema.*

    ::

        class Meta:
            unique_together = (('cod_proyecto', 'cod_usuario'),)


    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.

    """
    cod_proyecto = models.ForeignKey(Proyecto)
    cod_usuario = models.ForeignKey(Usuario)
    habilitado = models.BooleanField('active', default=True,
        help_text='Designa si este usuario esta habilitado o no dentro de este proyecto')

    class Meta:
        unique_together = (('cod_proyecto', 'cod_usuario'),)
