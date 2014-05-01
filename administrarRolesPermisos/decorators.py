from administrarRolesPermisos.models import RolFase, PermisoFase
from django.http.response import HttpResponseRedirect
from functools import wraps

# TODO: Completar!!

def permisoFase_requerido(permiso):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):


            roles = RolFase.roles_usuarios.filter(usuario_id=request.user.id)
            for rol in roles:
                permisos = rol.permisos.all()
                for perm in permisos:
                    if perm.nombre == permiso:
                        return func(request, *args, **kwargs)

            return HttpResponseRedirect('/acceso_denegado/')
        return wraps(func)(inner_decorator)
    return decorator
