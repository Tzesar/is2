#encoding:utf-8
import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from administrarItems.models import ItemBase

from administrarProyectos.forms import NewProjectForm, ChangeProjectForm, setUserToProjectForm, ChangeProjectLeaderForm
from administrarProyectos.models import UsuariosVinculadosProyectos, Proyecto
from administrarProyectos.tables import ProyectoTablaAdmin
from administrarRolesPermisos.decorators import user_passes_test, vinculadoProyecto, admin_requerido, puede_trabajar
from administrarRolesPermisos.forms import asignarUsuariosRolForm, asignarMiembrosComiteForm
from administrarRolesPermisos.models import Rol
from administrarFases.models import Fase
from administrarTipoItem.models import TipoItem, Atributo
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

    admin = request.user

    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        form.fields["lider_proyecto"].queryset = Usuario.objects.exclude(pk__in=(admin.id, -1), is_active=True)
        if form.is_valid():
            form.save()
            proyectoNuevo = Proyecto.objects.get(nombre=form["nombre"].value())

            # logger.info('El usuario ' + request.user.username + ' ha creado el proyecto: ' +
            #             form["nombre"].value() + ' dentro del sistema')

            vincularLider(proyectoNuevo, form["lider_proyecto"].value())

            # Crea el rol Comite de cambios y asigna al Lider a este grupo.
            grupoComite = Group(name="ComiteDeCambios-"+str(proyectoNuevo.nombre))
            grupoComite.save()
            rolComite = Rol(grupo=grupoComite, proyecto=proyectoNuevo)
            rolComite.save()

            grupoComite.user_set.add(proyectoNuevo.lider_proyecto)

            return HttpResponseRedirect('/projectlist/')
    else:
        form = NewProjectForm()
        form.fields["lider_proyecto"].queryset = Usuario.objects.exclude(pk__in=(admin.id, -1), is_active=True)
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
        liderAnterior = project.lider_proyecto
        form = ChangeProjectForm(request.POST, instance=project)
        if form.is_valid():
            if 'lider_proyecto' in form.changed_data:
                liderNuevo = form.cleaned_data['lider_proyecto']

                nombreComite = u'ComiteDeCambios-'+project.nombre
                comite = Rol.objects.get(grupo__name__contains=nombreComite)

                comite.grupo.user_set.remove(liderAnterior)
                comite.grupo.user_set.add(liderNuevo)
            form.save()

            proyectoModificado = Proyecto.objects.get(nombre=form["nombre"].value())
            # logger.info('El usuario ' + request.user.username + ' ha modificado el proyecto PR-' +
            #             id_proyecto + proyectoModificado.nombre + ' dentro del sistema')

            return projectList(request, False, True, proyectoModificado)
    else:
        form = ChangeProjectForm(instance=project)
    return render(request, 'proyecto/changeproject.html', {'user': request.user, 'form': form, 'project': project})


@login_required()
# @lider_requerido
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
    nombreComite = u'ComiteDeCambios-' + str(project.nombre)
    rol = Rol.objects.get(grupo__name__contains=nombreComite)

    if request.method == 'POST':
        form = ChangeProjectLeaderForm(request.POST, instance=project)
        miembrosComiteForm = asignarMiembrosComiteForm(request.POST, id_proyecto=id_proyecto,
                                                       id_lider=project.lider_proyecto_id)
        if form.is_valid() and miembrosComiteForm.is_valid():
            form.save()

            miembrosComite = miembrosComiteForm.get_cleaned_data()
            rol.grupo.user_set.clear()
            for miembro in miembrosComite:
                miembroNuevo = Usuario.objects.get(id=miembro)
                rol.grupo.user_set.add(miembroNuevo)

            # logger.info('El Lider de Proyecto ' + request.user.username + ' ha modificado el proyecto PR-' +
            #             id_proyecto + form["nombre"].value() + ' dentro del sistema')

            messages = []
            messages.append(u'El proyecto se ha modificado correctamente.')
            request.session['messages'] = messages
            return HttpResponseRedirect(reverse('administrarProyectos.views.workProject', kwargs={'id_proyecto': id_proyecto}))


    form = ChangeProjectLeaderForm(instance=project)

    miembrosComite = list(rol.grupo.user_set.all().values_list('id', flat=True))
    miembrosComiteForm = asignarMiembrosComiteForm(id_proyecto=id_proyecto, id_lider=project.lider_proyecto_id,
                                                   initial={'miembros': miembrosComite})
    return render(request, 'proyecto/changeprojectleader.html', {'user': request.user, 'form': form, 'project': project,
                                                                 'miembrosComiteForm': miembrosComiteForm})


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

    proyectos = ProyectoTablaAdmin(Proyecto.objects.all().order_by('nombre'))
    RequestConfig(request, paginate={"per_page": 25}).configure(proyectos)
    return render(request, "proyecto/projectlist.html", {'user': request.user, 'proyectos': proyectos}, )


