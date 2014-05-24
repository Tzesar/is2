#encoding:utf-8
import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from administrarItems.models import ItemBase

from administrarProyectos.forms import NewProjectForm, ChangeProjectForm, setUserToProjectForm, ChangeProjectLeaderForm
from administrarProyectos.models import UsuariosVinculadosProyectos
from administrarProyectos.tables import ProyectoTablaAdmin
from administrarRolesPermisos.models import Rol
from administrarRolesPermisos.decorators import *
from administrarFases.models import Fase
from autenticacion.models import Usuario


# logger = logging.getLogger(__name__)


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
            proyectoNuevo = Proyecto.objects.get(nombre=form["nombre"].value())

            # logger.info('El usuario ' + request.user.username + ' ha creado el proyecto: ' +
            #             form["nombre"].value() + ' dentro del sistema')

            vincularLider(proyectoNuevo, form["lider_proyecto"].value())

            return projectList(request, True, False, proyectoNuevo)
    else:
        form = NewProjectForm()
        form.fields["lider_proyecto"].queryset = Usuario.objects.exclude(pk__in=admin)
    return render(request, 'proyecto/createproject.html', {'user': request.user, 'form': form},)


def vincularLider(project, lider_code):
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

            proyectoModificado = Proyecto.objects.get(nombre=form["nombre"].value())
            # logger.info('El usuario ' + request.user.username + ' ha modificado el proyecto PR-' +
            #             id_proyecto + proyectoModificado.nombre + ' dentro del sistema')

            return projectList(request, False, True, proyectoModificado)
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

            return HttpResponseRedirect('/workproject/'+str(project.id))
    else:
        form = ChangeProjectLeaderForm(instance=project)

    return render(request, 'proyecto/changeprojectleader.html', {'user': request.user, 'form': form, 'project': project})


@login_required()
@admin_requerido
def projectList(request, exitoCrear=False, exitoModif=False, proyecto=None):
    """
    *Vista para listar todos los proyectos dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar los proyectos, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``Proyecto``.
    :param kwargs: Keyword Arguments para la el modelo ``Proyecto``.
    :return: Proporciona la pagina ``projectlist.html`` con la lista de todos los proyectos existentes en el sistema
    """
    proyectos = ProyectoTablaAdmin( Proyecto.objects.all().order_by('nombre') )
    RequestConfig(request, paginate={"per_page": 25}).configure(proyectos)
    return render(request, "proyecto/projectlist.html", {'user': request.user, 'proyectos': proyectos, 'exitoCreacion': exitoCrear,
                                                         'exitoModif': exitoModif, 'proyecto': proyecto,}, )


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

    # Obtiene una lista de los usuarios ya vinculados al proyecto y una lista de los usuarios con estado
    # Inactivo dentro del sistema para luego unir las dos listas en una.
    # usuariosExcluidos = list(UsuariosVinculadosProyectos.objects.filter(cod_proyecto=project).values_list('cod_usuario', flat=True))
    # usuariosExcluidos.append(-1,)

    if request.method == 'POST':
        form = setUserToProjectForm(request.POST, id_proyecto=project.id)
        if form.is_valid():
            nuevosUsuariosAsociados = form.get_cleaned_data()
            for idNuevoUsuario in nuevosUsuariosAsociados:
                usuarioVinculado = UsuariosVinculadosProyectos()
                usuarioVinculado.cod_usuario_id = idNuevoUsuario
                usuarioVinculado.cod_proyecto = project
                usuarioVinculado.save()

            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = setUserToProjectForm(id_proyecto=project.id)
    return render(request, 'proyecto/setUserToProject.html', {'form': form, 'projecto': project,
                                                              'usuariosVinculados': UsuariosVinculadosProyectos.objects.filter(cod_proyecto=project),
                                                              'user': request.user},)


@login_required()
def workProject(request, id_proyecto):
    """
    *Vista para el trabajo sobre un proyecto dentro del sistema.
    Opción válida para usuarios asociados a un proyecto, ya sea como* ``Líder de Proyecto`` *o como participante.*

    :param request: HttpRequest necesario para visualizar el área de trabajo de los usuarios en un proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema.
    :param args: Argumentos para el modelo ``Proyecto``.
    :param kwargs: Keyword Arguments para la el modelo ``Proyecto``.
    :return: Proporciona la pagina ``workProject.html``, página dedica al desarrollo del proyecto.
             Vista para el desarrollo del proyecto
    """
    error = None
    message = None

    # Esto sucede cuando se accede normalmente al template
    if request.method == 'GET':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        usuario = request.user
        fases = Fase.objects.filter(proyecto=proyecto).order_by('nro_orden')
        cantFases = fases.count()

        if usuario == proyecto.lider_proyecto:
            roles = Rol.objects.filter(proyecto=proyecto)

            usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
            usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)
            return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': roles, 'cantFases': cantFases,
                                                                       'usuariosAsociados': usuariosAsociados, 'error': error, 'message': message})

        else:
            return HttpResponseRedirect('/desarrollo/' + str(proyecto.id))

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
        usuario = UsuariosVinculadosProyectos.objects.get(cod_usuario=idUsuario, cod_proyecto=id_proyecto)
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


