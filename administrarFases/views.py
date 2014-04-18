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

    :param request:
    :return:
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = NewPhaseForm(request.POST, project)
        if form.is_valid():
            logger.info('El usuario ' + request.user.username + ' ha creado la fase: ' +
                        form["nombre"].value() + ' dentro del proyecto: ' + project.nombre)
            fase = form.save(commit=False)
            fase.proyecto = project
            fase.save()
            return HttpResponseRedirect('/base/')
    else:
        form = NewPhaseForm()
    return render_to_response('fase/createphase.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def changePhase(request, id_fase):
    """
    Vista para la modificacion de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param request:
    :return:
    """

    phase = Fase.objects.get(pk=id_fase)
    if request.method == 'POST':
        form = ChangePhaseForm(request.POST, instance=phase)
        if form.is_valid():
            logger.info('El usuario ' + request.user.username + ' ha modificado la fase ' +
                        phase.nombre + ' dentro del proyecto: ' + phase.proyecto)
            form.save()
            return HttpResponseRedirect('/base/')
    else:
        form = ChangePhaseForm(instance=phase)
    return render_to_response('fase/changephase.html', {'form': form}, context_instance=RequestContext(request))


def deletePhase(request, id_fase):
    phase = Fase.objects.get(pk=id_fase)
    logger.info('El usuario ' + request.user.username + ' ha eliminado la fase ' +
                        phase.nombre + ' dentro del proyecto: ' + phase.proyecto)
    phase.delete()
    return render(request, "base.html",)

@login_required
def phaseList(request):
    phase = Fase.objects.all()
    return render(request, "fase/phaselist.html", {'phase': phase}, )