#encoding:utf-8
from django.contrib.auth.models import Group
from django.core.mail import send_mail, send_mass_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils import timezone
from guardian.shortcuts import assign_perm, remove_perm, get_objects_for_user
import pydot
from django.shortcuts import render

from administrarFases.models import Fase
from administrarFases.views import workphase
from administrarItems.models import ItemBase, ItemRelacion
from administrarLineaBase.forms import createLBForm, createSCForm, asignarItemSolicitudForm, emitirVotoForm
from administrarLineaBase.models import LineaBase, SolicitudCambios, Votacion
from administrarProyectos.models import UsuariosVinculadosProyectos
from administrarProyectos.views import vistaDesarrollo
from administrarTipoItem.models import TipoItem
from administrarRolesPermisos.decorators import user_passes_test, crear_linea_base, puede_cancelar_solicitud, \
    puede_votar, puede_visualizar_solicitud
from autenticacion.models import Usuario
from is2.settings import MEDIA_ROOT, DEFAULT_FROM_EMAIL
from administrarRolesPermisos.decorators import user_passes_test, crear_linea_base, vinculado_proyecto_requerido, \
    verificar_permiso
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
    messages = []

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

                messages.append('Linea Base establecida para la fase: ' + fase.nombre)
                error = 0
                request.session['messages'] = messages
                request.session['error'] = error
                return HttpResponseRedirect(reverse('administrarFases.views.workphase', kwargs={'id_fase': id_fase}))
        else:

            form = createLBForm()
            return render(request, 'lineabase/createlb.html', {'form': form, 'proyecto': proyecto,
                                                           'user': request.user, 'fase':fase,
                                                           'itemsVAL': itemsVAL},)
    else:

        error = 1
        messages.append(u'Error al crear Linea Base. No existen items VALIDADOS en la fase.')
        request.session['messages'] = messages
        request.session['error'] = error
        return HttpResponseRedirect(reverse('administrarFases.views.workphase', kwargs={'id_fase': id_fase}))


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


@verificar_permiso(["consultar_Lineas_Base"], "id_fase", False)
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


# TODO: necesitan permisos el lider y el creador de la solicitud
@puede_cancelar_solicitud()
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
    mensaje = []

    if solicitud.estado == 'VOT':
        solicitud.estado = 'CAN'
        solicitud.save()
        mensaje.append('La solicitud ha sido cancelada con éxito.')
        error = 0

        request.session['messages'] = mensaje
        request.session['error'] = error
    else:
        mensaje.append('No se puede cancelar la solicitud. La misma ya no esta en votacion')
        error = 1

        request.session['messages'] = mensaje
        request.session['error'] = error

    return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication', kwargs={'id_fase': id_fase}))


@vinculado_proyecto_requerido("id_fase")
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

    nombre = "ComiteDeCambios-" + str(proyecto.id)
    miembro = False
    if usuario.groups.filter(name=nombre).exists():
        miembro = True

    misSolicitudes_lista = {}
    for s in misSolicitudes:
        misSolicitudes_lista[s] = s.votacion_set.filter(usuario=request.user)

    otrasSolicitudes_lista = {}
    for s in otrasSolicitudes:
        otrasSolicitudes_lista[s] = s.votacion_set.filter(usuario=request.user)

    usuario = request.user
    objetos = get_objects_for_user(usuario, 'crear_Solicitud_Cambio', klass=Fase)
    puedeCrearSC = False

    if fase in objetos:
        puedeCrearSC = True

    error = None
    messages = None
    if 'error' in request.session:
        error = request.session.pop('error')
    if 'messages' in request.session:
        messages = request.session.pop('messages')

    return render(request, 'lineabase/workapplication.html', {'proyecto': proyecto, 'fase': fase, 'user': usuario,
                                                              'misSolicitudes': misSolicitudes_lista.items(),
                                                              'error': error, 'messages': messages,
                                                              'puedeCrearSC': puedeCrearSC, 'miembro': miembro,
                                                              'otrasSolicitudes': otrasSolicitudes_lista.items(), })


@puede_visualizar_solicitud()
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


@verificar_permiso(["crear_Linea_Base"], "id_fase", False)
def crearSolicitudCambios(request, id_fase):
    """
    *Función utilizada para la creación de solicitudes de cambios en el sistema. En ella se debe especificar
    los ítems que se desean modificar, el motivo expreso de la solicitud y el informe de impacto.*

    :param request: HttpRequest, se utiliza para llamar a la función, es la solicitud de la acción.
    :param id_fase: Identificador de la Fase a la que pertenece la solicitud..

    """
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto
    mensajes = []

    tipos = TipoItem.objects.filter(fase=fase)
    opciones = ItemBase.objects.filter(estado='ELB', tipoitem__in=tipos)
    if not opciones:
        mensajes.append('Error al crear la solicitud de cambios. No existen items en Linea Base en esta fase.')
        error = 1
        request.session['messages'] = mensajes
        request.session['error'] = error
        return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication', kwargs={'id_fase': id_fase}))

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

                mensajes.append('Solicitud Creada y Enviada satisfactoriamente al comité de cambios')
                error = 0
                request.session['messages'] = mensajes
                request.session['error'] = error
                # enviarNotificacionesComite(solicitud.id)

                return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication', kwargs={'id_fase': id_fase}))

    form = createSCForm()
    asignarItemSolicitud = asignarItemSolicitudForm(id_fase=id_fase)

    return render(request, 'lineabase/createsolicitud.html', {'form': form, 'fase': fase, 'proyecto': proyecto,
                                                    'user': request.user, 'asignarItemSolicitud': asignarItemSolicitud, },
                                                    context_instance=RequestContext(request))


