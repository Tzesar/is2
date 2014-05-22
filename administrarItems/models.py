#encoding:utf-8
import reversion
from django.db import models

from administrarLineaBase.models import LineaBase, SolicitudCambios
from administrarTipoItem.models import TipoItem, Atributo
from autenticacion.models import Usuario


class ItemBase(models.Model):
    """
    *Modelo para la clase* ``ItemBase`` *, en el cual se encuentras todos los atributos de un ítem:*
        + *Usuario*: Usuario que ha creado el ítem
        + *Usuario Modificacion*: Usuario que ha realizado la última modificación sobre el ítem
        + *Nombre*: Nombre del Ítem
        + *Descripción*: Breve reseña del ítem
        + *Fecha de Creación*: Fecha de creación del ítem
        + *Fecha de Modificación*: Fecha de última modificación del ítem.
        + *Estado*: Los estados posibles del Ítem. Por default: ACT(Activo)
        + *Tipo de Ítem*: Tipo de ítem al cual pertenece el ítem.
        + *Complejidad*: Es el nivel complejidad que abarca el item.
        + *Costo*: Es el nivel costo de recurso estimados a utilizar para desarrollar el item.
        + *Versión*: Es la última versión del ítem
        + *Linea Base*: Indica a que línea base pertenece el ítem. En caso de no pertenecer a ninguna queda como null
        + *Solicitudes*: Indica las solicitudes en las cuales el ítem se ha incluido para modificarlo una vez que se encuentra en línea base


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

    usuario = models.ForeignKey(Usuario, related_name='Usuario Creador')
    usuario_modificacion = models.ForeignKey(Usuario, related_name='Usuario Modificador')
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=140, help_text='Introduzca una breve reseña del proyecto', null=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='ACT', help_text='Estado del item')
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text='Fecha de creacion del Item', null=True)
    fecha_modificacion = models.DateTimeField(help_text='Fecha de modificacion del Item', null=True)
    tipoitem = models.ForeignKey(TipoItem)
    complejidad = models.IntegerField(help_text='Ingresar la complejidad del ítem creado, un valor entre 0-100')
    costo = models.IntegerField(help_text='Ingresar el costo de desarrollar el ítem')
    tiempo = models.IntegerField(help_text='Ingresar el tiempo estimado para desarrollar ')
    version = models.IntegerField(help_text='Version actual del item', default=1)
    linea_base = models.ForeignKey(LineaBase, null=True, verbose_name='Linea Base a la que pertenece el item')
    solicitudes = models.ManyToManyField(SolicitudCambios, related_name='items', help_text='Items especificados para modificar')

    def __unicode__(self):
        return self.nombre

reversion.register(ItemBase)


class ItemRelacion(models.Model):
    """
    Modelo útilizado para especificar las relaciones existentes entre los ítems.
        + *Item Padre*: Es el ítem que posee el rol de ser Padre o Antecesor de otro ítem.
        + *Item Hijo*: Es el ítem que posee el rol de ser Hijo o Sucesor de otro ítem.
        + *Estado*: Indica el estado de la relación, una relación puede ser Deshabilitada.
    """
    opciones_estado = (
        ('ACT', 'Activo'),
        ('DES', 'Desactivado'), )

    itemPadre = models.ForeignKey(ItemBase, verbose_name='ItemPadre', related_name='ItemPadre')
    itemHijo = models.ForeignKey(ItemBase, verbose_name='ItemHijo', related_name='ItemHijo', unique=True)
    estado = models.CharField(max_length=3, choices=opciones_estado, default='ACT', help_text='Estado de la relación')


class CampoNumero(models.Model):
    """
    *Modelo especifícado para todos los atributos que pertenecen al tipo ``Numérico``
        + *Item*: Item al que pertence el atributo.
        + *Atributo*: Atributo al que pertenece el campo numérico.
        + *Valor*: Valor del campo.
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.FloatField(verbose_name='Valor del dato numérico')

reversion.register(CampoNumero)


class CampoTextoCorto(models.Model):
    """
   *Modelo especifícado para todos los atributos que pertenecen al tipo ``Alfanumérico``
        + *Item*: Item al que pertence el atributo.
        + *Atributo*: Atributo al que pertenece el campo alfanumérico.
        + *Valor*: Valor del campo.
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.CharField(max_length=140, verbose_name='Texto')

reversion.register(CampoTextoCorto)


class CampoTextoLargo(models.Model):
    """
    *Modelo especifícado para todos los atributos que pertenecen al tipo ``Alfanumérico``
        + *Item*: Item al que pertence el atributo.
        + *Atributo*: Atributo al que pertenece el campo alfanumérico.
        + *Valor*: Valor del campo.
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    valor = models.CharField(max_length=900, verbose_name='Texto')

reversion.register(CampoTextoLargo)


class CampoFile(models.Model):
    """
    *Modelo especifícado para todos los atributos que pertenecen al tipo ``Archivo``
        + *Item*: Item al que pertence el atributo.
        + *Atributo*: Atributo al que pertenece el campo archivo.
        + *Archivo*: Dirección y nombre del archivo.
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    archivo = models.FileField(verbose_name='Archivo', upload_to='archivos')

reversion.register(CampoFile)


class CampoImagen(models.Model):
    """
    *Modelo especifícado para todos los atributos que pertenecen al tipo ``Imagen``
        + *Item*: Item al que pertence el atributo.
        + *Atributo*: Atributo al que pertenece el campo imagen.
        + *Imagen*: Dirección y nombre de la iamgen.
    """
    item = models.ForeignKey(ItemBase)
    atributo = models.ForeignKey(Atributo)
    imagen = models.ImageField(verbose_name='Imagen', upload_to='archivos')

reversion.register(CampoImagen)


