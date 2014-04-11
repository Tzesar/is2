from django.shortcuts import render, render_to_response, HttpResponseRedirect, RequestContext
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


@login_required
def base(request):
    """
    Prueba para el login
    :param request: HttpRequest con los datos de la sesion del usuario logeado.
    :return: Template base.html
    """
    return render(request, 'base.html')

