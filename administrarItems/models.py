#encoding:utf-8
from django.db import models
from administrarTipoItem.models import TipoItem, Atributo
from autenticacion.models import Usuario
import reversion


class ItemBase(models.Model):
    """
    *Modelo para la clase* ``Proyecto`` *, en el cual se encuentras todos los atributos de un proyecto:*
        + *Nombre*: Nombre del Ítem
        + *Descripción*: Breve reseña del ítem
        + *Fecha de Modificación*: Fecha de última modificación del ítem.
        + *Estado*: Los estados posibles del Ítem. Por default: ACT(Activo)
        + *Tipo de Ítem*: Tipo de ítem al cual pertenece el ítem

    :param args: Argumentos para el modelo ``Model``.
    :param kwargs: Keyword Arguments para la el modelo ``Model``.
    """
    opciones_estado = (
        ('ACT', 'Activo'),
        ('DDB', 'Dado de Baja'),
        ('VAL', 'Validado'),
        ('ELB', 'En linea base'),
        ('REV', 'Revision'),
        ('FIN', 'Finalizado'), )

    usuario = models.ForeignKey(Usuario, null=True, related_name='Usuario Creador')
    usuario_modificacion = models.ForeignKey(Usuario, null=True, related_name='Usuario Modificador')
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    fecha_mod = models.DateField(help_text='Fecha de última modificación', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='ACT', help_text='Estado del item')
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text='Fecha de creacion del Item', null=True)
    fecha_modificacion = models.DateTimeField(help_text='Fecha de modificacion del Item', null=True)
    tipoitem = models.ForeignKey(TipoItem)
    complejidad = models.IntegerField( help_text='Ingresar la complejidad del ítem creado, un valor entre 0-100')
    costo = models.IntegerField(help_text='Ingresar el costo de desarrollar el ítem')
    tiempo = models.IntegerField(help_text='Ingresar el tiempo estimado para desarrollar ')

    def __unicode__(self):
        return self.nombre

reversion.register(ItemBase)


class ItemRelacion(models.Model):
    """
    Modelo para la relación entre ítems.
    """
    opciones_estado = (
        ('ACT', 'Activo'),
        ('DES', 'Desactivado'), )

    itemPadre = models.ForeignKey(ItemBase, verbose_name='ItemPadre', related_name='ItemPadre')
    itemHijo = models.ForeignKey(ItemBase, verbose_name='ItemHijo', related_name='ItemHijo', unique=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='ACT', help_text='Estado de la relación')



class CampoNumero(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.FloatField(verbose_name='Valor del dato numérico')

reversion.register(ItemBase)


class CampoTextoCorto(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.CharField(max_length=140, verbose_name='Texto')

reversion.register(ItemBase)


class CampoTextoLargo(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.CharField(max_length=900, verbose_name='Texto')

reversion.register(ItemBase)


class CampoFile(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    archivo = models.FileField(verbose_name='Archivo', upload_to='archivos')

reversion.register(ItemBase)


class CampoImagen(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    imagen = models.ImageField(verbose_name='Imagen', upload_to='archivos')

reversion.register(ItemBase)


