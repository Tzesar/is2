#encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def accesoDenegado(request, id_error):
    """
    *Función que verifica que un usuario contenga los permisos necesarios para acceder o utilizar algún
    componente dentro del sistema.*

    :param request: HttpRequest es la solicitud de la acción.
    :param id_error: Identificado del error, es decir, el nivel de acceso el cual se requiere.
    :return: Retorna una respuesta Http 403, el cual estipula que el usuario no posee los permisos necesarios para realizar dicha acción.
    """
    id_error_admin = 1
    if id_error == id_error_admin:
        return render(request, 'acceso_denegadoAdmin.html')

    return render(request, 'acceso_denegadoLider.html')