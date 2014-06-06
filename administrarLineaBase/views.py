#encoding:utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils import timezone
from guardian.shortcuts import assign_perm
import pydot
from django.shortcuts import render

from administrarFases.models import Fase
from administrarFases.views import workphase
from administrarItems.models import ItemBase, ItemRelacion
from administrarLineaBase.forms import createLBForm, createSCForm, asignarItemSolicitudForm, emitirVotoForm
from administrarLineaBase.models import LineaBase, SolicitudCambios, Votacion
from administrarProyectos.views import vistaDesarrollo
from administrarTipoItem.models import TipoItem
from administrarRolesPermisos.decorators import user_passes_test, crear_linea_base
from is2.settings import MEDIA_ROOT


@user_passes_test(crear_linea_base)
def createLB(request, id_fase):
    """
    *Función para la creación de Linea Base, la creación de una Linea Base consiste en registrar todos los ítems
    validados de una fase, e introducirlos a una Linea Base, en donde estos se almacenan en su estado final dentro
    del proyecto.*

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase, a la cual se encuentra vinculada la Liena Base.
    :return: Crea una Liena Base y registra en ella todos los ítems validados dentro de la Fase.
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
                return workphase(request, id_fase)
        else:

            form = createLBForm()
        return render(request, 'lineabase/createlb.html', {'form': form, 'proyecto': proyecto,
                                                        'user': request.user, 'fase':fase, })
    else:

        error = 1
        messages = []
        messages.append(u'Error al crear Linea Base. No existen items VALIDADOS en la fase.')
        request.session['messages'] = messages
        request.session['error'] = error
        return HttpResponseRedirect(reverse('administrarFases.views.workphase', kwargs={'id_fase': id_fase}))
        # return workphase(request, id_fase)


def calculoImpacto(padres, hijos, costo, tiempo, grafo):
    """
    *Función que realiza el calculo de impacto, para todos aquellos ítems que son incluidos en una solicitud de cambios.
    Se utiliza para formar el grafo de relaciones y establever el costo y tiempo estimados a utilizar para las modificaciones
    especificadas. Realiza una búsqueda recursiva de todos los sucesores/hijos que se ecuentran afectados por los ítems
    que se desean modificar.

    :param padres: Lista que almacena todos los ancestros de un item.
    :param hijos: Lista que almacena todos los descendientes de un ítem.
    :param costo: Costo estimado(acumulado) para cumpliar con las modificaciones.
    :param tiempo: Tiempo estimado(acumulado) para cumpliar con las modificaciones.
    :param grafo: Grafo de relaciones de los ítems.
    :return costo: Costo estimado(TOTAL) para cumpliar con las modificaciones.
    :return tiempo: Tiempo estimado(TOTAL) para cumpliar con las modificaciones.
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


def generarGrafo(id_item):
    """
    *Función que realiza la creación del grafo de relaciones de un ítem.*

    :param id_item: Identificador del ítem del cual se desea formar su grafo de relaciones.

    """
    item = ItemBase.objects.get(pk=id_item)

    grafo = pydot.Dot(graph_type='graph')
    costo = []
    tiempo = []
    padres = [id_item]
    hijos = []

    calculoImpacto(padres, hijos, costo, tiempo, grafo)
    direccion = MEDIA_ROOT + 'grafos/' + item.nombre
    grafo.write(direccion, format='png')

    return


def generarCalculoImpacto(id_item, id_solicitud):
    """
    *Función que realiza el llamado para realizar el calculo de impacto por los ítems especificados en la solicitud,
    y genera el informe de impacto para todos los ítems con sus respectivos grafos de relaciones.

    :param id_item: identificador del ítem especificado en la solicitud de cambios.
    :param id_solicitud: Identificador de la Solicitud en la cual el ítem fue especificado para su modificación.
    :return costo: Costo estimado(TOTAL) para cumpliar con las modificaciones.
    :return tiempo: Tiempo estimado(TOTAL) para cumpliar con las modificaciones.

    """
    item = ItemBase.objects.get(pk=id_item)
    tipoitem = item.tipoitem
    fase = tipoitem.fase

    grafo = pydot.Dot(graph_type='graph')
    costo = []
    tiempo = []
    padres = [id_item]
    hijos = []

    calculoImpacto(padres, hijos, costo, tiempo, grafo)
    costo = sum(costo)
    tiempo = sum(tiempo)
    direccion = MEDIA_ROOT + 'grafos/' + item.nombre + '_' + str(id_solicitud)
    grafo.write(direccion, format='png')

    return costo, tiempo