def vistaDesarrollo(request, id_proyecto):
    """
    *Vista para el área de desarrollo del proyecto.*
    *En él se observan las principales fases e ítems que se encuentran en desarrollo dentro del proyecto*

    :param request: HttpRequest necesario para vincular los usuarios a proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto que se encuentra actualmente en desarrollo.
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = Fase.objects.filter(proyecto=proyecto).order_by('nro_orden')
    error = None
    message = None

    itemsPorFase = {}

    for f in fases:
        ti = TipoItem.objects.filter(fase=f)
        itemsPorFase[f.id] = ItemBase.objects.filter(tipoitem__in=ti)

    return render(request, 'proyecto/workProject.html', {'user': request.user, 'proyecto': proyecto, 'fases': fases,
                                                         'itemsPorFase': itemsPorFase.items(), 'error': error, 'message': message})


@login_required()
@lider_requerido
def startProject(request, id_proyecto):
    """
    *Vista para comenzar a desarrollar un proyecto dentro del sistema. *

    :param id_proyecto: Identificador del proyecto, el cual pasa a un estado de Desarrollo
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    roles = Rol.objects.filter(proyecto=proyecto)
    fases = proyecto.fase_set.all().order_by('nro_orden')
    cantFases = fases.count()

    usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
    usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)

    message = ''
    error = 0
    if proyecto.estado != 'PEN':
        message = 'No se puede Iniciar un proyecto que se encuentra en el estado: ' + proyecto.get_estado_display()
        error = 1
    else:
        if roles and fases:
            for f in fases:
                tipos = TipoItem.objects.filter(fase=f)
                if not tipos:
                    error = 1
                else:
                    for t in tipos:
                        atributos = Atributo.objects.filter(tipoDeItem=t)
                        if not atributos:
                            error = 1

            if error == 1:
                message = 'No se dan las condiciones para iniciar el proyecto. Existen fases sin tipos de item,' \
                          ' o tipos de item sin atributos.'
            else:
                proyecto.estado = 'ACT'
                proyecto.fecha_inicio = timezone.now()
                proyecto.save()

                primeraFase = Fase.objects.get(proyecto=proyecto, nro_orden=1)
                primeraFase.estado = 'DES'
                primeraFase.save()

                message = 'El proyecto ha sido iniciado exitosamente.'
        else:
            message = 'Debe especificar al menos un rol y una fase para que el proyecto se considere válido y pueda iniciarse.'
            error = 1

    fases = proyecto.fase_set.all().order_by('nro_orden')
    return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                'fases': fases, 'roles': roles, 'cantFases': cantFases,
                                                                'usuariosAsociados': usuariosAsociados,
                                                                'message': message, 'error': error})


@login_required()
@lider_requerido
def cancelProject(request, id_proyecto):
    """
    *Vista para cancelar un proyecto dentro del sistema. *

    :param id_proyecto: Identificador del proyecto, el cual pasa a un estado de Anulado
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = proyecto.fase_set.all().order_by('id')
    roles = Rol.objects.filter(proyecto=proyecto)

    usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
    usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)

    #TODO: Insertar mensajes de exitos/fallos en el template
    if proyecto.estado == 'ANU':
        message = 'No se puede anular un proyecto que ya se encuentra anulado'
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': roles,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

    elif proyecto.estado == 'FIN':
        message = 'No se puede anular un proyecto que ya se encuentra finalizado'
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': roles,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

    elif proyecto.estado == 'ACT':
        message = 'No se puede anular un proyecto que se encuentra en estado ACTIVO. Favor comunicarse con el Administrador'
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': roles,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

    else:
        proyecto.estado = 'ANU'
        proyecto.save()
        error = 0
        message = 'El proyecto ha sido anulado'
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': roles,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})


@login_required()
@lider_requerido
def finProject(request, id_proyecto):
    """
    *Vista para finalizar un proyecto dentro del sistema. *

    :param id_proyecto: Identificador del proyecto, el cual pasa a un estado de Finalizado
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = proyecto.fase_set.all().order_by('nro_orden')
    cantFases = fases.count()
    roles = Rol.objects.filter(proyecto=proyecto)

    usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
    usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)

    for fase in fases:
        if fase.estado != 'FIN':
            message = 'No se puede Finalizar el Proyecto. Aún existen fases en desarrollo'
            error = 1
            return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                'fases': fases, 'roles': roles, 'cantFases': cantFases,
                                                                'usuariosAsociados': usuariosAsociados,
                                                                'message': message, 'error': error})

    if proyecto.estado != 'ACT':
        message = 'No se puede Finalizar un proyecto que se encuentra en el estado: ' + proyecto.get_estado_display()
        error = 1
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': roles, 'cantFases': cantFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})

    else:
        proyecto.estado = 'FIN'
        proyecto.fecha_inicio = timezone.now()
        proyecto.save()
        message = 'El proyecto ha sido Finalizdo exitosamente.'
        error = 0
        return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'roles': roles, 'cantFases': cantFases,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'message': message, 'error': error})


