#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django_tables2 import RequestConfig
from administrarProyectos.forms import NewProjectForm, ChangeProjectForm, setUserToProjectForm
from administrarProyectos.models import Proyecto, UsuariosVinculadosProyectos
from administrarProyectos.tables import ProyectoTablaAdmin
from administrarFases.models import Fase
from administrarRolesPermisos.models import RolGeneral, RolFase
from autenticacion.models import Usuario
from administrarRolesPermisos.decorators import *

import logging

logger = logging.getLogger(__name__)


@login_required()
@admin_requerido
def createProject(request):
    """
    *Vista para la creación de proyectos en el sistema.
    Opción válida para usuarios con rol de ``Administrador``.*

    :param request: HttpRequest necesario para crear proyectos, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``Proyecto``.
    :param kwargs: Keyword Arguments para la el modelo ``Proyecto``.
    :return: Proporciona la pagina ``createproject.html`` con el formulario correspondiente
             Crea el proyecto en el sistema regresando al menu principal
    """
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha creado el proyecto: ' +
                        form["nombre"].value() + ' dentro del sistema')

            vincularLider(form["nombre"].value(), form["lider_proyecto"].value())

            return HttpResponseRedirect('/main/')
    else:
        form = NewProjectForm()
    return render(request, 'proyecto/createproject.html', {'user': request.user, 'form': form})


def vincularLider(nombre_proyecto, lider_code):
    project = Proyecto.objects.get(nombre=nombre_proyecto)
    lider = Usuario.objects.get(pk=lider_code)
    vinculo = UsuariosVinculadosProyectos(cod_usuario=lider, cod_proyecto=project, habilitado=True)
    vinculo.save()


@login_required()
@admin_requerido
def changeProject(request, id_proyecto):
    """
    *Vista para la modificación de un proyecto dentro del sistema.
    Opción válida para usuarios con rol de Administrador.*

    :param request: HttpRequest necesario para modificar proyectos, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``Proyecto``.
    :param kwargs: Keyword Arguments para la el modelo ``Proyecto``.
    :return: Proporciona la pagina ``changeproject.html`` con el formulario correspondiente
             Modifica el proyecto y luego regresa al menu principal
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    users = Usuario.objects.filter(is_active=True)
    if request.method == 'POST':
        form = ChangeProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el proyecto PR-' +
                        id_proyecto + ' dentro del sistema')
            return HttpResponseRedirect('/projectlist/')
    else:
        form = ChangeProjectForm(instance=project)
    return render(request, 'proyecto/changeproject.html', {'user': request.user, 'form': form, 'project': project, 'users': users})


@login_required()
@admin_requerido
def projectList(request):
    """
    *Vista para listar todos los proyectos dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar los proyectos, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``Proyecto``.
    :param kwargs: Keyword Arguments para la el modelo ``Proyecto``.
    :return: Proporciona la pagina ``projectlist.html`` con la lista de todos los proyectos existentes en el sistema
    """
    proyectos = ProyectoTablaAdmin( Proyecto.objects.all() )
    RequestConfig(request, paginate={"per_page": 25}).configure(proyectos)
    return render(request, "proyecto/projectlist.html", {'user': request.user, 'proyectos': proyectos}, )


@login_required()
@lider_requerido
def setUserToProject(request, id_proyecto):
    """
    *Vista para vincular usuarios a un proyecto existente.
    Acción solo realizada por los usuarios con rol de ``Líder de proyecto``*

    :param request: HttpRequest necesario para vincular los usuarios a proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema al cual se le vincularán usuarios para su desarrollo.
    :return: Proporciona la pagina ``setusertoproject.html`` con la lista de todos los usuarios existentes en el sistema para listar al proyecto
            Usuarios vinculados correctamente al proyecto.
    """
    project = Proyecto.objects.get(pk=id_proyecto)

    u = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=project)
    #print u
    usersInProject = u.values_list('cod_usuario', flat=True)
    #print usersInProject

    if request.method == 'POST':
        form = setUserToProjectForm(request.POST)
        form.fields['cod_usuario'].queryset = Usuario.objects.exclude(pk__in=usersInProject)
        if form.is_valid():
            usertoproject = form.save(commit=False)
            usertoproject.cod_proyecto = project
            usertoproject.save()
            return HttpResponseRedirect('/main/')
    else:
        form = setUserToProjectForm(instance=project)
        form.fields['cod_usuario'].queryset = Usuario.objects.exclude(pk__in=usersInProject)
    return render(request, 'proyecto/setusertoproject.html', {'form': form, 'project': project, 'user': request.user},)


# TODO: eliminar luego si es necesario
@login_required()
def viewSetUserProject(request, id_proyecto):
    """
    *Vista para visualizar usuarios que se encuentren vinculados a un proyecto*

    :param request: HttpRequest necesario para visualizar los usuarios a proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema.
    :return: Proporciona la pagina ``usersetproject.html`` con la lista de todos los usuarios vinculados al proyecto
             Lista de los usuarios vinculados correctamente al proyecto.
    """

    project = Proyecto.objects.get(pk=id_proyecto)
    userproject = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=id_proyecto)

    return render(request, "proyecto/usersetproject.html", {'project': project, 'userproject': userproject},
                  context_instance=RequestContext(request))


@login_required()
def workProject(request, id_proyecto):
    """
    *Vista para el trabajo sobre un proyecto dentro del sistema.
    Opción válida para usuarios asociados a un proyecto, ya sea como ``Líder de Proyecto`` o como participante.*

    :param request: HttpRequest necesario para visualizar el área de trabajo de los usuarios en un proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema.
    :return: Proporciona la pagina ``workProject.html``, página dedica al desarrollo del proyecto.
             Vista para el desarrollo del proyecto
    """

    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuario = request.user

    if usuario == proyecto.lider_proyecto:
        fases = Fase.objects.none()
        rolesFases = RolFase.objects.filter(proyecto__pk=id_proyecto)
        rolesGenerales = RolGeneral.objects.filter(proyecto__pk=id_proyecto)
        usuariosAsociados = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=id_proyecto)
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                   'fases': fases, 'rolesFases': rolesFases,
                                                                   'rolesGenerales': rolesGenerales,
                                                                   'usuariosAsociados': usuariosAsociados})
    else:
        return render(request, 'proyecto/workProject.html', {'user': request.user, })



