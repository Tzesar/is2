#encoding:utf-8

from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import available_attrs
from guardian.shortcuts import get_perms, get_objects_for_user
from administrarItems.models import ItemBase
from administrarLineaBase.models import SolicitudCambios

from administrarProyectos.models import Proyecto
from administrarProyectos.models import UsuariosVinculadosProyectos
from administrarFases.models import Fase
from autenticacion.models import Usuario


def admin_requerido(function):
    """
    *``Decorador``: Verifica que el usuario actual sea ``Administrador`` antes de concederle acceso a la vista.*

    :param function: Vista sobre la cual se controla el acceso.
    :return: El método ``es_admin`` que realiza las verificaciones.
    """

    def es_admin(request, *args, **kwargs):
        """
        *``Método del Decorador``: Es llamado por el decorador ``admin_requerido`` para verificar que el usuario actual sea ``Administrador``.*

        :param request: HttpRequest con los datos del usuario actual.
        :return: La ``vista`` en el caso de que el usuario sea el ``Administrador``, caso contrario se redirige a ``/acceso_denegado/``.
        """
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        return HttpResponseRedirect('/denegado/1')
    return es_admin


def user_passes_test(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request, **kwargs):
                return view_func(request, *args, **kwargs)
            # return HttpResponseForbidden()
            return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))
            # path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            # login_scheme, login_netloc = urlparse.urlparse(login_url or settings.LOGIN_URL)[:2]
            # current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            # if ((not login_scheme or login_scheme == current_scheme) and
            #         (not login_netloc or login_netloc == current_netloc)):
            #     path = request.get_full_path()
            # from django.contrib.auth.views import redirect_to_login
            # return redirect_to_login(path, login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def vinculadoProyecto(request, **kwargs):
    usuario = request.user
    id_proyecto = kwargs.pop('id_proyecto', None)

    if not id_proyecto:
        return False

    if usuario.id == -1:
        return False
    try:
        proyecto = Proyecto.objects.get(id=id_proyecto)
    except ObjectDoesNotExist:
        raise Http404

    if not proyecto:
        return False

    usuarioVinculado = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=proyecto, cod_usuario=usuario)

    if usuarioVinculado:
        return True
    else:
        return False


def puede_crear_fase(request, **kwargs):
        """
        *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
        sea Líder del proyecto al cual la vista intenta acceder.*

        :param request: HttpRequest con los datos del usuario actual.
        :param id_proyecto: Id del proyecto al cual se intenta acceder.
        :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
        """
        id_proyecto = kwargs.pop('id_proyecto', None)
        if not id_proyecto:
            return False

        try:
            proyecto = Proyecto.objects.get(id=id_proyecto)
        except ObjectDoesNotExist:
            raise Http404

        lider = proyecto.lider_proyecto
        currentUser = request.user

        if currentUser == lider:
            return True
        return False


def puede_modificar_fase(request, **kwargs):
        """
        *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
        sea Líder del proyecto al cual la vista intenta acceder.*

        :param request: HttpRequest con los datos del usuario actual.
        :param id_proyecto: Id del proyecto al cual se intenta acceder.
        :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
        """
        id_fase = kwargs.pop('id_fase', None)
        if not id_fase:
            return False

        try:
            fase = Fase.objects.get(id=id_fase)
        except ObjectDoesNotExist:
            raise Http404

        lider = Usuario.objects.get(id=fase.proyecto.lider_proyecto_id)
        currentUser = request.user

        if currentUser == lider:
            return True

        return False


def puede_trabajar(request, **kwargs):
    """

    :param request:
    :param kwargs:
    :return:
    """

    id_proyecto = kwargs.pop('id_proyecto', None)
    if not id_proyecto:
        return False

    try:
        proyecto = Proyecto.objects.get(id=id_proyecto)
    except ObjectDoesNotExist:
        raise Http404

    usuario = request.user

    if usuario.id == -1:
        return False

    if usuario == proyecto.lider_proyecto:
        return True

    objetos = get_objects_for_user(usuario, 'consultar_Proyecto', klass=Proyecto)

    if proyecto in objetos:
        return True

    return False


def crear_linea_base(request, **kwargs):
    """

    :param request:
    :param kwargs:
    :return:
    """

    id_fase = kwargs.pop('id_fase', None)
    if not id_fase:
        return False

    try:
        fase = Fase.objects.get(id=id_fase)
    except ObjectDoesNotExist:
        raise Http404

    usuario = request.user
    proyecto = fase.proyecto

    if usuario.id == -1:
        return False

    if usuario == proyecto.lider_proyecto:
        return True

    objetos = get_objects_for_user(usuario, 'crear_Linea_base', klass=Fase)

    if fase in objetos:
        return True

    return False