def visualizarLB(request, id_fase):
    """
    *Función que cumple con el papel de visualizar una Linea Base existente dentro de una fase.*

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase, de la cual se desea visualizar las Lineas Bases Creadas.
    """
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto
    LB = LineaBase.objects.filter(fase=fase)
    items = ItemBase.objects.filter(linea_base__in=LB)
    if LB:
        return render(request, 'lineabase/visualizarlb.html', {'user': request.user, 'proyecto': proyecto, 'fase': fase,
                                                               'items': items, 'lb': LB})
    else:
        mensaje = []
        mensaje.append('Aun no se han creado Lineas Base en la fase: ' + fase.nombre)
        error = 1

        request.session['messages'] = mensaje
        request.session['error'] = error
        return HttpResponseRedirect(reverse('administrarProyectos.views.vistaDesarrollo',
                                            kwargs={'id_proyecto': fase.proyecto_id}))


def cancelarSolicitudCambios(request, id_solicitud, id_fase):
    """
    *Función para cancelar una solicitud de cambios, de forma que los cambios solicitados seas descartados
    inmediatamente sin necesidad de realizar una votación.*
    Obs. Solo puede ser Cancelado si la Solicitud aún no ha sido Aceptada o Rechazada

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase a la que pertenece la solicitud..
    :param id_solicitud: Identificador de la Solicitud de Cambios que se desea cancelar.

    """

    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)

    if solicitud.estado == 'VOT':
        solicitud.estado = 'CAN'
        solicitud.save()
        mensaje = 'La solicitud ha sido cancelada con éxito'
        error = 0

        request.session['messages'] = mensaje
        request.session['error'] = error
    else:
        mensaje = 'No se puede cancelar la solicitud.'
        error = 1

        request.session['messages'] = mensaje
        request.session['error'] = error

    return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication', kwargs={'id_fase': id_fase}))
    # return workApplication(request, id_fase)


def workApplication(request, id_fase):
    """
    *Función que cumple con el rol de listar todas las Solicitudes de Cambios de los Usuarios dentro del Proyecto.
    El usuario visualiza las Solicitudes creadas por él y por otros usuarios. Se listan todas las solicitudes con
    sus atributos y estados respectivos.*
    Obs. Aqui se realizan las votaciones sobre las solicitudes.

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase, de la cual se consultarán las solicitudes.

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

    error = None
    messages = None
    if 'error' in request.session:
        error = request.session.pop('error')
    if 'messages' in request.session:
        messages = request.session.pop('messages')
    return render(request, 'lineabase/workapplication.html', {'proyecto': proyecto, 'fase': fase, 'user': usuario,
                                                              'misSolicitudes': misSolicitudes_lista.items(),
                                                              'error': error, 'messages': messages,
                                                              'otrasSolicitudes': otrasSolicitudes_lista.items()})


def visualizarSolicitud(request, id_solicitud, id_fase):
    """
    *Funcion para visualizar las Solicitudes creadas. Se consulta explicitamente todos los atributos de la Solicitud
    y en caso de finalizar la votación, nos muestra el resultado de esta junto con el usuario que emitio el voto y
    su postura con respecto a la solicitud de cambios.*

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase a la que pertenece la solicitud..
    :param id_solicitud: Identificador de la Solicitud de Cambios que se desea cancelar.

    """
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    solicitud = SolicitudCambios.objects.filter(pk=id_solicitud)

    itemsSolicitud = solicitud[0].items.all()

    resultado_votacion = Votacion.objects.filter(solicitud=solicitud)

    items_grafos = {}
    for item in itemsSolicitud:
        direccion = '/static/grafos/' + item.nombre + '_' + str(id_solicitud)
        items_grafos[item] = direccion

    return render(request, 'lineabase/visualizarsolicitud.html', {'user': request.user, 'fase': fase,
                                                                  'proyecto': proyecto, 'solicitud': solicitud,
                                                                  'items': items_grafos.items(),
                                                                  'votaciones': resultado_votacion})


def crearSolicitudCambios(request, id_fase):
    """
    *Función utilizada para la creación de solicitudes de cambios en el sistema. En ella se debe especificar
    los ítems que se desean modificar, el motivo expreso de la solicitud y el informe de impacto.*

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase a la que pertenece la solicitud..

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
                for item in items:
                    itemNuevo = ItemBase.objects.get(id=item)
                    itemNuevo.solicitudes.add(solicitud)
                    itemNuevo.save()
                    costo, tiempo = generarCalculoImpacto(itemNuevo.id, solicitud.id)
                    solicitud.costo = solicitud.costo + costo
                    solicitud.tiempo = solicitud.tiempo + tiempo

                solicitud.save()
                mensaje = 'Solicitud Creada y Enviada satisfactoriamente al comité de cambios'
                error = 0

                request.session['messages'] = mensaje
                request.session['error'] = error
                # return workApplication(request, fase.id, error=error, mensaje=mensaje)
                return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication', kwargs={'id_fase': id_fase}))

    form = createSCForm()
    asignarItemSolicitud = asignarItemSolicitudForm(id_fase=id_fase)

    return render(request, 'lineabase/createsolicitud.html', {'form': form, 'fase': fase, 'proyecto': proyecto,
                                                    'user': request.user, 'asignarItemSolicitud': asignarItemSolicitud, },
                                                    context_instance=RequestContext(request))


