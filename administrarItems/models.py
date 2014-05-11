#encoding:utf-8
from django.db import models
from administrarTipoItem.models import TipoItem, Atributo


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

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    fecha_mod = models.DateField(help_text='Fecha de última modificación', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='PEN', help_text='Estado del proyecto')
    tipoitem = models.ForeignKey(TipoItem)
    complejidad = models.IntegerField( help_text='Ingresar la complejidad del ítem creado, un valor entre 0-100')
    costo = models.IntegerField(help_text='Ingresar el costo de desarrollar el ítem')
    tiempo = models.IntegerField(help_text='Ingresar el tiempo estimado para desarrollar ')

    def __unicode__(self):
        return self.nombre


class campoEntero(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.FloatField()
    version = models.IntegerField()


class campoTextoCorto(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.CharField(max_length=140)
    version = models.IntegerField()


class campoTextoLargo(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.CharField(max_length=900)
    version = models.IntegerField()


class campoFile(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(TipoItem)
    valor = models.FileField(name='Archivo', upload_to='archivos')
    version = models.IntegerField()


class campoImagen(models.Model):
    """
    Campo Entero
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(TipoItem)
    valor = models.ImageField(name='Imagen', upload_to='archivos')
    version = models.IntegerField()