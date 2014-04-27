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

import logging

logger = logging.getLogger(__name__)


@login_required()
def createProject(request):
    """
    *Vista para la creación de proyectos en el sistema.
    Opción válida para usuarios con rol de ``Administrador``.*

    :param request: HttpRequest necesario para crear proyectos, es la solicitud de la acción.
    :return: Proporciona la pagina ``createproject.html`` con el formulario correspondiente
             Crea el proyecto en el sistema regresando al menu principal
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
    *Vista para la modificación de un proyecto dentro del sistema.
    Opción válida para usuarios con rol de Administrador.*

    :param request: HttpRequest necesario para modificar proyectos, es la solicitud de la acción.
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


@login_required
def projectList(request):
    """
    *Vista para listar todos los proyectos dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar los proyectos, es la solicitud de la acción.
    :return: Proporciona la pagina ``projectlist.html`` con la lista de todos los proyectos existentes en el sistema
    """
    proyectos = ProyectoTablaAdmin( Proyecto.objects.all() )
    RequestConfig(request, paginate={"per_page": 25}).configure(proyectos)
    return render(request, "proyecto/projectlist.html", {'user': request.user, 'proyectos': proyectos}, )


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
    if request.method == 'POST':
        form = setUserToProjectForm(request.POST)
        if form.is_valid():
            usertoproject = form.save(commit=False)
            usertoproject.cod_proyecto = project
            usertoproject.save()
            return HttpResponseRedirect('/projectlist/')
    else:
        form = setUserToProjectForm(instance=project)
    return render('proyecto/setusertoproject.html', {'form': form, 'project': project, 'user': request.user},)


def viewSetUserProject(request, id_proyecto):
    """
    *Vista para visualizar usuarios que se encuentren vinculados a un proyecto*

    :param request: HttpRequest necesario para visualizar los usuarios a proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema.
    :return: Proporciona la pagina ``usersetproject.html`` con la lista de todos los usuarios vinculados al proyecto
             Lista de los usuarios vinculados correctamente al proyecto.
    """
    userproject = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=id_proyecto)
    project = Proyecto.objects.get(pk=id_proyecto)

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