def votarSolicitud(request, id_solicitud, voto):
    """
    *Función para realizar las votaciones correspondientes a una solicitud de cambio. *

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param voto: Postura asumida por el miembro del Comite de Cambios.
    :param id_solicitud: Identificador de la Solicitud de Cambios que se desea cancelar.
    """

    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)
    fase = solicitud.fase
    proyecto = fase.proyecto

    if request.method == 'POST':
        form = emitirVotoForm(request.POST)
        if form.is_valid():
            if str(voto) == "1":
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
            if votos.count() >= 3:
                for voto in votos:
                    if voto.voto == 'GOOD':
                        aceptado = aceptado + 1
                    else:
                        rechazado = rechazado + 1

                if aceptado > rechazado:
                    solicitud.estado = 'ACP'
                    for item in solicitud.items.all():
                        assign_perm("credencial", solicitud.usuario, item)
                        padres = [item.id]
                        hijos = []
                        buscarHijos(padres, hijos)

                else:
                    solicitud.estado = 'RCH'

                solicitud.save()


            mensaje = 'Voto confirmado para la solicitud ' + str(solicitud.id)
            error = 0
            # request.method = 'GET'

            request.session['messages'] = mensaje
            request.session['error'] = error
            return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication', kwargs={'id_fase': fase.id}))
            # return workApplication(request, fase.id, error=error, mensaje=mensaje)
    else:
        form = emitirVotoForm()
    return render(request, 'lineabase/createvote.html', {'form': form, 'proyecto': proyecto,
                                                         'user': request.user, 'fase': fase,
                                                         'solicitud': solicitud}, )


def buscarHijos(padres, hijos):
    """
    *Vista para realizar una busqueda recursiva de todos los descendientes de un ítem.*

    :param padres: Lista que almacena todos los ancestros de un item.
    :param hijos: Lista que almacena todos los descendientes de un ítem.
    """
    if padres:
        padre = padres.pop()
        item = ItemBase.objects.get(pk=padre)
        if item.estado == 'ELB':
            item.estado = 'REV'
            item.save()
            fase = item.tipoitem.fase
            if fase.estado == 'FIN':
                fase.estado = 'REV'
                fase.save()

        item_hijos = list(ItemRelacion.objects.filter(itemPadre=padre).values_list('itemHijo', flat=True))
        hijos.extend(item_hijos)
        padres.extend(item_hijos)

        buscarHijos(padres, hijos)

    else:
        return