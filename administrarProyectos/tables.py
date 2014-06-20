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
        info_url = reverse("administrarProyectos.views.infoProject", args=[record.pk])
        proyecto = Proyecto.objects.get(pk=record.pk)
        if proyecto.estado == 'ANU' or proyecto.estado == 'FIN':
            return mark_safe('<span data-toggle="tooltip" title="Informacion del Proyecto" id="tooltip"> '
                             '<a href="%s" class="btn btn-sm btn-primary"><span class="glyphicon glyphicon-eye-open"></span></a></span> '
                              % info_url)
        return mark_safe('<span data-toggle="tooltip" title="Modificar Proyecto" id="tooltip"> '
                         '<a href="%s" class="btn btn-sm btn-primary"><span class="glyphicon glyphicon-wrench"></span></a></span> '
                         % modificar_url +
                         '<span data-toggle="tooltip" title="Anular Proyecto" id="tooltip"> '
                         '<a href="%s" class="btn btn-sm btn-danger"><span class="glyphicon glyphicon-remove"></span></a> '
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

    modificar = tables.Column(verbose_name='Ver', orderable=False, empty_values=())

    def render_modificar(self, record):
        modificar_url = reverse("administrarProyectos.views.workProject", args=[record.pk])
        info_url = reverse("administrarProyectos.views.infoProject", args=[record.pk])
        proyecto = Proyecto.objects.get(pk=record.pk)
        if proyecto.estado == 'ACT' or proyecto.estado == 'PEN':
            return mark_safe('<span data-toggle="tooltip" title="Trabajar en Proyecto" id="tooltip"> '
                             '<a href="%s" class="btn btn-sm btn-primary"><span class="glyphicon glyphicon-forward"></span></a> '
                             % modificar_url )
        elif proyecto.estado == 'ANU':
            return mark_safe('<span data-toggle="tooltip" title="Informacion del Proyecto" id="tooltip"> '
                             '<a href="%s" class="btn btn-sm btn-danger"><span class="glyphicon glyphicon-eye-open"></span></a> '
                             % info_url )
        elif proyecto.estado == 'FIN':
            return mark_safe('<span data-toggle="tooltip" title="Informacion del Proyecto" id="tooltip"> '
                             '<a href="%s" class="btn btn-sm btn-success"><span class="glyphicon glyphicon-eye-open"></span></a> '
                             % info_url )


    class Meta:
        model = Proyecto
        attrs = {"class": "table table-hover"}

        fields = ('nombre', 'lider_proyecto', 'fecha_creacion', 'estado', )
        exclude = ('pk', 'descripcion', 'fecha_inicio', 'fecha_fin', 'observaciones', )

    def __init__(self, *args, **kwargs):
        super(ProyectoTabla, self).__init__(*args, **kwargs)