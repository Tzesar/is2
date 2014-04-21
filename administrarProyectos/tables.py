import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from administrarProyectos.models import Proyecto


class ProyectoTablaAdmin(tables.Table):

    modificar = tables.Column(verbose_name='Ver', orderable=False, empty_values=())

    def render_modificar(self, record):
        modificar_url = reverse("administrarProyectos.views.changeProject", args=[record.pk])
        return mark_safe('<a href="%s" class="btn btn-info"><span class="glyphicon glyphicon-chevron-right"></span></a>'
                         % modificar_url)

    class Meta:
        model = Proyecto
        attrs = {"class": "table table-hover"}

        fields = ('codigo', 'nombre', 'lider_proyecto', 'fecha_creacion', 'estado', )
        exclude = ('descripcion', 'fecha_inicio', 'fecha_fin', 'observaciones', )


class ProyectoTabla(tables.Table):

    modificar = tables.Column(verbose_name='Ver', orderable=False, empty_values=())

    def render_modificar(self, record):
        modificar_url = reverse("administrarProyectos.views.workProject", args=[record.pk])
        return mark_safe('<a href="%s" class="btn btn-info"><span class="glyphicon glyphicon-chevron-right"></span></a>'
                         % modificar_url)

    class Meta:
        model = Proyecto
        attrs = {"class": "table table-hover"}

        fields = ('codigo', 'nombre', 'lider_proyecto', 'fecha_creacion', 'estado', )
        exclude = ('pk', 'descripcion', 'fecha_inicio', 'fecha_fin', 'observaciones', )
