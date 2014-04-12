from django.contrib.auth.decorators import login_required
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
    return render(request, "usuario/createuser.html", { 'form': form, }, context_instance=RequestContext(request) )

def userlist(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuario/userlist.html", { 'usuarios':usuarios}, )