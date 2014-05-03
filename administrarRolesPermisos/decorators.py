from administrarRolesPermisos.models import RolFase, PermisoFase
from django.http.response import HttpResponseRedirect
from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
from administrarTipoItem.models import TipoItem, Atributo
from functools import wraps


# def permisoFase_requerido(permiso):
#     def decorator(func):
#         def inner_decorator(request, *args, **kwargs):
#
#
#             roles = RolFase.roles_usuarios.filter(usuario_id=request.user.id)
#             for rol in roles:
#                 permisos = rol.permisos.all()
#                 for perm in permisos:
#                     if perm.nombre == permiso:
#                         return func(request, *args, **kwargs)
#
#             return HttpResponseRedirect('/acceso_denegado/')
#         return wraps(func)(inner_decorator)
#     return decorator


def admin_requerido(f):
    def decorator(request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.user.is_superuser:
            return f(request, *args, **kwargs)
        return HttpResponseRedirect('/acceso_denegado/1')
    return decorator


def lider_requerido(f):
    def decorator(request, id_proyecto, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        lider = Proyecto.objects.get(pk=id_proyecto).lider_proyecto
        currentUser = request.user

        if currentUser == lider:
            return f(request, id_proyecto, *args, **kwargs)
        return HttpResponseRedirect('/acceso_denegado/2')
    return decorator


def lider_requerido2(f):
    def decorator(request, id_fase, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        lider = Fase.objects.get(pk=id_fase).proyecto.lider_proyecto
        currentUser = request.user

        if currentUser == lider:
            return f(request, id_fase, *args, **kwargs)
        return HttpResponseRedirect('/acceso_denegado/2')
    return decorator


def lider_requerido3(f):
    def decorator(request, id_tipoitem, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        lider = TipoItem.objects.get(pk=id_tipoitem).fase.proyecto.lider_proyecto
        currentUser = request.user

        if currentUser == lider:
            return f(request, id_tipoitem, *args, **kwargs)
        return HttpResponseRedirect('/acceso_denegado/2')
    return decorator


def lider_requerido4(f):
    def decorator(request, id_atribute, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        lider = Atributo.objects.get(pk=id_atribute).tipoDeItem.fase.proyecto.lider_proyecto
        currentUser = request.user

        if currentUser == lider:
            return f(request, id_atribute, *args, **kwargs)
        return HttpResponseRedirect('/acceso_denegado/2')
    return decorator