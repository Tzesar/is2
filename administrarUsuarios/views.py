#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, RequestContext, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import json
from administrarUsuarios.forms import CustomUserChangeForm, CustomUserCreationForm, CambiarUsuarioForm
from autenticacion.models import Usuario
import logging

logger = logging.getLogger(__name__)


@login_required
def createUser(request):
    """
    Vista para la creacion de usuarios en el sistema.

    :param request: HttpRequest
    :return: Proporciona la pagina createuser.html con el formulario correspondiente:
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha creado el usuario: ' +
                        form["username"].value() + ' dentro del sistema')
            return HttpResponseRedirect("/userlist/")
    else:
        form = CustomUserChangeForm()
    return render(request, "usuario/createuser.html", {'form': form, })


@login_required()
def changeUser(request):
    """
    Vista para la modificacion de datos del usuario actual en el sistema.
    Modificación de los datos propios del usuario actual.

    :param request: HttpRequest necesario para modificar los datos de usuario
    :return:  Proporciona la pagina changeuser1.html con el formulario correspondiente
    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CustomUserChangeForm(postdata, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado sus datos personales dentro del sistema')
            return HttpResponseRedirect("/userlist/")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "usuario/changeuser.html", {'form': form, 'user': request.user})

@login_required()
def changeUser2(request):
    """
    Vista para la modificacion de datos del usuario actual en el sistema.
    Modificación de los datos propios del usuario actual.

    :param request: HttpRequest necesario para modificar los datos de usuario
    :return:  Proporciona la pagina changeuser1.html con el formulario correspondiente
    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        myform = CambiarUsuarioForm(postdata, instance=request.user)
        if myform.is_valid():
            myform.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado sus datos personales dentro del sistema')
            return HttpResponseRedirect("/userlist/")
    else:
        myform = CambiarUsuarioForm(instance=request.user)
    return render(request, "usuario/changeuser2.html", {'myform': myform, 'user': request.user})


@login_required()
def changePass(request):
    """
    Vista para la modificación de contrasena  del usuario.
    Modificación de los datos propios del usuario actual.

    :param request: HttpRequest necesario para modificar la contrasena del usuario
    :return:  Proporciona la pagina changePass.html con el formulario correspondiente
    """

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado su contrasena dentro del sistema')
            return HttpResponseRedirect("/userlist/")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "usuario/changepass.html", {'form': form, 'user': request.user}, )


@login_required
def userList(request):
    """
    Vista para listar los usuarios existentes en el sistema.

    :param: HttpRequest necesario para listar los usuarios
    :return:  Proporciona la pagina userlist.html con la lista respectiva de los usuarios existentes en el sistema
    """
    if request.method == 'GET':
        usuarios = Usuario.objects.all().order_by('id')
        return render(request, "usuario/userList.html", {'user': request.user, 'usuarios': usuarios}, )

    xhr = request.GET.has_key('xhr')

    idUsuario = request.POST['usuarioModificado']
    estadoNuevo = request.POST['estadoNuevo']

    if idUsuario and estadoNuevo:
        idUsuario = int(idUsuario)
        if estadoNuevo == 'true':
            estadoNuevo = True
        else:
            estadoNuevo = False
    else:
        responseDict = {'exito': False}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')

    usuario = Usuario.objects.get(id=idUsuario)

    if usuario:
        usuario.is_active = estadoNuevo
    else:
        responseDict = {'exito': False}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')

    usuario.save()
    # TODO: Deshabilitar al usuario de todos los proyectos a los que pertenece

    if xhr:
        responseDict = {'exito': True}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')


def changeAnyUser(request, id_usuario):
    """
    Vista para la modificacion de usuarios en el sistema.
    Función válida solo para el usuario con rol de Administrador.

    :param request: HttpRequest necesario para modificar los datos de usuario
    :return:  Proporciona la pagina changeanyuser.html con el formulario correspondiente
    """
    usuarios = Usuario.objects.get(pk=id_usuario)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CustomUserChangeForm(postdata, instance=usuarios)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el usuario ' +
                        usuarios.username + ' dentro del sistema')
            return HttpResponseRedirect("/userlist/")
    else:
        form = CustomUserChangeForm(instance=usuarios)
    return render(request, "usuario/changeanyuser.html", {'form': form, 'usuario': usuarios, 'user': request.user}, )
