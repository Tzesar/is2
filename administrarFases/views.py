#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from administrarFases.forms import NewPhaseForm, ChangePhaseForm
from django.shortcuts import render_to_response, render, get_object_or_404
from administrarProyectos.models import Proyecto
import logging

logger = logging.getLogger(__name__)


@login_required()
def createPhase(request):
    """
    Vista para la creación de fases en el sistema.
    Opción válida para usuarios con los roles correspondientes.
    :param request:
    :return:
    """
    nom = Proyecto.nombre(pk=1)
    if request.method == 'POST':
        form = NewPhaseForm(request.POST)
        if form.is_valid():
            logger.info('El usuario ' + request.user.username + ' ha creado la fase: ' +
                        form["nombre"].value() + ' dentro del proyecto: ' + nom)
            form.save()
            return HttpResponseRedirect('/base/')
    else:
        form = NewPhaseForm()
    return render_to_response('proyecto/createproject.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def changePhase(request):
    """
    Vista para la modificacion de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.
    :param request:
    :return:
    """

    nombre = 1
    project = get_object_or_404(Proyecto, pk=nombre)
    if request.method == 'POST':
        form = ChangePhaseForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/base/')
    else:
        form = ChangePhaseForm()
    return render_to_response('proyecto/changeproject.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def projectlist(request):
    project = Proyecto.objects.all()
    return render(request, "proyecto/projectlist.html", {'project': project}, )