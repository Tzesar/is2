from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, RequestContext
from administrarUsuarios.forms import CustomUserChangeForm, CustomUserCreationForm
from autenticacion.models import Usuario


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
            return HttpResponseRedirect("/base/")
    else:
        form = CustomUserChangeForm()
    return render(request, "usuario/createuser.html", { 'form': form, })


@login_required()
def changeUser(request):
    """
    Vista para la modificacion de usuarios en el sistema.

    :param request: HttpRequest necesario para modificar los datos de usuario
    :return:  Proporciona la pagina changeuser.html con el formulario correspondiente
    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CustomUserChangeForm(postdata, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/base/")
    else:
        form = CustomUserChangeForm()
    return render(request, "usuario/changeuser.html", { 'form': form, }, context_instance=RequestContext(request) )


@login_required()
def changePass(request):
    """
    Vista para la modificacion de contrasena  del usuario.

    :param request: HttpRequest necesario para modificar la contrasena del usuario
    :return:  Proporciona la pagina changePass.html con el formulario correspondiente
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/base/")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "usuario/changepass.html", { 'form': form, }, context_instance=RequestContext(request) )


@login_required
def userlist(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuario/userlist.html", { 'usuarios':usuarios}, )