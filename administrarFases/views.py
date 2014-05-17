#encoding:utf-8
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render

from administrarFases.forms import NewPhaseForm, ChangePhaseForm
from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
from administrarTipoItem.models import TipoItem, Atributo
from django.db import IntegrityError

# logger = logging.getLogger(__name__)


@login_required()
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

            try:
                fase.save()
            except IntegrityError as e:
                return render(request, "keyduplicate_fase.html", {'project': project, "message": e.message },
                  context_instance=RequestContext(request) )

            # logger.info('El usuario ' + request.user.username + ' ha creado la fase ' +
            #             form["nombre"].value() + ' dentro del proyecto ' + project.nombre)

            # generarPermisosFase(project, fase)

            return HttpResponseRedirect('/workproject/'+str(project.id))
    else:
        form = NewPhaseForm()
    return render(request, 'fase/createphase.html', {'form': form, 'proyecto': project, 'user': request.user,})


#TODO: Botones Iniciar Fase - Finalizar Fase
@login_required()
def changePhase(request, id_fase):
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

            # logger.info('El usuario ' + request.user.username + ' ha modificado la fase PH-' +
            #             id_fase + ': ' + form["nombre"].value() + ' dentro del proyecto' + project.nombre + 'en el sistema.')

            return HttpResponseRedirect('/workproject/'+str(project.id))
    else:
        form = ChangePhaseForm(instance=phase)
    return render(request, 'fase/changephase.html', {'phaseForm': form, 'phase': phase, 'project': project, 'tiposItem': tiposDeItem, 'user': request.user},
                              context_instance=RequestContext(request))


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

    # eliminarPermisos(phase)

    for ti in tiposItem:
        attrs = Atributo.objects.filter(tipoDeItem=ti)
        for attr in attrs:
            attr.delete()
        ti.delete()

    phase_copy = phase
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    phase.delete()

    # logger.info('El usuario '+ request.user.username +' ha eliminado la fase '+ phase_copy.nombre +
    #             ' dentro del proyecto: ' + project.nombre)

    return HttpResponseRedirect('/workproject/'+str(project.id))


@login_required
# @lider_requerido
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
          context_instance=RequestContext(request) )

    # logger.info('El usuario '+ request.user.username +' ha importado la fase '+  phase.nombre +
    #             ' al proyecto destino: ' + phase.proyecto.nombre)


    return HttpResponseRedirect('/phaselist/' + str(project.id))