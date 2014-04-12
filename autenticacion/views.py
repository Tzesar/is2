from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login


def myLogin(request, *args, **kwargs):
    """
    Vista para la plantilla login.html.

    :param request: HttpRequest de autenticacion
    :param args: Lista de argumentos
    :param kwargs: Diccionarios
    :return: Proporciona la pagina login.html
    """
    if request.method == 'POST':
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(604800)
    return login(request, *args, **kwargs)

@login_required
def base(request):
    """
    Vista para la plantilla base.html

    :param request: HttpRequest con los datos de la sesion del usuario actual.
    :return: Template base.html. Los demas templates heredan de este la estructura y los estilos.
    """
    return render(request, 'base.html')