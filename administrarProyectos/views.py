#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from administrarProyectos.forms import NewProjectForm, ChangeProjectForm, setUserToProjectForm
from django.shortcuts import render_to_response, render
from administrarProyectos.models import Proyecto, UsuariosVinculadosProyectos
from autenticacion.models import Usuario
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@login_required()
def createProject(request):
    """
    Vista para la creación de proyectos en el sistema.
    Opción válida para usuarios con rol de Administrador.

    :param: Recibe la petición request
    :return: Crea el proyecto en el sistema regresando al menu principal
    """
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            logger.info('El usuario ' + request.user.username + ' ha creado el proyecto: ' +
                        form["nombre"].value() + ' dentro del sistema')
            project.fecha_creacion = timezone.now()
            project.save()
            return HttpResponseRedirect('/base/')
    else:
        form = NewProjectForm()
    return render_to_response('proyecto/createproject.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def changeProject(request, id_proyecto):
    """
    Vista para la modificacion de un proyecto dentro del sistema.
    Opción válida para usuarios con rol de Administrador.

    :param: Recibe la petición request y el identificador del proyecto el cual vamos a modificar
    :return: Modifica el proyecto y luego regresa al menu principal
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = ChangeProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el proyecto PR-' +
                        id_proyecto + ' dentro del sistema')
            return HttpResponseRedirect('/base/')
    else:
        form = ChangeProjectForm(instance=project)
    return render_to_response('proyecto/changeproject.html', {'form': form, 'project': project},
                              context_instance=RequestContext(request))


@login_required
def projectlist(request):
    """
    Vista para listar todos los proyectos dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request
    :return: Lista todos los proyectos existentes en el sistema
    """
    project = Proyecto.objects.all()
    return render(request, "proyecto/projectlist.html", {'project': project}, )


def setUserToProject(request, id_proyecto):
    """
    Vista para vincular usuarios a un proyecto existente.

    Acción solo realizada por los usuarios con rol de líder de proyecto
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = setUserToProjectForm(request.POST)
        if form.is_valid():
            usertoproject = form.save(commit=False)
            usertoproject.cod_proyecto = project
            usertoproject.save()
            return HttpResponseRedirect('/base/')
    else:
        form = setUserToProjectForm(instance=project)
    return render_to_response('proyecto/setusertoproject.html', {'form': form, 'project': project},
                              context_instance=RequestContext(request))


def viewSetUserProject(request, id_proyecto):
    """
    Vista para visualizar usuarios que se encuentren vinculados a un proyecto
    """
    userproject = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=id_proyecto)
    project = Proyecto.objects.get(pk=id_proyecto)

    return render(request, "proyecto/usersetproject.html", {'project': project, 'userproject': userproject},
                  context_instance=RequestContext(request))

