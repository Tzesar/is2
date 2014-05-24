#encoding:utf-8
import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from administrarUsuarios.forms import CustomUserChangeForm, CustomUserCreationForm, CambiarUsuarioForm
from autenticacion.models import Usuario
# from administrarRolesPermisos.decorators import admin_requerido


# logger = logging.getLogger(__name__)


@login_required
def createUser(request):
    """
    *Vista para la creación de usuarios en el sistema.*

    :param request: HttpRequest con los datos de la sesion del usuario actual, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``AbstractBaseUser``.
    :param kwargs: Keyword Arguments para la el modelo ``AbstractBaseUser``.
    :return: Proporciona la pagina ``createuser.html`` con el formulario correspondiente

    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # logger.info('El usuario ' + request.user.username + ' ha creado el usuario: ' +
            #             form["username"].value() + ' dentro del sistema')
            return HttpResponseRedirect("/userlist/")
    else:
        form = CustomUserCreationForm()
    return render(request, "usuario/createuser.html", {'form': form, })


@login_required()
def changeUser(request):
    """
    *Vista para la modificacion de datos del usuario actual en el sistema.
    Modificación de los datos propios del usuario actual.*

    :param request: HttpRequest necesario para modificar los datos de usuario, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``AbstractBaseUser``.
    :param kwargs: Keyword Arguments para la el modelo ``AbstractBaseUser``.
    :return:  Proporciona la pagina ``changeuser.html`` con el formulario correspondiente
    """

    if request.method == 'POST':
        postdata = request.POST.copy()
        userForm = CambiarUsuarioForm(postdata, instance=request.user)
        if userForm.is_valid():
            userForm.save()
            # logger.info('El usuario ' + request.user.username + ' ha modificado sus datos personales dentro del sistema')
            return HttpResponseRedirect("/main/")
    else:
        userForm = CambiarUsuarioForm(instance=request.user)
    return render(request, "usuario/changeuser.html", {'userForm': userForm, 'user': request.user})


@login_required()
def changePass(request):
    """
    *Vista para la modificación de contrasena  del usuario.
    Modificación de los datos propios del usuario actual.*

    :param request: HttpRequest necesario para modificar la contrasena del usuario, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``AbstractBaseUser``.
    :param kwargs: Keyword Arguments para la el modelo ``AbstractBaseUser``.
    :return:  Proporciona la pagina ``changePass.html`` con el formulario correspondiente.
    """

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # logger.info('El usuario ' + request.user.username + ' ha modificado su contrasena dentro del sistema')
            return HttpResponseRedirect("/changeuser/")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "usuario/changepass.html", {'form': form, 'user': request.user}, )


@login_required
def userList(request):
    """
    *Vista para listar los usuarios existentes en el sistema.*

    :param request: HttpRequest necesario para listar los usuarios, es la solicitud de la acción.
    :param args: Argumentos para el modelo ``AbstractBaseUser``.
    :param kwargs: Keyword Arguments para la el modelo ``AbstractBaseUser``.
    :return:  Proporciona la pagina ``userlist.html`` con la lista respectiva de los usuarios existentes en el sistema.
    """

    # Esto sucede cuando se accede normalmente al template
    if request.method == 'GET':
        usuarios = Usuario.objects.all().exclude(is_superuser=True).order_by('id')
        return render(request, "usuario/userList.html", {'user': request.user, 'usuarios': usuarios}, )

    # Esto sucede cuando se modifica el estado de un usuario dentro del sistema
    #   cuando ajax envia una solicitud con el metodo POST

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

    if xhr:
        responseDict = {'exito': True}
        return HttpResponse(json.dumps(responseDict), mimetype='application/javascript')


@login_required()
def changeAnyUser(request, id_usuario):
    """
    *Vista para la modificacion de usuarios en el sistema.
    Función válida solo para el usuario con rol de Administrador.*

    :param request: HttpRequest necesario para modificar los datos de usuario, es la solicitud de la acción.
    :param id_usuario: Identificador del usuario el cual se desea modificar.
    :return:  Proporciona la pagina ``changeanyuser.html`` con el formulario correspondiente.
    """
    usuarios = Usuario.objects.get(pk=id_usuario)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CambiarUsuarioForm(postdata, instance=usuarios)
        if form.is_valid():
            form.save()
            # logger.info('El usuario ' + request.user.username + ' ha modificado el usuario ' +
            #             usuarios.username + ' dentro del sistema')
            return HttpResponseRedirect("/userlist/")
    else:
        form = CambiarUsuarioForm(instance=usuarios)
    return render(request, "usuario/changeanyuser.html", {'form': form, 'usuario': usuarios, 'user': request.user}, )


def userListJson(request, tipoUsuario):
    """
    No es una vista, retorna la lista de usuarios activos dentro del sistema en formato JSON dependiendo del tipo que
    se solicita.

    :param request: HTTPRequest con datos para mantener la seguridad.
    :return: Lista de usuarios con estado activo en formato JSON
    """

    if tipoUsuario == 'LP':
        # query es la pregunta que envia el js
        query = request.GET['query']
        usuarios = Usuario.objects.filter(is_active=True, is_superuser=False, username__contains=query).exclude(id=-1).values_list('username', 'pk').order_by('username')


    # Crea una lista del objeto usuarios
    usuariosList = list(usuarios)
    suggestions = []

    for usuario in usuariosList:
        v, d = usuario
        suggestions.append({'value': v, 'data': d})

    # Crear diccionario con los nombres de usuarios
    respuesta = dict(suggestions=suggestions, query="Unit")

    # TODO: Alguna prueba de seguridad
    respuestaJSON = json.dumps(respuesta)

    return HttpResponse(respuestaJSON, mimetype='application/json')