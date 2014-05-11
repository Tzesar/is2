from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def accesoDenegado(request, id_error):
    id_error_admin = 1
    if id_error == id_error_admin:
        return render(request, 'acceso_denegadoAdmin.html')

    return render(request, 'acceso_denegadoLider.html')