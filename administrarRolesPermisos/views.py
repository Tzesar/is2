#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import IntegrityError

from administrarRolesPermisos.forms import NuevoRolForm, RoleObjectPermissionsForm, asignarUsuariosRolForm

from administrarRolesPermisos.models import Rol

from autenticacion.models import Usuario
from administrarProyectos.models import Proyecto, UsuariosVinculadosProyectos
from administrarRolesPermisos.decorators import *
from administrarFases.models import Fase




@login_required
def crearRol(request, id_proyecto):
    """
    *Vista para la creacion de roles en un proyecto.*
    *Permite asignar el ``Rol`` a usuarios vinculados al proyecto*
    *Un ``Rol`` es un conjunto de permisos que son válidos sobre una fase, un ``permiso``*
    *asigna privilegios específicos sobre una ``fase`` dada.*

    :param request: HttpRequest
    :param idProyecto: Clave única del proyecto donde se está creando el ``Rol``.
    :return: Proporciona la pagina createrole.html con los formularios correspondientes: ``NuevoRol`` y ``NuevoRolPermiso``
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = Fase.objects.filter(proyecto=proyecto)

    if request.method == 'POST':
        # Se crea el formulario para crear el rol con los datos del POST
        rolForm = NuevoRolForm(request.POST)

        # Verifica que el rol tenga los datos correctos
        if rolForm.is_valid():
            rol = rolForm.save(commit=False)
            rol.proyecto = proyecto

            # Se crean los formularios para otorgarle al rol los permisos sobre los objetos especificos, proyecto o fases
            grupoForm = RoleObjectPermissionsForm(rol, proyecto, request.POST, field_name='permisosProyecto')
            fasesForms = []
            for fase in fases:
                faseForm = RoleObjectPermissionsForm(rol, fase, request.POST, field_name='permisosFases'+str(fase.id))
                fasesForms.append(faseForm)

            # Se crea el formulario que contiene los usuarios asignados al rol
            asignarUsuariosForm = asignarUsuariosRolForm(request.POST, id_proyecto=id_proyecto)

            # Verifica que los datos de los permisos y los usuarios asociados al rol sean correctos
            if grupoForm.is_valid() and asignarUsuariosForm.is_valid() and not encontrarFormInvalidas(fasesForms):
                # Guarda el rol en la base de datos
                rol.save()

                # Asocia los permisos sobre el proyecto y las fases al rol
                grupoForm.save_obj_perms()
                for faseForm in fasesForms:
                    faseForm.save_obj_perms()

                # Asigna los usuarios al rol
                usuariosRol = asignarUsuariosForm.get_cleaned_data()
                for usuario in usuariosRol:
                    usuarioNuevo = Usuario.objects.get(id=usuario)
                    rol.user_set.add(usuarioNuevo)

                return HttpResponseRedirect('/workproject/'+str(proyecto.id))

    # Crea un grupo temporal para generar los formularios iniciales
    rol = Rol()

    # Formulario para crear un nuevo rol. Definicion de rol en models de esta app.
    rolForm = NuevoRolForm()

    # Formularios para asignar permisos a un rol sobre un objeto especifico.
    # Primer argumento: rol
    # Segundo argumento: objeto especifico
    grupoForm = RoleObjectPermissionsForm(rol, proyecto, field_name='permisosProyecto',
                                          field_label='', attrs={'class': 'form-control proyecto'})
    fasesForms = []
    for fase in fases:
        faseForm = RoleObjectPermissionsForm(rol, fase, field_name='permisosFases'+str(fase.id),
                                             field_label='', attrs={'class': 'form-control fase'})
        fasesForms.append(faseForm)

    # Formulario para asignar usuarios al rol
    # asignarUsuariosForm = asignarUsuariosRolForm(proyecto, initial={'usuarios': [2, ]})
    asignarUsuariosForm = asignarUsuariosRolForm(id_proyecto=id_proyecto)

    return render(request, "rol/createrole.html", {'proyecto': proyecto, 'user': request.user, 'rolForm': rolForm,
                                                   'grupoForm': grupoForm, 'fasesForms': fasesForms,
                                                   'asignarUsuariosForm': asignarUsuariosForm, })


def encontrarFormInvalidas(formsList):
    """
    *Recibe una lista de ``forms`` de cualquier tipo y devuelve una lista de ``forms`` que no son válidos.*

    :param formsList: Una lista de ``Forms``.
    :return formsInvalidos: Una lista de los ``Forms`` que resultaron inválidos, un subconjunto de ``formsList``.
    """

    formsInvalidos = []
    for form in formsList:
        if not form.is_valid():
            formsInvalidos.append(form)

    return formsInvalidos


@login_required
def modificarRol(request, id_proyecto, id_rol):
    """
    *Vista para la modificación de roles en un proyecto.*
    *Permite asignar el ``Rol`` a usuarios vinculados al proyecto*
    *Un ``Rol`` es un conjunto de permisos que son válidos sobre una fase o proyecto, un ``permiso``*
    *asigna privilegios específicos sobre una ``fase`` o ``proyecto`` dados.*

    :param request: HttpRequest
    :param idProyecto: Clave única del proyecto donde se está creando el ``Rol``.
    :param idProyecto: Clave única del ``Rol`` que se está modificando.
    :return: Proporciona la pagina changerole.html con los formularios correspondientes: ````
    """

    rol = Rol.objects.get(id=id_rol)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = Fase.objects.filter(proyecto=proyecto)

    if request.method == 'POST':

        # Se crea el formulario para crear el rol con los datos del POST
        rolForm = NuevoRolForm(request.POST)

        # Verifica que el rol tenga los datos correctos
        if rolForm.is_valid():
            rol = rolForm.save(commit=False)
            rol.proyecto = proyecto

            # Se crean los formularios para otorgarle al rol los permisos sobre los objetos especificos, proyecto o fases
            grupoForm = RoleObjectPermissionsForm(rol, proyecto, request.POST, field_name='permisosProyecto')
            fasesForms = []
            for fase in fases:
                faseForm = RoleObjectPermissionsForm(rol, fase, request.POST, field_name='permisosFases'+str(fase.id))
                fasesForms.append(faseForm)

            # Se crea el formulario que contiene los usuarios asignados al rol
            asignarUsuariosForm = asignarUsuariosRolForm(request.POST, id_proyecto=id_proyecto)

            # Verifica que los datos de los permisos y los usuarios asociados al rol sean correctos
            if grupoForm.is_valid() and asignarUsuariosForm.is_valid() and not encontrarFormInvalidas(fasesForms):
                # Guarda el rol en la base de datos
                rol.save()

                # Asocia los permisos sobre el proyecto y las fases al rol
                grupoForm.save_obj_perms()
                for faseForm in fasesForms:
                    faseForm.save_obj_perms()

                # Asigna los usuarios al rol
                usuariosRol = asignarUsuariosForm.get_cleaned_data()
                for usuario in usuariosRol:
                    usuarioNuevo = Usuario.objects.get(id=usuario)
                    rol.user_set.add(usuarioNuevo)

                return HttpResponseRedirect('/workproject/'+str(proyecto.id))

    # Formulario para crear un nuevo rol. Definicion de rol en models de esta app.
    rolForm = NuevoRolForm(instance=rol)

    # Formularios para asignar permisos a un rol sobre un objeto especifico.
    # Primer argumento: rol
    # Segundo argumento: objeto especifico
    grupoForm = RoleObjectPermissionsForm(rol, proyecto, field_name='permisosProyecto',
                                          field_label='', attrs={'class': 'form-control proyecto'})
    fasesForms = []
    for fase in fases:
        faseForm = RoleObjectPermissionsForm(rol, fase, field_name='permisosFases'+str(fase.id),
                                             field_label='', attrs={'class': 'form-control fase'})
        fasesForms.append(faseForm)

    # Formulario para asignar usuarios al rol
    usuariosRol = list(rol.user_set.all().values_list('id', flat=True))
    asignarUsuariosForm = asignarUsuariosRolForm(id_proyecto=id_proyecto, initial={'usuarios': usuariosRol})

    return render(request, "rol/changerole.html", {'proyecto': proyecto, 'user': request.user, 'rolForm': rolForm,
                                                   'grupoForm': grupoForm, 'fasesForms': fasesForms,
                                                   'asignarUsuariosForm': asignarUsuariosForm, })


@login_required
def eliminarRol(request, id_proyecto, id_rol):
    """
    *Vista para la eliminación de roles en un proyecto.*
    *Permite desasignar a los usuarios del ``Rol``, además de borrar todas las asociaciones entre el rol y los ``permisos``.*

    :param request: HttpRequest
    :param idProyecto: Clave única del proyecto donde se está borrando el ``Rol``.
    :param idProyecto: Clave única del ``Rol`` que se está eliminando.
    :return: Redirige a la página ``/workproject/`` en cuestión.
    """

    rol = Rol.objects.get(pk=id_rol)
    proyecto = Proyecto.objects.get(pk=id_proyecto)

    rol.delete()

    return HttpResponseRedirect('/workproject/'+str(proyecto.id))


@login_required()
def accesoDenegado(request, id_error):
    """
    *Vista que muestra un mensaje de acceso denegado. Es utilizada por los decoradores ``admin_requerido`` y ``lider_requerido``.*
    *El mensaje de error mostrado depende del argumento ``id_error``. Donde 1 significa que el usuario necesita ser
    ``Administrador`` para ver el contenido de la vista, y 2 que significa que el usuario debe ser ``Líder`` del proyecto
    al cual afecta la vista.*

    :param request: HttpRequest
    :param id_error: Identificador del error encontrado.
    :return: Redirige a la página ``/acceso_denegado/`` en cuestión.
    """

    if id_error == str(1):
        return render(request, 'acceso_denegadoAdmin.html')

    return render(request, 'acceso_denegadoLider.html')