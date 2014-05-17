#encoding:utf-8

from django.http.response import HttpResponseRedirect

from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
from administrarTipoItem.models import TipoItem, Atributo


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


def lider_requerido(function):
    """
    *``Decorador``: Verifica que el usuario actual sea ``Líder del proyecto`` al cual la vista intenta acceder.*

    :param function: La vista sobre la cual se está realizando la comprobación.
    :return: El método ``es_lider`` que realiza las verificaciones.
    """

    def es_lider(request, id_proyecto, *args, **kwargs):
        """
        *``Metodo del Decorador``: Es llamado por el decorador ``lider_requerido`` para comprobar que el usuario logueado
        sea Líder del proyecto al cual la vista intenta acceder.*

        :param request: HttpRequest con los datos del usuario actual.
        :param id_proyecto: Id del proyecto al cual se intenta acceder.
        :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
        """
        lider = Proyecto.objects.get(pk=id_proyecto).lider_proyecto
        currentUser = request.user

        if currentUser == lider:
            return function(request, id_proyecto, *args, **kwargs)
        return HttpResponseRedirect('/acceso_denegado/2')
    return es_lider