@puede_votar()
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
    mensaje = []

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
                    solicitud.save()
                    # enviarNotificacionSolicitudAprobada(solicitud.id)
                    for item in solicitud.items.all():
                        assign_perm("credencial", solicitud.usuario, item)
                        padres = [item.id]
                        hijos = []
                        buscarHijos(padres, hijos)

                else:
                    solicitud.estado = 'RCH'
                    solicitud.save()

            mensaje.append('Voto confirmado para la solicitud ' + str(solicitud.id))
            error = 0
            # enviarSolicitudRespuesta(solicitud.id)
            request.session['messages'] = mensaje
            request.session['error'] = error
            return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication', kwargs={'id_fase': fase.id}))
    else:
        form = emitirVotoForm()
    return render(request, 'lineabase/createvote.html', {'form': form, 'proyecto': proyecto, 'user': request.user,
                                                         'fase': fase, 'solicitud': solicitud}, )


# TODO: controlar permisos al revocar credencial
def revocarPermisos(request, id_solicitud):

    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)

    for item in solicitud.items.all():
        remove_perm("credencial", solicitud.usuario, item)

    mensajes = []
    mensajes.append(u'Permisos de Modificacion de items de Linea Base revocados a ' + solicitud.usuario.username.capitalize())
    error = 0
    request.session['messages'] = mensajes
    request.session['error'] = error
    return HttpResponseRedirect(reverse('administrarLineaBase.views.workApplication',
                                        kwargs={'id_fase': solicitud.fase_id}))


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


def enviarNotificacionesComite(id_solicitud):
    """
    *Función para notificar al Comite de Cambios que se ha emitido una nueva solicitud de cambios y esta
    lista para su votación*

    :param id_solicitud: Identificador de la solicitud que se ha creado y notificado a los miembros del comite.
    """
    # TODO: Explota al crear solicitudes
    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)
    fase = solicitud.fase
    proyecto = fase.proyecto

    nombre = 'ComiteDeCambios-' + str(proyecto.id)
    grupo = Group.objects.get(name=nombre)
    miembros = grupo.user_set.all()
    asunto = 'Notificacion: Nueva Solicitud de Cambios'

    for user in miembros:
        mensaje =   'Estimado ' + user.get_full_name() + ':\n\n' \
                    'Usted ha recibido este correo por que forma parte del Comite de Cambios del Proyecto ' + \
                     proyecto.nombre + ' y esto es una notificacion sobre la nueva solicitud de cambios recibida.' \
                    '\nSolicitud Numero: ' + str(solicitud.id) + '\nSolicitante: ' + solicitud.usuario.get_full_name()\
                    + '\n\nAtte.\nZARpm Team'
        send_mail(asunto, mensaje, DEFAULT_FROM_EMAIL, [user.email] )


def enviarNotificacionSolicitudAprobada(id_solicitud):
    """
    *Función para notificar a todos los usuarios vinculados al proyecto que se ha Aceptado una solicitud de cambios.*

    :param id_solicitud: Identificador de la solicitud que se ha creado y notificado a los miembros del comite.
    """
    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)
    fase = solicitud.fase
    proyecto = fase.proyecto

    mensajes = []
    usuarios = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=proyecto).exclude(cod_usuario=solicitud.usuario)

    for user in usuarios:
        mensaje = ('Notificacion: Solicitud de Cambios Aprobada',  'Estimado Usuario:\n\n' \
                    'Usted ha recibido este correo por que forma parte del equipo de Desarrollo del Proyecto ' + \
                     proyecto.nombre + ' y esto es una notificacion sobre la solicitud de cambio que ha sido APROBADA.' \
                    '\nSolicitud Numero: ' + str(solicitud.id) + '\nSolicitante: ' + solicitud.usuario.get_full_name()\
                    + '\n\nAtte.\nZARpm Team', DEFAULT_FROM_EMAIL, [user.cod_usuario.email])
        mensajes.append(mensaje)

    send_mass_mail((mensajes))


def enviarSolicitudRespuesta(id_solicitud):
    """
    *Función para notificar al emisor la respuesta del comite de cambios sobre la solicitud realizada.*

    :param id_solicitud: Identificador de la solicitud que se ha creado y notificado a los miembros del comite.
    """
    #TODO: aca explota al votar sobre una solicitud
    solicitud = SolicitudCambios.objects.get(pk=id_solicitud)
    fase = solicitud.fase
    proyecto = fase.proyecto
    user = solicitud.usuario

    asunto = 'Notificacion: Respuesta del Comite de Cambios'

    mensaje =   'Estimado ' + user.get_full_name() + ':\n\n' \
                'Usted ha recibido este correo por que ha enviado una solicitud de cambios al Comite de Cambios del Proyecto ' + \
                 proyecto.nombre + ' y esto es una notificacion con la respuesta de la solicitud de cambios expedida.' \
                '\nSolicitud Numero: ' + str(solicitud.id) + '\nSolicitante: ' + solicitud.usuario.get_full_name()\
                + '\nVotacion: ' + solicitud.estado + '\n\nAtte.\nZARpm Team'

    send_mail(asunto, mensaje, DEFAULT_FROM_EMAIL, [user.email] )