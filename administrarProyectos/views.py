#encoding:utf-8
import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from administrarProyectos.forms import NewProjectForm, ChangeProjectForm, setUserToProjectForm, ChangeProjectLeaderForm
from administrarProyectos.models import Proyecto, UsuariosVinculadosProyectos
from administrarProyectos.tables import ProyectoTablaAdmin
from administrarRolesPermisos.models import RolFase
from autenticacion.models import Usuario
from administrarRolesPermisos.decorators import *


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

    admin = Usuario.objects.filter(is_superuser=True)

    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        form.fields["lider_proyecto"].queryset = Usuario.objects.exclude(pk__in=admin)
        if form.is_valid():
            form.save()

            logger.info('El usuario ' + request.user.username + ' ha creado el proyecto: ' +
                        form["nombre"].value() + ' dentro del sistema')

            vincularLider(form["nombre"].value(), form["lider_proyecto"].value())

            return HttpResponseRedirect('/projectlist/')
    else:
        form = NewProjectForm()
        form.fields["lider_proyecto"].queryset = Usuario.objects.exclude(pk__in=admin)
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
    # TODO: Agregar referencia a los autores de autocomplete.js

    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = ChangeProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el proyecto PR-' +
                        id_proyecto + form["nombre"].value() + ' dentro del sistema')
            return HttpResponseRedirect('/projectlist/')
    else:
        form = ChangeProjectForm(instance=project)
    return render(request, 'proyecto/changeproject.html', {'user': request.user, 'form': form, 'project': project})


@login_required()
@lider_requerido
def changeProjectLeader(request, id_proyecto):
    """
    *Vista para la modificación de un proyecto dentro del sistema.
    Opción válida para usuarios con rol de Lider.*

    :param request: HttpRequest necesario para modificar proyectos, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``Proyecto``.
    :param kwargs: Keyword Arguments para la el modelo ``Proyecto``.
    :return: Proporciona la pagina ``changeproject.html`` con el formulario correspondiente
             Modifica el proyecto y luego regresa al menu principal
    """

    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = ChangeProjectLeaderForm(request.POST, instance=project)
        if form.is_valid():
            form.save()

            logger.info('El Lider de Proyecto ' + request.user.username + ' ha modificado el proyecto PR-' +
                        id_proyecto + form["nombre"].value() + ' dentro del sistema')

            return HttpResponseRedirect('/workproject/'+str(project.id))
    else:
        form = ChangeProjectLeaderForm(instance=project)

    return render(request, 'proyecto/changeprojectleader.html', {'user': request.user, 'form': form, 'project': project})


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
    usersInProject = u.values_list('cod_usuario', flat=True)

    if request.method == 'POST':
        form = setUserToProjectForm(request.POST)
        form.fields['cod_usuario'].queryset = Usuario.objects.exclude(pk__in=usersInProject).filter(is_superuser=False)
        if form.is_valid():
            usertoproject = form.save(commit=False)
            usertoproject.cod_proyecto = project
            usertoproject.save()
            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = setUserToProjectForm(instance=project)
        form.fields['cod_usuario'].queryset = Usuario.objects.exclude(pk__in=usersInProject).filter(is_superuser=False)
    return render(request, 'proyecto/setUserToProject.html', {'form': form, 'project': project, 'user': request.user},)


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

    return render(request, "proyecto/usersetproject.html",
                  {'project': project, 'userproject': userproject, 'user': request.user},)

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

    # Esto sucede cuando se accede normalmente al template
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        usuario = request.user

        if usuario == proyecto.lider_proyecto:
            fases = proyecto.fase_set.all().order_by('id')
            rolesFases = RolFase.objects.filter(proyecto=proyecto).order_by('nombre')

            usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
            usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)
            return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': rolesFases,
                                                                       'usuariosAsociados': usuariosAsociados})
        else:
            return render(request, 'proyecto/workProject.html', {'user': request.user, })

    # Esto sucede cuando se modifica el estado de un usuario dentro del proyecto
    #   cuando ajax envia una solicitud con el metodo POST

    xhr = request.GET.has_key('xhr')

    idUsuario = request.POST['usuarioModificado']
    estadoNuevo = request.POST['estadoNuevo']

    if idUsuario and estadoNuevo:
        idUsuario = int(idUsuario)
        if estadoNuevo == 'true':
            estadoNuevo = True
        else:
            estadoNuevo = False
    else:
        responseDict = {'exito': False}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')

    try:
        usuario = UsuariosVinculadosProyectos.objects.get(cod_usuario=idUsuario)
    except ObjectDoesNotExist:
        responseDict = {'exito': False}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')

    if usuario:
        usuario.habilitado = estadoNuevo
    else:
        responseDict = {'exito': False}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')

    usuario.save()

    if xhr:
        responseDict = {'exito': True}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')

@login_required()
@lider_requerido
def startProject(request, id_proyecto):
    """
    *Vista par inicar un proyecto*
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = proyecto.fase_set.all().order_by('id')
    rolesFases = RolFase.objects.filter(proyecto=proyecto).order_by('nombre')

    usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
    usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)

    if proyecto.estado != 'PEN':
        message = 'No se puede Iniciar un proyecto que se encuentra en el estado: ' + proyecto.get_estado_display()
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': rolesFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})
    else:
        proyecto.estado = 'ACT'
        proyecto.fecha_inicio = timezone.now()
        proyecto.save()
        message = 'El proyecto ha sido iniciado exitosamente.'
        error = 0
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': rolesFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

@login_required()
@lider_requerido
def cancelProject(request, id_proyecto):
    """
    *Vista para anular un proyecto*
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = proyecto.fase_set.all().order_by('id')
    rolesFases = RolFase.objects.filter(proyecto=proyecto).order_by('nombre')

    usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
    usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)

    #TODO: Insertar mensajes de exitos/fallos en el template
    if proyecto.estado == 'ANU':
        message = 'No se puede anular un proyecto que ya se encuentra anulado'
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': rolesFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

    elif proyecto.estado == 'FIN':
        message = 'No se puede anular un proyecto que ya se encuentra finalizado'
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': rolesFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

    elif proyecto.estado == 'ACT':
        message = 'No se puede anular un proyecto que se encuentra en estado ACTIVO. Favor comunicarse con el Administrador'
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': rolesFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

    else:
        proyecto.estado = 'ANU'
        proyecto.save()
        error = 0
        message = 'El proyecto ha sido anulado'
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': rolesFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})


@login_required()
@lider_requerido
def finProject(request, id_proyecto):
    """
    *Vista par inicar un proyecto*
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    #TODO: Insertar mensajes de exitos/fallos en el template
    if project.estado == 'ANU':
        return workProject(request, id_proyecto)
    elif project.estado == 'PEN':
        return workProject(request, id_proyecto)
    elif project.estado == 'FIN':
        return workProject(request, id_proyecto)
    else:
        project.estado = 'FIN'
        #TODO: Revisar que todas las fases se encuentren en estado finalizado
        fases = Fase.objects.filter(proyecto=id_proyecto)
        for fase in fases:
            if fase.estado != 'FIN':
                #TODO: con mensaje de fallo al finalizar el proyecto, por que la fase.nombre no esta finalizada
                return workProject(request, id_proyecto)

        project.save()
        return workProject(request, id_proyecto)


