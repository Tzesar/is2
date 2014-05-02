#uncoding:utf-8

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, password_reset
from django_tables2 import RequestConfig
from administrarProyectos.models import Proyecto, UsuariosVinculadosProyectos
from administrarProyectos.tables import ProyectoTabla
from is2.settings import DEFAULT_FROM_EMAIL


def myLogin(request, *args, **kwargs):
    """
    *Establece el tiempo de vida de la sesión.*

    :param request: HttpRequest con el contenido de la pagina actual.
    :param args: Argumentos para la funcion contrib.auth.views.login.
    :param kwargs: Keyword Arguments para la funcion contrib.auth.views.login.
    :return: Retorna el resultado de la funcion contrib.auth.views.login.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('main'))
    else:
        if request.method == 'POST':
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(604800)
        return login(request, *args, **kwargs)


@login_required
def base(request):
    """
    *Vista para la plantilla* ``base.html``

    :param request: HttpRequest con los datos de la sesion del usuario actual.
    :param args: Argumentos para la funcion.
    :param kwargs: Keyword Arguments para la funcion.
    :return: Template base.html. Los demas templates heredan de este la estructura y los estilos.
    """
    return render(request, 'base.html')

@login_required
def main(request):
    """
    *Vista para la plantilla* ``main.html``

    :param request: HttpRequest con los datos de la sesion del usuario actual.
    :param args: Argumentos para la funcion.
    :param kwargs: Keyword Arguments para la funcion.
    :return: Template mainAdmin.html para el Administrador y mainAnyUser.html para los demas usuarios.
    """

    if request.user.is_superuser:
        return render(request, 'mainAdmin.html', {'user': request.user})
    else:
        # proyectos = Proyecto.objects.filter(lider_proyecto=request.user, usuarios_asociados__in=[request.user, ])

        #proyectos = ProyectoTabla(Proyecto.objects.filter(usuariosvinculadosproyectos__in=[request.user]))
        u = UsuariosVinculadosProyectos.objects.filter(cod_usuario=request.user.id).values_list('cod_proyecto', flat=True)
        proyectos = ProyectoTabla(Proyecto.objects.filter(pk__in=u))
        RequestConfig(request, paginate={"per_page": 25}).configure(proyectos)

        return render(request, 'mainAnyUser.html', {'user': request.user, 'proyectos': proyectos})


def UserResetPassword(request):
    """
    *Vista para la función de re-establecer la contraseña de un usuario vía correo electrónico*

    :param request: HttpRequest con los datos para la petición formal de reestablecer la contraseña.
    """
    if request.method == 'POST':
        return password_reset(request, from_email=DEFAULT_FROM_EMAIL)
    else:
        return render(request, 'autenticacion/forgot_password.html')

