#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, RequestContext, render_to_response
from administrarRolesPermisos.forms import NewRoleForm, ChangeRoleForm, AsignRoleForm
from administrarRolesPermisos.models import RolFase, PermisoFase
from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
from autenticacion.models import Usuario
from administrarProyectos.models import UsuariosVinculadosProyectos
from administrarRolesPermisos.decorators import *

import logging

logger = logging.getLogger(__name__)


@login_required
@lider_requerido
def createRole(request, id_proyecto):
    """
    Vista para la creacion de roles en un proyecto.

    :param request: HttpRequest
    :return: Proporciona la pagina createrole.html con el formulario correspondiente:
    """

    project = Proyecto.objects.get(pk=id_proyecto)
    fases = Fase.objects.filter(proyecto=project)
    if request.method == 'POST':
        form = NewRoleForm(request.POST)
        form.fields['permisos'].queryset = PermisoFase.objects.filter(fase__in=fases)
        if form.is_valid():
            rol = form.save(commit=False)
            rol.proyecto = project
            rol.save()
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha creado el rol: ' +
                        form["nombre"].value() + ' en el proyecto' + project.nombre)

            roles = RolFase.objects.filter(proyecto=id_proyecto).order_by('id')

            return render(request, "rol/rolelist.html", {'roles': roles, 'project': project, })
    else:
        form = NewRoleForm()
        form.fields['permisos'].queryset = PermisoFase.objects.filter(fase__in=fases)

    return render(request, "rol/createrole.html", {'form': form, 'project': project, })


# TODO: eliminar si es necesario
def roleList(request, id_proyecto):
    if request.method == 'GET':
        roles = RolFase.objects.filter(proyecto=id_proyecto).order_by('id')
        project = Proyecto.objects.get(pk=id_proyecto)
        return render(request, "rol/rolelist.html", {'roles': roles, 'project': project}, )


@login_required
@lider_requerido
def changeRole(request, id_proyecto, id_rol):
    """
    Vista para la modificacion de un rol dentro de un proyecto
    Opción válida para usuarios con rol Líder de Proyecto.

    :param request:
    :return:
    """
    rol = RolFase.objects.get(pk=id_rol)
    project = Proyecto.objects.get(pk=id_proyecto)
    fases = Fase.objects.filter(proyecto=project)

    if request.method == 'POST':
        form = ChangeRoleForm(request.POST, instance=rol)
        form.fields['permisos'].queryset = PermisoFase.objects.filter(fase__in=fases)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el rol: ' +
                        form["nombre"].value())

            roles = RolFase.objects.filter(proyecto=id_proyecto).order_by('id')
            return render(request, "rol/rolelist.html", { 'roles': roles, 'project': project, })
    else:
        form = ChangeRoleForm(instance=rol)
        form.fields['permisos'].queryset = PermisoFase.objects.filter(fase__in=fases)

    return render_to_response('rol/changerole.html', {'form': form, 'rol': rol, 'project': project}, context_instance=RequestContext(request))


@login_required
@lider_requerido
def deleteRole(request, id_proyecto, id_rol):
    rol = RolFase.objects.get(pk=id_rol)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    logger.info('El usuario ' + request.user.username + ' ha eliminado el rol ' +
                        rol.nombre + ' dentro del proyecto: ' + proyecto.nombre)
    rol.delete()

    roles = RolFase.objects.filter(proyecto=id_proyecto).order_by('id')
    return render(request, "rol/rolelist.html", { 'roles': roles, 'project': proyecto, })


@login_required
@lider_requerido
def asignRole(request, id_proyecto, id_rol):

    rol = RolFase.objects.get(pk=id_rol)
    project = Proyecto.objects.get(pk=id_proyecto)

    usuariosVinculados = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=project).values_list('cod_usuario', flat=True)


    if request.method == 'POST':
        form = AsignRoleForm(request.POST, instance=rol)
        form.fields['roles_usuarios'].queryset = Usuario.objects.filter(pk__in=usuariosVinculados)
        if form.is_valid():
            form.save()

            roles = RolFase.objects.filter(proyecto=id_proyecto).order_by('id')
            return render(request, "rol/rolelist.html", { 'roles': roles, 'project': project, })
    else:
        form = AsignRoleForm(instance=rol)
        form.fields['roles_usuarios'].queryset = Usuario.objects.filter(pk__in=usuariosVinculados)

    return render_to_response('rol/asignrole.html', {'form': form, 'rol': rol, 'project': project}, context_instance=RequestContext(request))


def accesoDenegado(request, id_error):
    print id_error
    if id_error == str(1):
        return render(request, 'acceso_denegadoAdmin.html')

    return render(request, 'acceso_denegadoLider.html')