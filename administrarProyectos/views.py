#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig
from administrarProyectos.forms import NewProjectForm, ChangeProjectForm
from administrarProyectos.models import Proyecto
from administrarProyectos.tables import ProyectoTabla
from autenticacion.models import Usuario
import logging

logger = logging.getLogger(__name__)


@login_required()
def createProject(request):
    """
    Vista para la creación de proyectos en el sistema.
    Opción válida para usuarios con rol de Administrador.

    :param request:
    :return:
    """
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha creado el proyecto: ' +
                        form["nombre"].value() + ' dentro del sistema')
            return HttpResponseRedirect('/main/')
    else:
        form = NewProjectForm()
    return render(request, 'proyecto/createproject.html', {'user': request.user, 'form': form})


@login_required()
def changeProject(request, id_proyecto):
    """
    Vista para la modificacion de un proyecto dentro del sistema.
    Opción válida para usuarios con rol de Administrador.

    :param request:
    :return:
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    users = Usuario.objects.filter(is_active=True)
    if request.method == 'POST':
        form = ChangeProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el proyecto: ' +
                        form["nombre"].value() + ' dentro del sistema')
            return HttpResponseRedirect('/main/')
    else:
        form = ChangeProjectForm(instance=project)
    return render(request, 'proyecto/changeproject.html', {'user': request.user, 'form': form, 'project': project, 'users': users})


@login_required
def projectList(request):
    proyectos = ProyectoTabla( Proyecto.objects.all() )
    RequestConfig(request, paginate={"per_page": 25}).configure(proyectos)
    return render(request, "proyecto/projectlist.html", {'user': request.user, 'proyectos': proyectos}, )