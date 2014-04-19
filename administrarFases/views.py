#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from administrarFases.forms import NewPhaseForm, ChangePhaseForm
from django.shortcuts import render_to_response, render, get_object_or_404
from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
import logging

logger = logging.getLogger(__name__)


@login_required()
def createPhase(request, id_proyecto):
    """
    Vista para la creación de fases en el sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request y el identificador del Proyecto, de tal manera a identificar el proyecto a la cual pertence la fase.
    :return: Crea la fase dentro del proyecto especificando y luego regresa al menu principal
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = NewPhaseForm(request.POST, project)
        if form.is_valid():
            fase = form.save(commit=False)
            fase.proyecto = project
            fase.save()
            logger.info('El usuario ' + request.user.username + ' ha creado la fase ' +
                        form["nombre"].value() + ' dentro del proyecto ' + project.nombre)
            return HttpResponseRedirect('/base/')
    else:
        form = NewPhaseForm()
    return render_to_response('fase/createphase.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def changePhase(request, id_fase):
    """
    Vista para la modificacion de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request y el identificador de la fase la cual vamos a modificar
    :return: Modifica la fase especifica  y luego regresa al menu principal
    """

    phase = Fase.objects.get(pk=id_fase)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    if request.method == 'POST':
        form = ChangePhaseForm(request.POST, instance=phase)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado la fase con codigo  PH-' +
                        id_fase + ' dentro del proyecto: ' + project.nombre)
            return HttpResponseRedirect('/base/')
    else:
        form = ChangePhaseForm(instance=phase)
    return render_to_response('fase/changephase.html', {'form': form, 'phase': phase, 'project': project},
                              context_instance=RequestContext(request))


def deletePhase(request, id_fase):
    """
    Vista para la eliminación de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request y el identificador de la fase la cual deseamos modificar
    :return: Elimina la fase especifica en el proyecto y luego regresa al menu principal
    """
    phase = Fase.objects.get(pk=id_fase)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    logger.info('El usuario {0} ha eliminado la fase {1}{2} dentro del proyecto: {3}'.format(request.user.username,
                                                                                             phase.proyecto,
                                                                                             phase.nombre,
                                                                                             project.nombre))
    phase.delete()
    return render(request, "base.html",)

@login_required
def phaseList(request, id_proyecto):
    """
    Vista para la listar todas las fases dentro de algún proyecto.
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request y el identificado de proyecto, para listar todas las fases pertenecientes al proyecto especificado
    :return: Lista todas las fases pertenecientes al proyecto especificado
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    phase = Fase.objects.filter(proyecto=id_proyecto)
    return render(request, "fase/phaselist.html", {'phase': phase, 'project':project }, context_instance=RequestContext(request) )