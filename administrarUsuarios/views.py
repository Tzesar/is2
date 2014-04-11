from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from administrarUsuarios.forms import UserCreationForm


@login_required
def createUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/base/")
    else:
        form = UserCreationForm()
    return render(request, "usuario/createuser.html", { 'form': form, })