#encoding:utf-8
from django.template import RequestContext
from django.utils import timezone
import pydot
from django.shortcuts import render

from administrarFases.models import Fase
from administrarFases.views import workphase
from administrarItems.models import ItemBase, ItemRelacion
from administrarLineaBase.forms import createLBForm, createSCForm, asignarItemSolicitudForm, emitirVotoForm
from administrarLineaBase.models import LineaBase, SolicitudCambios, Votacion
from administrarProyectos.views import vistaDesarrollo
from administrarTipoItem.models import TipoItem
from is2.settings import MEDIA_ROOT


def createLB(request, id_fase):
    """
    Esta es la vista para la creación de Linea Base
    """
    fase = Fase.objects.get(pk=id_fase)
    tipoitem = TipoItem.objects.filter(fase=fase)
    items = ItemBase.objects.filter(tipoitem=tipoitem)
    proyecto = fase.proyecto
    itemsVAL = items.filter(estado='VAL')

    if itemsVAL:
        if request.method == 'POST':
            form = createLBForm(request.POST)
            if form.is_valid():
                lineaBase = form.save(commit=False)
                lineaBase.fase = fase
                lineaBase.fecha_creacion = timezone.now()
                lineaBase.fecha_modificacion = timezone.now()
                lineaBase.save()
                for item in itemsVAL:
                    item.estado = 'ELB'
                    item.linea_base = LineaBase.objects.get(pk=lineaBase.id, fase=fase)
                    item.save()


                # Activamos la siguiente fase al crear la primera linea base
                cantFases = Fase.objects.filter(proyecto=proyecto).count()
                if fase.nro_orden != cantFases:
                    ordenNext = fase.nro_orden + 1
                    faseSgte = Fase.objects.get(proyecto=proyecto, nro_orden=ordenNext)
                    if faseSgte.estado == 'PEN':
                        faseSgte.estado = 'DES'
                        faseSgte.save()

                mensaje = 'Linea Base establecida para la fase: ' + fase.nombre
                error = 0
                request.method = 'GET'
                return workphase(request, id_fase, error=error, message=mensaje)
        else:
            form = createLBForm()
        return render(request, 'lineabase/createlb.html', {'form': form, 'proyecto': proyecto,
                                                        'user': request.user, 'fase':fase, })
    else:
        mensaje = 'Error al crear Linea Base. No existen items VALIDADOS en la fase'
        error = 1
        return workphase(request, id_fase, error=error, message=mensaje)


def calculoImpacto(padres, hijos, costo, tiempo, grafo):
    """
    Vista para realizar el calculo de impacto
    """

    if padres:
        padre = padres.pop()
        item = ItemBase.objects.get(pk=padre)
        costo.append(item.costo)
        tiempo.append(item.tiempo)

        item_hijos = list(ItemRelacion.objects.filter(itemPadre=padre).values_list('itemHijo', flat=True))
        hijos.extend(item_hijos)
        padres.extend(item_hijos)

        for articulo in item_hijos:
            itemHijo = ItemBase.objects.get(pk=articulo)
            arista = pydot.Edge(item.nombre, itemHijo.nombre)
            grafo.add_edge(arista)

        calculoImpacto(padres, hijos, costo, tiempo, grafo)

    else:
        return (costo, tiempo)


def generarCalculoImpactoHTML(request, id_item):
    """
    Vista para la creación del resumen del calculo de impacto de relaciones
    """
    usuario = request.user
    item = ItemBase.objects.get(pk=id_item)
    tipoitem = item.tipoitem
    fase = tipoitem.fase
    proyecto = fase.proyecto

    grafo = pydot.Dot(graph_type='graph')
    costo = []
    tiempo = []
    padres = [id_item]
    hijos = []

    calculoImpacto(padres, hijos, costo, tiempo, grafo)
    costo = sum(costo)
    tiempo = sum(tiempo)
    direccion = MEDIA_ROOT + 'grafos/' + item.nombre
    graph = grafo.write(direccion, format='png')
    direccion = '/static/grafos/' + item.nombre

    return render(request, 'lineabase/visualizarsolicitud.html', {'user':usuario, 'fase':fase, 'item':item, 'proyecto':proyecto,
                                                            'costo': costo, 'tiempo':tiempo, 'grafo':graph, 'direccion':direccion },
                                                            context_instance=RequestContext(request))


def generarCalculoImpacto(request, id_item):
    """
    Vista para la creación del resumen del calculo de impacto de relaciones
    """
    usuario = request.user
    item = ItemBase.objects.get(pk=id_item)
    tipoitem = item.tipoitem
    fase = tipoitem.fase
    proyecto = fase.proyecto

    grafo = pydot.Dot(graph_type='graph')
    costo = []
    tiempo = []
    padres = [id_item]
    hijos = []

    calculoImpacto(padres, hijos, costo, tiempo, grafo)
    costo = sum(costo)
    tiempo = sum(tiempo)
    direccion = MEDIA_ROOT + 'grafos/' + item.nombre
    grafo.write(direccion, format='png')
    direccion = '/static/grafos/' + item.nombre

    return costo, tiempo


def visualizarLB(request, id_fase):
    """
    Esta es la vista para visualizar Líneas Bases existentes en la fase actual
    """
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto
    LB = LineaBase.objects.filter(fase=fase)
    items = ItemBase.objects.filter(linea_base__in=LB)
    if LB:
        return render(request, 'lineabase/visualizarlb.html', {'user': request.user, 'proyecto': proyecto, 'fase': fase,
                                                               'items': items, 'lb': LB})
    else:
        mensaje = 'Aun no se han creado Lineas Base en la fase: ' + fase.nombre
        error = 1
        return vistaDesarrollo(request, fase.proyecto.id, error=error, message=mensaje)


