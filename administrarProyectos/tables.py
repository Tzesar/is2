#encoding:utf-8
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from administrarProyectos.models import Proyecto


class ProyectoTablaAdmin(tables.Table):
    """
    *Tabla personalizada para la modificación de proyectos en el sistema.*

    :param args: Argumentos para el modelo ``Table``.
    :param kwargs: Keyword Arguments para la el modelo ``Table``.
    """

    modificar = tables.Column(verbose_name='Acciones', orderable=False, empty_values=())

    def render_modificar(self, record):
        modificar_url = reverse("administrarProyectos.views.changeProject", args=[record.pk])
        cancelar_url = reverse("administrarProyectos.views.cancelProject", args=[record.pk])
        return mark_safe('<a href="%s" class="text-info"><span class="glyphicon glyphicon-eye-open"></span></a> '
                         % modificar_url +
                         '<a href="%s" class="text-danger"><span class="glyphicon glyphicon-remove-sign"></span></a> '
                         % cancelar_url)

    class Meta:
        model = Proyecto
        attrs = {"class": "table table-hover"}

        fields = ('nombre', 'lider_proyecto', 'fecha_creacion', 'estado', )
        exclude = ('descripcion', 'fecha_inicio', 'fecha_fin', 'observaciones', )

    def __init__(self, *args, **kwargs):
        super(ProyectoTablaAdmin, self).__init__(*args, **kwargs)

class ProyectoTabla(tables.Table):
    """
    *Tabla personalizada para el desarrollo de proyectos en el sistema.*

    :param args: Argumentos para el modelo ``Table``.
    :param kwargs: Keyword Arguments para la el modelo ``Table``.
    """

    modificar = tables.Column(verbose_name='Acciones', orderable=False, empty_values=())

    def render_modificar(self, record):
        modificar_url = reverse("administrarProyectos.views.workProject", args=[record.pk])
        return mark_safe('<a href="%s" class="text-info"><span class="glyphicon glyphicon-eye-open"></span></a> '
                         % modificar_url )



    class Meta:
        model = Proyecto
        attrs = {"class": "table table-hover"}

        fields = ('nombre', 'lider_proyecto', 'fecha_creacion', 'estado', )
        exclude = ('pk', 'descripcion', 'fecha_inicio', 'fecha_fin', 'observaciones', )

    def __init__(self, *args, **kwargs):
        super(ProyectoTabla, self).__init__(*args, **kwargs)