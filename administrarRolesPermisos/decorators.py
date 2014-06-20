#encoding:utf-8

from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
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
    ``Decorador`` *: Verifica que el usuario actual sea* ``Administrador`` *antes de concederle acceso a la vista.*

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
        return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))
    return es_admin


def verificar_permiso(permisos, nombre_id, conjuncion):
    """
    *Verifica que el parámetro* ``nombre_id`` *de encuentre en el* ``request`` *de la vista decorada. Según este parámetro,*
    *si es* ``item`` *o* ``fase`` *, sigue procedimientos distintos para obtener el objeto* ``ItemBase`` *y los permisos que*
    *posee el usuario sobre dicho item. Luego verifica que la lista* ``permisos`` *se encuentre dentro de los permisos del*
    *item. El argumento* ``conjuncion`` *especifica que el usuario debe poseer todos los* ``permisos`` *sobre el item para*
    *acceder a la vista decorada. En caso contrario, se muestra la página* ``accesoDenegado`` *.*

    :param permisos: Lista de strings, que contiene los códigos de los permisos que el usuario debe poseer sobre el item.
    :param nombre_id: Nombre del parámetro que identifica al item.
    :param conjuncion: ``False`` si el usuario debe poseer al menos uno de los permisos especificados en el argumento ``permisos`` sobre el item. ``True`` si se requieren todos y cada uno de los permisos.
    :return: La ``vista`` en el caso de que el usuario sea el posea los permisos necesarios, caso contrario se redirige a ``/acceso_denegado/``.
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
    *Verifica que el parámetro* ``nombre_id_item`` *corresponda a un* ``ItemBase`` *existente. Luego obtiene los permisos*
    *que posee el usuario sobre el item. Por último, comprueba si el usuario es el* ``Líder del Proyecto`` *, luego*
    *verifica si el usuario pertenece al* ``Comité de Cambios`` *. En caso contrario, se muestra la página* ``accesoDenegado`` *.*

    :param nombre_id_item: Nombre del parámetro que identifica al item, se recupera del request de la vista que se protege.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto o pertenezca al ``Comité de Cambios``, caso contrario se redirige a ``/acceso_denegado/``.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            id_item = kwargs.pop(nombre_id_item, None)

            if not id_item:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

            try:
                item = ItemBase.objects.get(id=id_item)
            except ObjectDoesNotExist:
                raise Http404

            nombre = 'ComiteDeCambios-' + str(item.tipoitem.fase.proyecto_id)
            grupo = Group.objects.get(name=nombre)
            miembros = grupo.user_set.all()

            if request.user == item.tipoitem.fase.proyecto.lider_proyecto:
                kwargs[nombre_id_item] = id_item
                return view_func(request, *args, **kwargs)
            elif request.user in miembros:
                kwargs[nombre_id_item] = id_item
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator


def lider_requerido(nombre_id):
    """
    *Verifica que el parámetro* ``nombre_id`` *se encuentra en el* ``request`` *de la vista que se decora. Según este*
    *parámetro, si es* ``fase`` *o* ``proyecto`` *, sigue procedimientos distintos para obtener el objeto* ``Proyecto`` *.*
    *Por último, comprueba si el usuario es el* ``Líder del Proyecto`` *. En caso contrario, se muestra la página*
    ``accesoDenegado`` *.*

    :param nombre_id: Nombre del parámetro que identifica al item, se recupera del request de la vista que se protege.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
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
    *Verifica que el parámetro* ``nombre_id`` *se encuentra en el* ``request`` *de la vista que se decora, según este*
    *parámetro, si es* ``fase`` *o* ``proyecto`` *, sigue procedimientos distintos para obtener el objeto* ``Proyecto`` *.*
    *Luego, obtiene todos los usuarios vinculados al proyecto en cuestión y por último verifica si el usuario actual se*
    *encuentra en esa lista. En caso contrario, se muestra la página de* ``accesoDenegado`` *.*

    :param nombre_id: Nombre del parámetro que identifica al item, se recupera del request de la vista que se protege.
    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, caso contrario se redirige a ``/acceso_denegado/``.
    """
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
    *Obtiene el identificador de la solicitud del* ``request`` *de la vista decorada. Recupera el objeto*
    ``SolicitudCambios`` *, si no existe muestra la página 404, y luego obtiene el proyecto sobre el cual se trabaja.*
    *Por último, verifica si el usuario es* ``Líder de Proyecto`` *o es el creador de la* ``Solicitud`` *para mostrar la*
    *vista decorada. En caso contrario, se muestra la página de* ``accesoDenegado`` *.*

    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto o haya creado la ``solicitud``, caso contrario se redirige a ``/acceso_denegado/``.
    """
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
    *Obtiene el identificador de la solicitud del* ``request`` *de la vista decorada. Recupera el objeto*
    ``SolicitudCambios`` *, si no existe muestra la página 404, luego obtiene el proyecto sobre el cual se trabaja.*
    *Por último, verifica si el usuario es* ``Líder de Proyecto`` *, es el creador de la* ``Solicitud`` *o pertenece al*
    ``comité de cambios`` *para mostrar la vista decorada. En caso contrario, se muestra la página de*
    ``accesoDenegado`` *.*

    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto, haya creado la ``solicitud`` o sea miembro del comite de cambios, caso contrario se redirige a ``/acceso_denegado/``.
    """
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
    *Obtiene el identificador de la solicitud del* ``request`` *de la vista decorada. Recupera el objeto*
    ``SolicitudCambios`` *, si no existe muestra la página 404, luego obtiene el proyecto sobre el cual se trabaja.*
    *Por último, verifica si pertenece al* ``comité de cambios`` *para mostrar la vista decorada. En caso contrario,*
    *se muestra la página de* ``accesoDenegado`` *.*

    :return: La ``vista`` en el caso de que el usuario sea miembro del comite de cambios, caso contrario se redirige a ``/acceso_denegado/``.
    """
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


