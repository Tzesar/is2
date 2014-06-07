#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import Group

from administrarRolesPermisos.forms import NuevoRolForm, RoleObjectPermissionsForm, asignarUsuariosRolForm
from administrarRolesPermisos.models import Rol
from autenticacion.models import Usuario
from administrarRolesPermisos.decorators import *
from administrarFases.models import Fase


@lider_requerido("id_proyecto")
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
        rolGrupoForm = NuevoRolForm(request.POST)

        # Verifica que el grupo del rol tenga los datos correctos
        if rolGrupoForm.is_valid():
            rolGrupo = rolGrupoForm.save(commit=False)

            # Se crean los formularios para otorgarle al rol los permisos sobre los objetos especificos, proyecto o fases
            grupoPermisosForm = RoleObjectPermissionsForm(rolGrupo, proyecto, request.POST, field_name='permisosProyecto')
            fasesForms = []
            for fase in fases:
                faseForm = RoleObjectPermissionsForm(rolGrupo, fase, request.POST, field_name='permisosFases'+str(fase.id))
                fasesForms.append(faseForm)

            # Se crea el formulario que contiene los usuarios asignados al rol
            asignarUsuariosForm = asignarUsuariosRolForm(request.POST, id_proyecto=id_proyecto)

            # Verifica que los datos de los permisos y los usuarios asociados al rol sean correctos
            if grupoPermisosForm.is_valid() and asignarUsuariosForm.is_valid() and not encontrarFormInvalidas(fasesForms):
                # Guarda el rol en la base de datos
                rolGrupo.save()

                # Asocia los permisos sobre el proyecto y las fases al grupo del rol
                grupoPermisosForm.save_obj_perms()
                for faseForm in fasesForms:
                    faseForm.save_obj_perms()

                # Asigna los usuarios al grupo del rol
                usuariosRol = asignarUsuariosForm.get_cleaned_data()
                for usuario in usuariosRol:
                    usuarioNuevo = Usuario.objects.get(id=usuario)
                    rolGrupo.user_set.add(usuarioNuevo)

                rol = Rol(grupo=rolGrupo, proyecto=proyecto)
                rol.save()

                return HttpResponseRedirect(reverse('administrarProyectos.views.workProject',
                                                    kwargs={'id_proyecto': id_proyecto}))

    # Formulario para crear un nuevo rol. Definicion de rol en models de esta app.
    rolGrupoForm = NuevoRolForm()

    # Crea un grupo temporal para generar los formularios iniciales
    rolGrupo = Group()

    # Formularios para asignar permisos a un rol sobre un objeto especifico.
    # Primer argumento: rol
    # Segundo argumento: objeto especifico
    grupoPermisosForm = RoleObjectPermissionsForm(rolGrupo, proyecto, field_name='permisosProyecto',
                                                  field_label='', attrs={'class': 'form-control proyecto'})
    fasesPermisosForms = []
    for fase in fases:
        faseForm = RoleObjectPermissionsForm(rolGrupo, fase, field_name='permisosFases'+str(fase.id),
                                             field_label='', attrs={'class': 'form-control fase'})
        fasesPermisosForms.append(faseForm)

    # Formulario para asignar usuarios al rol
    # asignarUsuariosForm = asignarUsuariosRolForm(proyecto, initial={'usuarios': [2, ]})
    asignarUsuariosForm = asignarUsuariosRolForm(id_proyecto=id_proyecto)

    return render(request, "rol/createrole.html", {'proyecto': proyecto, 'user': request.user, 'rolGrupoForm': rolGrupoForm,
                                                   'grupoPermisosForm': grupoPermisosForm, 'fasesPermisosForms': fasesPermisosForms,
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
    :param id_proyecto: Clave única del proyecto donde se está creando el ``Rol``.
    :param id_rol: Clave única del ``Rol`` que se está modificando.
    :return: Proporciona la pagina changerole.html con los formularios correspondientes: ````
    """

    rol = Rol.objects.get(id=id_rol)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = Fase.objects.filter(proyecto=proyecto)

    if request.method == 'POST':

        # Se crea el formulario para modificar el rol con los datos del POST
        rolGrupoForm = NuevoRolForm(request.POST, instance=rol.grupo)

        # Verifica que el rol tenga los datos correctos
        if rolGrupoForm.is_valid():
            rolGrupo = rol.grupo

            # Se crean los formularios para otorgarle al rol los permisos sobre los objetos especificos, proyecto o fases
            grupoPermisosForm = RoleObjectPermissionsForm(rolGrupo, proyecto, request.POST, field_name='permisosProyecto')
            fasesForms = []
            for fase in fases:
                faseForm = RoleObjectPermissionsForm(rolGrupo, fase, request.POST, field_name='permisosFases'+str(fase.id))
                fasesForms.append(faseForm)

            # Se crea el formulario que contiene los usuarios asignados al rol
            asignarUsuariosForm = asignarUsuariosRolForm(request.POST, id_proyecto=id_proyecto)

            # Verifica que los datos de los permisos y los usuarios asociados al rol sean correctos
            if grupoPermisosForm.is_valid() and asignarUsuariosForm.is_valid() and not encontrarFormInvalidas(fasesForms):

                # Asocia los permisos sobre el proyecto y las fases al rol
                grupoPermisosForm.save_obj_perms()
                for faseForm in fasesForms:
                    faseForm.save_obj_perms()

                # Asigna los usuarios al rol
                usuariosRol = asignarUsuariosForm.get_cleaned_data()
                rolGrupo.user_set.clear()
                for usuario in usuariosRol:
                    usuarioNuevo = Usuario.objects.get(id=usuario)
                    rolGrupo.user_set.add(usuarioNuevo)

                messages = []
                message = 'Rol ' + rol.grupo.name + ' modificado exitosamente.'
                error = 0
                messages.append(message)
                request.session['messages'] = messages
                request.session['error'] = error
                return HttpResponseRedirect(reverse('administrarProyectos.views.workProject',
                                                    kwargs={'id_proyecto': id_proyecto}))

    # Formulario para crear un nuevo rol. Definicion de rol en models de esta app.
    rolGrupoForm = NuevoRolForm(instance=rol.grupo)

    # Formularios para asignar permisos a un grupo sobre un objeto especifico, este grupo es luego asociado a
    # un rol.
    # Primer argumento: grupo
    # Segundo argumento: objeto especifico
    grupoPermisosForm = RoleObjectPermissionsForm(rol.grupo, proyecto, field_name='permisosProyecto',
                                                  field_label='', attrs={'class': 'form-control proyecto'})
    fasesPermisosForms = []
    for fase in fases:
        faseForm = RoleObjectPermissionsForm(rol.grupo, fase, field_name='permisosFases'+str(fase.id),
                                             field_label='', attrs={'class': 'form-control fase'})
        fasesPermisosForms.append(faseForm)

    # Formulario para asignar usuarios al rol
    usuariosRol = list(rol.grupo.user_set.all().values_list('id', flat=True))
    asignarUsuariosForm = asignarUsuariosRolForm(id_proyecto=id_proyecto, initial={'usuarios': usuariosRol})

    return render(request, "rol/changerole.html", {'proyecto': proyecto, 'user': request.user, 'rol': rol,
                                                   'rolGrupoForm': rolGrupoForm, 'grupoPermisosForm': grupoPermisosForm,
                                                   'fasesPermisosForms': fasesPermisosForms,
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
    rol.delete()
    rol.grupo.delete()

    return HttpResponseRedirect(reverse('administrarProyectos.views.workProject', kwargs={'id_proyecto': id_proyecto}))


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