@login_required()
# @lider_requerido
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

    # Obtiene una lista de los usuarios ya vinculados al proyecto y una lista de los usuarios con estado
    # Inactivo dentro del sistema para luego unir las dos listas en una.

    if request.method == 'POST':
        form = setUserToProjectForm(request.POST, id_proyecto=project.id)
        if form.is_valid():
            nuevosUsuariosAsociados = form.get_cleaned_data()
            for idNuevoUsuario in nuevosUsuariosAsociados:
                usuarioVinculado = UsuariosVinculadosProyectos()
                usuarioVinculado.cod_usuario_id = idNuevoUsuario
                usuarioVinculado.cod_proyecto = project
                usuarioVinculado.save()

            return HttpResponseRedirect(reverse('administrarProyectos.views.workProject', kwargs={'id_proyecto': id_proyecto}))
    else:
        form = setUserToProjectForm(id_proyecto=project.id)
    return render(request, 'proyecto/setUserToProject.html', {'form': form, 'projecto': project,
                                                              'usuariosVinculados': UsuariosVinculadosProyectos.objects.filter(cod_proyecto=project),
                                                              'user': request.user},)


@login_required()
@user_passes_test(vinculadoProyecto)
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
        fases = Fase.objects.filter(proyecto=proyecto).order_by('nro_orden')

        if usuario == proyecto.lider_proyecto:
            cantFases = fases.count()
            roles = Rol.objects.filter(proyecto=proyecto)[1:]

            usuariosInactivos = Usuario.objects.filter(is_active=False).values_list('id', flat=True)
            usuariosAsociados = proyecto.usuariosvinculadosproyectos_set.exclude(cod_usuario__in=usuariosInactivos)

            error = None
            messages = None
            if 'error' in request.session:
                error = request.session.pop('error')
            if 'messages' in request.session:
                messages = request.session.pop('messages')
            return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,
                                                                       'fases': fases, 'cantFases': cantFases, 'roles': roles,
                                                                       'usuariosAsociados': usuariosAsociados,
                                                                       'error': error, 'messages': messages})
        else:
            return render(request, 'proyecto/workProject.html', {'user': request.user, 'proyecto': proyecto, 'fases': fases, })

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
    # TODO: cancelar todas las solicitudes de cambio creadas por este usuario

    if xhr:
        responseDict = {'exito': True}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')


