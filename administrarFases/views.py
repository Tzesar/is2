#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render
from django.utils.html import format_html
from django.db import IntegrityError

from administrarFases.forms import NewPhaseForm, ChangePhaseForm
from administrarLineaBase.models import LineaBase
from administrarProyectos.views import workProject, vistaDesarrollo
from administrarRolesPermisos.decorators import *
from administrarItems.models import ItemRelacion, ItemBase



@login_required()
@lider_requerido
def createPhase(request, id_proyecto):
    """
    *Vista para la creación de fases en el sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para crear fases dentro de los proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema al cual se le vincularán las fases creadas.
    :param args: Argumentos para el modelo ``Fase``.
    :param kwargs: Keyword Arguments para la el modelo ``Fase``.
    :return: Proporciona la pagina ``createphase.html`` con el formulario correspondiente.
            Crea la fase dentro del proyecto especificando y luego regresa al menu principal
    """

    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = NewPhaseForm(request.POST, project)
        if form.is_valid():
            fase = form.save(commit=False)
            fase.proyecto = project
            fasesProyecto = Fase.objects.filter(proyecto=project)

            if fasesProyecto:
                fase.nro_orden = fasesProyecto.count() + 1
            else:
                fase.nro_orden = 1

            try:
                fase.save()
            except IntegrityError:
                err = format_html('<b><i>Datos Erróneos:</b></i><br>'
                                  '<i>El nombre especificado de fase ya existe. Verifiquelo y vuelva a intentarlo</i>')
                return render(request, "fase/createphase.html", {'form': form, 'user': request.user,
                                                                 'proyecto': project, "error": err },
                                                                  context_instance=RequestContext(request))

            mensaje ='Fase: ' + Fase.objects.last().nombre + ', creada exitosamente'
            request.method = 'GET'
            return workProject(request, id_proyecto, error=0, message=mensaje)
    else:
        form = NewPhaseForm()
    return render(request, 'fase/createphase.html', {'form': form, 'proyecto': project, 'user': request.user,
                                                     'error': {} })


@login_required()
def changePhase(request, id_fase, error=None, message=None):
    """
    *Vista para la modificacion de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para modificar la fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea modificar.
    :param args: Argumentos para el modelo ``Fase``.
    :param kwargs: Keyword Arguments para la el modelo ``Fase``.
    :return: Proporciona la pagina ``changephase.html`` con el formulario correspondiente.
             Modifica la fase especifica  y luego regresa al menu principal
    """

    try:
        Fase.objects.get(pk=id_fase)
    except Fase.DoesNotExist:
        print 'La fase especificada no existe'
        return

    phase = Fase.objects.get(pk=id_fase)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    tiposDeItem = TipoItem.objects.filter(fase=phase)
    if request.method == 'POST':
        form = ChangePhaseForm(request.POST, instance=phase)
        if form.is_valid():
            form.save()


            return HttpResponseRedirect('/workproject/'+str(project.id))
    else:
        form = ChangePhaseForm(instance=phase)
    return render(request, 'fase/changephase.html', {'phaseForm': form, 'phase': phase, 'project': project,
                                                     'tiposItem': tiposDeItem, 'user': request.user, 'error': error,
                                                     'message': message}, context_instance=RequestContext(request))


@login_required
def confirmar_eliminacion_fase(request, id_fase):
    """
    *Vista para la confirmar la eliminación definitiva de una fase del proyecto.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest - Solicitud de eliminación.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea eliminar.
    :return: Elimina la fase especifica  y luego regresa al menu de fases.
    """
    faseAEliminar = Fase.objects.get(pk=id_fase)
    tiposItem = TipoItem.objects.filter(fase=faseAEliminar)
    return render(request, 'fase/confirmar_eliminacion.html', {'fase': faseAEliminar,
                                                               'tipos': tiposItem},)

@login_required
def deletePhase(request, id_fase):
    """
    *Vista para la eliminación de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para eliminar fases de un proyectos, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea eliminar.
    :return: Elimina la fase especifica  y luego regresa al menu de fases.
    """

    phase = Fase.objects.get(pk=id_fase)
    tiposItem = TipoItem.objects.filter(fase=phase)


    for ti in tiposItem:
        attrs = Atributo.objects.filter(tipoDeItem=ti)
        for attr in attrs:
            attr.delete()
        ti.delete()

    phase_copy = phase
    phase.delete()

    mensaje = 'Fase: ' + phase_copy.nombre + ', eliminada exitosamente'
    return workProject(request, phase_copy.proyecto.id, error=0, message=mensaje )


