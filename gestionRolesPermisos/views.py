#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, RequestContext, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from gestionRolesPermisos.forms import NewRoleForm

import logging

logger = logging.getLogger(__name__)


@login_required
def createRole(request):
    """
    Vista para la creacion de roles en un proyecto.

    :param request: HttpRequest
    :return: Proporciona la pagina createrole.html con el formulario correspondiente:
    """
    if request.method == 'POST':
        form = NewRoleForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha creado el rol: ' +
                        form["username"].value() + ' en el proyecto X')
            return HttpResponseRedirect("/base/")
    else:
        form = NewRoleForm()
    return render(request, "rol/createrole.html", { 'form': form, })