@user_passes_test(puede_trabajar)
def vistaDesarrollo(request, id_proyecto):
    """
    * Vista para el área de desarrollo del proyecto.*
    * En él se observan las principales fases e ítems que se encuentran en desarrollo dentro del proyecto*
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = Fase.objects.filter(proyecto=proyecto).order_by('nro_orden')

    itemsPorFase = {}

    for f in fases:
        ti = TipoItem.objects.filter(fase=f)
        itemsPorFase[f.id] = ItemBase.objects.filter(tipoitem__in=ti)

    error = None
    messages = None
    if 'error' in request.session:
        error = request.session.pop('error')
    if 'messages' in request.session:
        messages = request.session.pop('messages')
    return render(request, 'proyecto/workProject.html', {'user': request.user, 'proyecto': proyecto, 'fases': fases,
                                                         'itemsPorFase': itemsPorFase.items(), 'error': error, 'messages': messages})


@login_required()
# @lider_requerido
def startProject(request, id_proyecto):
    """
    *Vista par iniciar un proyecto*
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    roles = Rol.objects.filter(proyecto=proyecto)
    fases = proyecto.fase_set.all().order_by('nro_orden')
    cantFases = fases.count()

    message = []
    error = 0
    if proyecto.estado != 'PEN':
        message = 'No se puede Iniciar un proyecto que se encuentra en el estado: ' + proyecto.get_estado_display()
        error = 1
    else:
        if roles and fases:
            for fase in fases:
                tipos = TipoItem.objects.filter(fase=fase)
                if not tipos:
                    error = 1
                    message.append('La fase ' + fase.nombre + ' debe tener un Tipo de Item asociado.')
                else:
                    for tipo in tipos:
                        atributos = Atributo.objects.filter(tipoDeItem=tipo)
                        if not atributos:
                            error = 1
                            message.append('El tipo de item ' + tipo.nombre + ' debe tener por lo menos un atributo'
                                                                              ' definido por el usuario.')
        else:
            message.append(u'Debe especificar al menos un rol y una fase para que el proyecto se considere válido'
                           u' y pueda iniciarse.')
            error = 1

        nombreComite = u'ComiteDeCambios-' + proyecto.nombre
        comite = Rol.objects.get(grupo__name__contains=nombreComite)
        if comite.grupo.user_set.all().count() < 3:
            message.append(u'El Comite de cambios debe tener tres miembros.')
            error = 1

        if error != 1:
            proyecto.estado = 'ACT'
            proyecto.fecha_inicio = timezone.now()
            proyecto.save()

            primeraFase = Fase.objects.get(proyecto=proyecto, nro_orden=1)
            primeraFase.estado = 'DES'
            primeraFase.save()

            message.append(u'El proyecto ha sido iniciado exitosamente.')

    request.session['messages'] = message
    request.session['error'] = error
    return HttpResponseRedirect(reverse('administrarProyectos.views.workProject', kwargs={'id_proyecto': id_proyecto}))


@login_required()
# @lider_requerido
def cancelProject(request, id_proyecto):
    """
    *Vista para anular un proyecto*
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)

    messages = []
    #TODO: Insertar mensajes de exitos/fallos en el template
    if proyecto.estado == 'ANU':
        messages.append('No se puede anular un proyecto que ya se encuentra anulado')
        error = 1
    elif proyecto.estado == 'FIN':
        messages.append('No se puede anular un proyecto que ya se encuentra finalizado')
        error = 1
    elif proyecto.estado == 'ACT':
        messages.append('No se puede anular un proyecto que se encuentra en estado ACTIVO. Favor comunicarse con el Administrador')
        error = 1
    else:
        proyecto.estado = 'ANU'
        proyecto.save()
        error = 0
        messages.append('El proyecto ha sido anulado')

    request.session['messages'] = messages
    request.session['error'] = error
    return HttpResponseRedirect(reverse('administrarProyectos.views.workProject', kwargs={'id_proyecto': id_proyecto}))
    # return render(request, 'proyecto/workProjectLeader.html', {'user': request.user, 'proyecto': proyecto,


@login_required()
# @lider_requerido
def finProject(request, id_proyecto):
    """
    *Vista par inicar un proyecto*
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = proyecto.fase_set.all().order_by('nro_orden')

    error = 0
    messages = []
    for fase in fases:
        if fase.estado != 'FIN':
            messages.append('No se puede Finalizar el Proyecto. Aún existen fases en desarrollo')
            error = 1
    if proyecto.estado != 'ACT':
        message = 'No se puede Finalizar un proyecto que se encuentra en el estado: ' + proyecto.get_estado_display()
        messages.append(message)
        error = 1
    else:
        proyecto.estado = 'FIN'
        proyecto.fecha_inicio = timezone.now()
        proyecto.save()
        messages.append('El proyecto ha sido Finalizdo exitosamente.')
        error = 0

    request.session['messages'] = messages
    request.session['error'] = error
    return HttpResponseRedirect(reverse('administrarProyectos.views.workProject', kwargs={'id_proyecto': id_proyecto}))