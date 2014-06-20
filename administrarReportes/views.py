#encoding: utf-8

import cStringIO as StringIO
import cgi
import os

import ho.pisa as pisa
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from administrarFases.models import Fase
from administrarItems.models import ItemBase, ItemRelacion
from administrarLineaBase.models import SolicitudCambios
from administrarProyectos.models import Proyecto
from administrarTipoItem.models import TipoItem


def generar_pdf(html, filename):
    """
    *Función que genera los* ``Reportes`` * en formato PDF. Recibe una codificación HTML y la convierte a formato PDF.*

    :param html: Página web (HTML) que se desea convertir en formato HTML
    :param filename: Nombre del reporte que se generará.
    :return: Despliega los reportes solicitados

    """
    STATICFILES_DIRS, = settings.STATICFILES_DIRS
    path = '%s/reportes/%s' % (STATICFILES_DIRS, filename)
    archivo = open(path, 'wb')
    result = StringIO.StringIO()
    pdf1 = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    pdf2= pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), archivo)
    archivo.close()
    if not pdf2.err:
        HttpResponseRedirect('/static/reportes/%s' %filename)
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el reporte: %s' % cgi.escape(html))



def reporte_proyecto(request, id_proyecto):
    """
    *Función que cumple con el trabajo de generar el reporte sobre de los proyectos que son solicitados por el usuario.*

    :param request: HTTPResponse, es la solicitud HTTP, que solicita la ejecución de dicha acción.
    :param id_proyecto: Identificador del proyecto el cual se desea obtener su reporte.
    :return: Despliega el reporte por proyecto en pantalla.

    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = Fase.objects.filter(proyecto=proyecto).order_by('nro_orden')

    itemsporfase = {}
    for fase in fases:
        tiposdelafase = TipoItem.objects.filter(fase=fase).order_by('id')
        items = ItemBase.objects.filter(tipoitem__in=tiposdelafase).order_by('id')

        relaciones = {}
        for i in items:
            try:
                itemRelacionado = ItemRelacion.objects.get(itemHijo=i).itemPadre
                relaciones[i] = itemRelacionado
            except:
                relaciones[i] = None

        itemsporfase[fase] = relaciones.items()

    filename = 'reporte_proyecto_' + proyecto.nombre + '.pdf'
    html = render_to_string('reportes/reporte_proyecto.html', {'pagesize':'A4', 'proyecto': proyecto, 'items': itemsporfase.items()},
                            context_instance=RequestContext(request))
    return generar_pdf(html, filename)


def reporte_solicitud(request, id_proyecto):
    """
    *Función que cumple con el trabajo de generar el reporte sobre de las solicitudes creadas sobre algún proyecto.*

    :param request: HTTPResponse, es la solicitud HTTP, que solicita la ejecución de dicha acción.
    :param id_proyecto: Identificador del proyecto el cual se desea obtener su reporte.
    :return: Despliega el reporte de las solicitudes creadas en el Proyecto.
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fases = Fase.objects.filter(proyecto=proyecto)

    solicitudesporfase = {}

    for fase in fases:
        solicitudes = SolicitudCambios.objects.filter(fase=fase).order_by('id')

        itemsensolicitud = {}
        for solicitud in solicitudes:
            itemsensolicitud[solicitud] = solicitud.items.all()

        solicitudesporfase[fase] = itemsensolicitud.items()


    filename = 'reporte_solicitudes_' + proyecto.nombre + '.pdf'
    html = render_to_string('reportes/reporte_solicitud.html', {'pagesize': 'A4', 'proyecto': proyecto, 'fases': fases,
                                                                'solicitudesporfase': solicitudesporfase.items()},
                            context_instance=RequestContext(request))

    return generar_pdf(html, filename)