@login_required
def phaseList(request, id_proyecto):
    """
    *Vista para la listar todas las fases dentro de algún proyecto.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar las fases dentro de los proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema.
    :param args: Argumentos para el modelo ``Fase``.
    :param kwargs: Keyword Arguments para la el modelo ``Fase``.
    :return: Proporciona la pagina ``phaselist.html`` con la lista todas las fases pertenecientes al proyecto especificado
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    phase_actual_project = Fase.objects.filter(proyecto=id_proyecto)
    phase_available = phase_actual_project.values_list('id', flat=True)

    phase = Fase.objects.exclude(pk__in=phase_available)
    return render(request, "fase/phaselist.html", {'phase': phase, 'project': project },
                  context_instance=RequestContext(request) )


#TODO: No debería existir caso particular de importar multiples fases
@login_required
def importPhase(request, id_fase, id_proyecto_destino):
    """
    *Vista para la importación de un tipo de ítem a otra fase*
    """

    phase = Fase.objects.get(pk=id_fase)
    phase.id = None
    phase.proyecto = Proyecto.objects.get(pk=id_proyecto_destino)
    project = phase.proyecto

    try:
        phase.save()
    except IntegrityError as e:
        return render(request, "keyduplicate_fase.html", {'project': project, "message": e.message },
          context_instance=RequestContext(request) )

    # logger.info('El usuario '+ request.user.username +' ha importado la fase '+  phase.nombre +
    #             ' al proyecto destino: ' + phase.proyecto.nombre)


    return HttpResponseRedirect('/changephase/' + str(phase.id))


#TODO: Revisar funcional pero ineficiente
@login_required
def importMultiplePhase(request, id_fase, id_proyecto_destino):
    """
    *Vista para la importación de un tipo de ítem a otra fase*
    """
    phase = Fase.objects.get(pk=id_fase)
    phase.id = None
    phase.proyecto = Proyecto.objects.get(pk=id_proyecto_destino)
    project = phase.proyecto

    try:
        phase.save()
    except IntegrityError as e:
        return render(request, "keyduplicate_fase.html", {'project': project, "message": e.message },
                      context_instance=RequestContext(request))


    return HttpResponseRedirect('/phaselist/' + str(project.id))


def workphase(request, id_fase, error=None, message=None):
    """
    *Vista para el trabajo sobre una fase de un proyecto.
    Opción válida para usuarios asociados a un proyecto, con permisos de trabajo sobre items de la fase en cuestion*

    :param request: HttpRequest necesario para visualizar el área de trabajo de los usuarios en la fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase sobre la cual se trabaja.
    :return: Proporciona la pagina ``workPhase.html``, página dedicada al desarrollo de la fase.
             Vista para el desarrollo de fases
    """

    if request.method == 'GET':
        faseTrabajo = Fase.objects.get(pk=id_fase)
        proyectoTrabajo = faseTrabajo.proyecto
        ti = TipoItem.objects.filter(fase=faseTrabajo)
        itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

        relaciones = {}
        for i in itemsFase:
            try:
                itemRelacionado = ItemRelacion.objects.get(itemHijo=i).itemPadre
                relaciones[i] = itemRelacionado
            except:
                relaciones[i] = None
        return render(request, 'fase/workPhase.html', {'proyecto': proyectoTrabajo, 'fase': faseTrabajo, 'user': request.user,
                                                       'listaItems': itemsFase, 'relaciones': relaciones.items(),
                                                       'error': error, 'message': message})


def subirOrden(request, id_fase):
    fase = Fase.objects.get(pk=id_fase)

    if fase.nro_orden == 1:
        mensaje = 'La fase ya es la primera. No se puede subir más'
    else:
        ordenAnterior = fase.nro_orden - 1
        faseAnterior = Fase.objects.get(proyecto=fase.proyecto, nro_orden=ordenAnterior)
        faseAnterior.nro_orden = fase.nro_orden
        fase.nro_orden = ordenAnterior

        faseAnterior.save()
        fase.save()

        return HttpResponseRedirect('/workproject/' + str(fase.proyecto.id))


def bajarOrden(request, id_fase):
    fase = Fase.objects.get(pk=id_fase)

    if fase.nro_orden == Fase.objects.filter(proyecto=fase.proyecto).count():
        mensaje = 'La fase ya es la última. No se puede bajar más'
    else:
        ordenPosterior = fase.nro_orden + 1
        fasePosterior = Fase.objects.get(proyecto=fase.proyecto, nro_orden=ordenPosterior)
        fasePosterior.nro_orden = fase.nro_orden
        fase.nro_orden = ordenPosterior

        fasePosterior.save()
        fase.save()

        return HttpResponseRedirect('/workproject/' + str(fase.proyecto.id))


def finPhase(request, id_fase):
    """
    Vista para finalizar una fase
    """
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto
    tipoItem = TipoItem.objects.filter(fase=fase)
    items = ItemBase.objects.filter(tipoitem__in=tipoItem)

    message = ''
    error = 0
    if items:
        for item in items:
            if item.estado == 'ACT' or item.estado == 'VAL' or item.estado == 'FIN':
                message = 'Fase:' + fase.nombre + '. No se pudo finalizar. Aun existen items fuera de Linea Base. Verifique esto y vuelva a intentarlo.'
                error = 1
    else:
        error = 1
        message = 'Fase: ' + fase.nombre + '. No se pudo finalizar. No se han creado items en la misma. Verifiquela y vuelva a intentarlo.'

    if error == 0:
        fase.estado = 'FIN'
        fase.save()
        message = 'La fase ha sido Finalizada exitosamente.'

    return vistaDesarrollo(request, proyecto.id, error=error, message=message)


def startPhase(request, id_fase):
    """
    Vista para iniciar una fase
    """
    fase = Fase.objects.get(pk=id_fase)

    fase_anterior = Fase.objects.get(nro_orden=fase.nro_orden-1)
    LB = LineaBase.objects.filter(fase=fase_anterior)
    if LB:
        fase.estado = 'DES'
        fase.save()
        mensaje = 'La fase ' + fase.nombre + ' se ha iniciado coorrectamente.'
        error = 0
        return vistaDesarrollo(request, fase.proyecto.id, error=error, message=mensaje)

    else:
        mensaje = 'La fase ' + fase.nombre + ' no se ha iniciado coorrectamente. Favor verifique la existencia ' \
                                             'de Lineas Base en la Fase Anterior: ' + fase_anterior.nombre
        error = 1
        return vistaDesarrollo(request, fase.proyecto.id, error=error, message=mensaje)