def cancelarSolicitudCambios(request, id_solicitud, id_fase):
    """
    Vista para cancelar una solicitud de cambios expedida
    """

    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)

    if solicitud.estado == 'VOT':
        solicitud.estado = 'CAN'
        solicitud.save()
        mensaje = 'La solicitud ha sido cancelada con éxito'
        error = 0
        return workApplication(request, id_fase, error=error, mensaje=mensaje)

    else:
        mensaje = 'No se puede cancelar la solicitud.'
        error = 1
        return workApplication(request, id_fase, error=error, mensaje=mensaje)


def workApplication(request, id_fase, error=None, mensaje=None):
    """
    Vista para la gestión de Solicitud de Cambios Creada por el usuario
    """
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto
    misSolicitudes = SolicitudCambios.objects.filter(usuario=usuario, fase=fase)
    misPK = misSolicitudes.values_list('id', flat=True)
    otrasSolicitudes = SolicitudCambios.objects.filter(fase=fase).exclude(pk__in=misPK)

    misSolicitudes_lista = {}
    for s in misSolicitudes:
        misSolicitudes_lista[s] = s.votacion_set.filter(usuario=request.user)

    otrasSolicitudes_lista = {}
    for s in otrasSolicitudes:
        otrasSolicitudes_lista[s] = s.votacion_set.filter(usuario=request.user)

    return render(request, 'lineabase/workapplication.html', {'proyecto': proyecto, 'fase': fase, 'user': usuario,
                                                              'misSolicitudes': misSolicitudes_lista.items(), 'error': error,
                                                              'otrasSolicitudes': otrasSolicitudes_lista.items()})


def visualizarSolicitud(request, id_solicitud, id_fase):
    """
    Vista para visualizar las Solicitudes creadas
    """
    fase = Fase.objects.get(pk=id_fase)
    tipoitem = TipoItem.objects.filter(fase=fase)
    proyecto = fase.proyecto

    solicitud = SolicitudCambios.objects.filter(pk=id_solicitud)

    itemsSolicitud = ItemBase.objects.filter(solicitudes__in=solicitud)

    grafos = []
    for item in itemsSolicitud:
        direccion = '/static/grafos/' + item.nombre
        grafos.append(direccion)

    return render(request, 'lineabase/visualizarsolicitud.html', {'user': request.user, 'fase': fase, 'proyecto': proyecto,
                                                             'solicitud': solicitud, 'items': itemsSolicitud, 'grafos':grafos})


def crearSolicitudCambios(request, id_fase):
    """
    Vista para la creación de solicitudes de cambios del sistema
    """
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    if request.method == 'POST':
        form = createSCForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.fase = fase
            solicitud.costo = 0
            solicitud.tiempo = 0

            asignarItemSolicitud = asignarItemSolicitudForm(request.POST, id_fase=id_fase)

            # Asigna los items a la solicitud
            if asignarItemSolicitud.is_valid():
                solicitud.save()
                items = asignarItemSolicitud.get_cleaned_data()
                print items
                for item in items:
                    itemNuevo = ItemBase.objects.get(id=item)
                    itemNuevo.solicitudes.add(solicitud)
                    itemNuevo.save()
                    costo, tiempo = generarCalculoImpacto(request, itemNuevo.id)
                    solicitud.costo = solicitud.costo + costo
                    solicitud.tiempo = solicitud.tiempo + tiempo


                solicitud.save()
                mensaje = 'Solicitud Creada y Enviada satisfactoriamente al comité de cambios'
                error = 0
                return workApplication(request, fase.id, error=error, mensaje=mensaje)

    form = createSCForm()
    asignarItemSolicitud = asignarItemSolicitudForm(id_fase=id_fase)

    return render(request, 'lineabase/createsolicitud.html', {'form': form, 'fase': fase, 'proyecto': proyecto,
                                                    'user': request.user, 'asignarItemSolicitud': asignarItemSolicitud, },
                                                    context_instance=RequestContext(request))


def votarSolicitud(request, id_solicitud, voto):
    """
    *Vista para realizar las votaciones correspondientes a una solicitud de cambio *
    """

    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)
    fase = solicitud.fase
    proyecto = fase.proyecto

    if request.method == 'POST':
        form = emitirVotoForm(request.POST)
        if form.is_valid():
            if voto == 1:
                votacion = form.save(commit=False)
                votacion.usuario = request.user
                votacion.solicitud = solicitud
                votacion.voto = 'GOOD'
                votacion.save()
            else:
                votacion = form.save(commit=False)
                votacion.usuario = request.user
                votacion.solicitud = solicitud
                votacion.voto = 'EVIL'
                votacion.save()

            votos = Votacion.objects.filter(solicitud=solicitud)
            aceptado = 0
            rechazado = 0
            if votos.count() == 3:
                for voto in votos:
                    if voto.voto == 'GOOD':
                        aceptado = aceptado + 1
                    else:
                        rechazado = rechazado + 1

                if aceptado > rechazado:
                    solicitud.estado = 'ACP'
                else:
                    solicitud.estado = 'RCH'

                solicitud.save()


            mensaje = 'Voto confirmado para la solicitud ' + str(solicitud.id)
            error = 0
            request.method = 'GET'
            return workApplication(request, fase.id, error=error, mensaje=mensaje)
    else:
        form = emitirVotoForm()
    return render(request, 'lineabase/createvote.html', {'form': form, 'proyecto': proyecto,
                                                         'user': request.user, 'fase': fase,
                                                         'solicitud': solicitud},
                  context_instance=RequestContext(request))