def verificar_permiso(permisos, nombre_id, conjuncion):
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            id = kwargs.pop(nombre_id, None)

            if 'item' in nombre_id:
                id_item = id
                if not id_item:
                    return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

                try:
                    item = ItemBase.objects.get(id=id_item)
                except ObjectDoesNotExist:
                    raise Http404

                permisosItem = get_perms(request.user, item.tipoitem.fase)
            else:
                id_fase = id
                if not id_fase:
                    return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

                try:
                    fase = Fase.objects.get(id=id_fase)
                except ObjectDoesNotExist:
                    raise Http404

                permisosItem = get_perms(request.user, fase)

            if conjuncion:
                for permiso in permisos:
                    if permiso not in permisosItem:
                        return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))
            else:
                for permiso in permisos:
                    if permiso in permisosItem:
                        kwargs[nombre_id] = id
                        return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def lider_miembro_comite_requerido(nombre_id_item):
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    # TODO: documentar el decorador lider_miembro_comite_requerido
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            id_item = kwargs.pop(nombre_id_item, None)

            if not id_item:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

            try:
                item = ItemBase.objects.get(id=id_item)
            except ObjectDoesNotExist:
                raise Http404

            permisosItem = get_perms(request.user, item)

            if request.user == item.tipoitem.fase.proyecto.lider_proyecto:
                kwargs[nombre_id_item] = id_item
                return view_func(request, *args, **kwargs)
            elif "credencial" in permisosItem:
                kwargs[nombre_id_item] = id_item
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def lider_requerido(nombre_id):
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    # TODO: documentar el decorador lider_requerido
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            id = kwargs.pop(nombre_id, None)

            proyecto = None
            if not id:
                    return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

            if 'fase' in nombre_id:
                id_fase = id

                try:
                    fase = Fase.objects.get(id=id_fase)
                except ObjectDoesNotExist:
                    raise Http404

                proyecto = fase.proyecto
            elif 'proyecto' in nombre_id:
                id_proyecto = id

                try:
                    proyecto = Proyecto.objects.get(id=id_proyecto)
                except ObjectDoesNotExist:
                    raise Http404

            if request.user == proyecto.lider_proyecto:
                kwargs[nombre_id] = id
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def vinculado_proyecto_requerido(nombre_id):
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    # TODO: documentar el decorador vinculado_proyecto_requerido
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            proyecto = None
            id = kwargs.pop(nombre_id, None)
            if 'proyecto' in nombre_id:
                id_proyecto = id
                if not id_proyecto:
                    return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

                try:
                    proyecto = Proyecto.objects.get(id=id_proyecto)
                except ObjectDoesNotExist:
                    raise Http404
                id = id_proyecto
            elif 'fase' in nombre_id:
                id_fase = id
                if not id_fase:
                    return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

                try:
                    proyecto = Fase.objects.get(id=id_fase).proyecto
                except ObjectDoesNotExist:
                    raise Http404
                id = id_fase

            usuarioVinculado = UsuariosVinculadosProyectos.objects.filter(cod_proyecto=proyecto, cod_usuario=request.user)
            if usuarioVinculado:
                kwargs[nombre_id] = id
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def puede_cancelar_solicitud():
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    # TODO: documentar el decorador puede_cancelar_solicitud
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if 'id_solicitud' not in kwargs:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))
            id_solicitud = kwargs['id_solicitud']

            try:
                solicitud = SolicitudCambios.objects.get(id=id_solicitud)
            except ObjectDoesNotExist:
                raise Http404

            try:
                proyecto = solicitud.fase.proyecto
            except ObjectDoesNotExist:
                raise Http404

            if request.user == proyecto.lider_proyecto:
                return view_func(request, *args, **kwargs)
            elif request.user == solicitud.usuario:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def puede_visualizar_solicitud():
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    # TODO: documentar el decorador puede_visualizar_solicitud
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if 'id_solicitud' not in kwargs:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))
            id_solicitud = kwargs['id_solicitud']

            try:
                solicitud = SolicitudCambios.objects.get(id=id_solicitud)
            except ObjectDoesNotExist:
                raise Http404

            try:
                proyecto = solicitud.fase.proyecto
            except ObjectDoesNotExist:
                raise Http404

            nombre_grupo = "ComiteDeCambios-" + str(solicitud.fase.proyecto_id)
            if request.user == proyecto.lider_proyecto:
                return view_func(request, *args, **kwargs)
            elif request.user == solicitud.usuario:
                return view_func(request, *args, **kwargs)
            elif request.user.groups.filter(name=nombre_grupo).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def puede_votar():
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    # TODO: documentar el decorador puede_votar
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if 'id_solicitud' not in kwargs:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))
            id_solicitud = kwargs['id_solicitud']

            try:
                solicitud = SolicitudCambios.objects.get(id=id_solicitud)
            except ObjectDoesNotExist:
                raise Http404

            nombre_grupo = "ComiteDeCambios-" + str(solicitud.fase.proyecto_id)
            if request.user.groups.filter(name=nombre_grupo).exists():
                return view_func(request, *args, **kwargs)
            elif request.user == solicitud.usuario:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def puede_modificar_item(request, **kwargs):
    """
    *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
    sea Líder del proyecto al cual la vista intenta acceder.*

    :param request: HttpRequest con los datos del usuario actual.
    :param id_proyecto: Id del proyecto al cual se intenta acceder.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
    id_item = kwargs.pop('id_item', None)
    if not id_item:
        return False

    try:
        item = ItemBase.objects.get(id=id_item)
    except ObjectDoesNotExist:
        raise Http404

    permisosItem = get_perms(request.user, item.tipoitem.fase)

    if "modificar_Item" in permisosItem:
        return True

    return False