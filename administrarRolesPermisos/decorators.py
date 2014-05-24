#encoding:utf-8

from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs

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
        return HttpResponseRedirect('/acceso_denegado/1')
    return es_admin


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
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

    proyecto = Proyecto.objects.get(id=id_proyecto)

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

        lider = Proyecto.objects.get(pk=id_proyecto).lider_proyecto
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

        fase = Fase.objects.get(id=id_fase)
        lider = Usuario.objects.get(id=fase.proyecto.lider_proyecto_id)
        currentUser = request.user

        if currentUser == lider:
            return True

        return False