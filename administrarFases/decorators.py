#encoding:utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from autenticacion.models import Usuario
from administrarFases.models import Fase


def puede_modificar_fase(request, **kwargs):
        """
        ``Metodo del Decorador`` : *Es llamado por el decorador* ``lider_requerido`` *para comprobar que el usuario logueado
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