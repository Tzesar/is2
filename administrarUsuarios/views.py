from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, RequestContext
from administrarUsuarios.forms import CustomUserChangeForm, CustomUserCreationForm


@login_required
def createUser(request):
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
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CustomUserChangeForm(postdata, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/base/")
    else:
        form = CustomUserChangeForm()
    return render(request, "usuario/createuser.html", { 'form': form, }, context_instance=RequestContext(request) )