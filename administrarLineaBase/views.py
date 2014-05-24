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
    *Vista para la creación de una* ``Linea Base`` * dentro de una fase específica.*

    :param request: HttpRequest necesario para la creación de una Linea Base, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase donde se creará la Linea Base.
    :return: Una nueva Línea Base fue establecida en la fase.

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
        mensaje = 'Error al crear Linea Base. No existen items VALIDADOS en la fase'
        error = 1

    return workphase(request, id_fase)


def calculoImpacto(padres, hijos, costo, tiempo, grafo):
    """
    *Función recursiva para realizar el cálculo de impacto por los ítems que se desean modificar dentro de una Línea Base.*
    *La función identificará todos los hijos que posea un ítem y al mismo tiempo los hijos de esto y los almacerará en padres
    e hijos respectivamente*

    :param padres: Recibe una lista vacía, en donde la función almacenará los padres de los ítems hijos.
    :param hijos: Recibe una lista vacía, donde la función almacenará todos los hijos del ítem.
    :param costo: Es el costo que se irá acumulando de acuerdo a los ítems que se encuentran afectados por la modificación de los ítems especificados en la solicitud.
    :param tiempo: Es el tiempo que se irá acumulando de acuerdo a los ítems que se encuentran afectados por la modificación de los ítems especificados en la solicitud.
    :param grafo: Es el grafo de relaciones que se irá formando de acuerdo a los ítems que serán afectados por la modificación de los ítems especificados en la solicitud.
    :return: Regresa el costo, tiempo y el grafo de relaciones entre los ítems afectados.
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

        arista = pydot.Edge(item.nombre, "^.^")
        grafo.add_edge(arista)
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
    *Función para la creación del resumen del calculo de impacto de relaciones.*
    *Esta función utiliza la función auxiliar* ``calculoImpacto`` * y junto con ella realiza la búsqueda de todos
    los ítems que se encuentran afectados por los items que se desean modificar*

    :param request: HttpRequest necesario para realizar el calculo de impacto, es la solicitud de la acción.
    :param id_item: Es el ítem que se desea modificar y por el cual se debe realizar el cálculo de impacto.
    :return: Regresa el costo y el tiempo estimados para la culminación de las modificaciones específicas.
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
    *Función para visualizar Líneas Bases existentes en la fase actual*

    :param request: HttpRequest necesario para visualizar las Lineas Base dentro de una fase, es la solicitud de la acción.
    :param id_fase: Es el identificador de la Fase a la cual se le consultará sobre las líneas bases existentes en ella.
    :return: Retorna una lista de todas las Lineas Bases existentes en la Fase y los ítems que forman parte de las mismas.

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
        return vistaDesarrollo(request, fase.proyecto.id)


def cancelarSolicitudCambios(request, id_solicitud, id_fase):
    """
    *Vista para cancelar una solicitud de cambios expedida*
    Obs. Solo puede cancelarse una solicitud que aún no ha sido Aprobada o Rechazada.

    :param request: HttpRequest necesario para cancelar la solicitud, es la solicitud de la acción.
    :param id_solicitud: Es el identificador de la Solicitud de Cambios que se desea cancelar.
    :param id_fase: Es el identificador de la fase a la cual se encuentra ligada la Solicitud de Cambios.
    return: Solicitud de Cambios cancelada exitosamente.
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


def workApplication(request, id_fase):
    """
    *Vista para la gestión de Solicitud de Cambios Creada por el usuario.*
    *El usuario puede gestionar las diferentes solicitudes de cambios que ha expedido y ver el proceso de estas.
    y también puede ver todas las solicitudes de cambios expedidas sobre la fase específica.

    :param request: HttpRequest necesario para visualizar las Solicitudes Existentes en la fase, es la solicitud de la acción.
    :param id_fase: Es el identificador de la fase a la cual se encuentran ligadas las Solicitudes de Cambios que se visualizan.
    :return: Retorna una lista de todas las Solicitudes de Cambios que fueron expedidas sobre la fase.
    """
    error = None
    message = None
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
    *Función para visualizar los atributos de la Solicitud de Cambios, los cuales se encuentran especificados en el modelos*
     ``Solicitud de Cambios``.

    :param request: HttpRequest necesario para visualizar la Solicitud de Cambios creada, es la solicitud de la acción.
    :param id_solicitud: Es el identificador de la Solcitud de Cambios la cual se desea visualizar.
    :param id_fase: Es el identificador de la Fase a la cual se encuentra ligada la Solicitud de Cambios.
    :return: Despliega en pantalla los datos correspondientes sobre una solicitud de cambios.
    """
    fase = Fase.objects.get(pk=id_fase)
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
    *Función para la creación de solicitudes de cambios en el sistema. En la cual se debe especificar las razones por la
    cual se desea realizar los cambios y una lista de ítems que desea modificar.*

    :param request: HttpRequest necesario para la creación de una Solicitud de Cambios en la fase, es la solicitud de la acción.
    :param id_fase: Es el identificador de la Fase a la cual se encuentra ligada la Solicitud de Cambios.
    :return: Regresa una Solicitud de Cambios creada exitosamente.

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
                    costo, tiempo = generarCalculoImpacto(request, itemNuevo.id)
                    solicitud.costo = solicitud.costo + costo
                    solicitud.tiempo = solicitud.tiempo + tiempo

                solicitud.save()
                mensaje = 'Solicitud Creada y Enviada satisfactoriamente al comité de cambios'
                error = 0
                return workApplication(request, fase.id)

    form = createSCForm()
    asignarItemSolicitud = asignarItemSolicitudForm(id_fase=id_fase)

    return render(request, 'lineabase/createsolicitud.html', {'form': form, 'fase': fase, 'proyecto': proyecto,
                                                    'user': request.user, 'asignarItemSolicitud': asignarItemSolicitud, },
                                                    context_instance=RequestContext(request))


def votarSolicitud(request, id_solicitud, voto):
    """
    *Función para expedir un voto correspondiente a una Solicitud de Cambios. Los votos son realizados por el comite de cambios.*

    :param request: HttpRequest necesario para votar la Solicitud de Cambios creada, es la solicitud de la acción.
    :param id_solicitud: Es el identificador de la Solcitud de Cambios la cual se desea votar.
    :param voto: Es el voto sobre la Solicitud de Cambios.
    :return: Voto confirmado y registrado exitosamente en el Sistema.
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


