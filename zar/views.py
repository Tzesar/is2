from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def about(request):
    """
    Despliega la informacion acerca del proyecto.

    :param request:
    :return:
    """
    return render(request, 'about.html')

def contact(request):
    """
    Despliega los responsables del proyecto y los medios para comunicarse con ellos.

    :param request:
    :return:
    """
    return render(request, 'contact.html')
