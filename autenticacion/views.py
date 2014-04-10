from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@csrf_protect
def login(request):
    """ Autorizacion de los usuarios

    :param request: HttpRequest con los datos de la sesion y del usuario anonimo.
    :return HttpResponse: HttpResponse con la plantilla indicada y el contexto correcto.
    """
    form = AuthenticationForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('autenticacion/login.html', c)


@login_required
def base(request):
    """
    Prueba para el login
    :param request: HttpRequest con los datos de la sesion del usuario logeado.
    :return: Template base.html
    """
    return render(request, 'base.html')