def puede_crear_linea_base():
    """
    *Verifica que el parámetro* ``id_fase`` *se encuentra en el* ``request`` *de la vista que se decora. Según este*
    *parámetro obtiene el objeto* ``Fase`` *y de este recupera el objeto* ``Proyecto`` *.*
    *Por último, comprueba si el usuario es el* ``Líder del Proyecto`` *o si el usuario posee el permiso*
    ``crear_Linea_Base`` *. En caso contrario, se muestra la página* ``accesoDenegado`` *.*

    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto o posee permisos para crear lineas base en la fase, caso contrario se redirige a ``/acceso_denegado/``.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if 'id_fase' not in kwargs:
                return HttpResponseBadRequest()
            id_fase = kwargs['id_fase']

            try:
                fase = Fase.objects.get(id=id_fase)
            except ObjectDoesNotExist:
                raise Http404

            try:
                proyecto = fase.proyecto
            except ObjectDoesNotExist:
                raise Http404

            usuario = request.user

            if usuario.id == -1:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

            if usuario == proyecto.lider_proyecto:
                return view_func(request, *args, **kwargs)

            objetos = get_objects_for_user(usuario, 'crear_Linea_Base', klass=Fase)

            if fase in objetos:
                return view_func(request, *args, **kwargs)

            return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))
        return _wrapped_view
    return decorator


def puede_revocar_credencial():
    """
    *Obtiene el identificador de la solicitud del* ``request`` *de la vista decorada. Recupera el objeto*
    ``SolicitudCambios`` *, si no existe muestra la página 404, luego obtiene el proyecto sobre el cual se trabaja.*
    *Por último, verifica si el usuario es* ``Líder de Proyecto`` *o pertenece al* ``comité de cambios`` *para mostrar*
    *la vista decorada. En caso contrario, se muestra la página de* ``accesoDenegado`` *.*

    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto o sea miembro del comite de cambios, caso contrario se redirige a ``/acceso_denegado/``.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if 'id_solicitud' not in kwargs:
                return HttpResponseBadRequest()
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


def puede_finalizar_revision_item():
    """
    *Obtiene el identificador del item del* ``request`` *de la vista decorada. Recupera el objeto* ``ItemBase`` *,*
    *si no existe muestra la página 404, luego obtiene el proyecto sobre el cual se trabaja. Por último, verifica si el*
    *usuario es* ``Líder de Proyecto`` *o es el creador de la* ``Solicitud`` *para mostrar la vista decorada. En caso*
    *contrario, se muestra la página de* ``accesoDenegado`` *.*

    :return: La ``vista`` en el caso de que el usuario sea el ``Líder`` del proyecto o haya creado la ``solicitud`` sea miembro del comite de cambios, caso contrario se redirige a ``/acceso_denegado/``.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if 'id_item' not in kwargs:
                return HttpResponseBadRequest()
            id_item = kwargs['id_item']

            try:
                item = ItemBase.objects.get(id=id_item)
            except ObjectDoesNotExist:
                raise Http404

            try:
                proyecto = item.tipoitem.fase.proyecto
            except ObjectDoesNotExist:
                raise Http404

            if request.user == proyecto.lider_proyecto:
                return view_func(request, *args, **kwargs)

            try:
                solicitud = SolicitudCambios.objects.get(usuario=request.user, estado='ACP', items=item)
            except ObjectDoesNotExist:
                raise Http404

            if request.user == solicitud.usuario:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('administrarRolesPermisos.views.accesoDenegado', args=(1,)))

        return _wrapped_view
    return decorator