from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def about(request):
    """
    Despliega la informacion acerca del proyecto.

    :param request: HttpRequest del contenido de la pagina about.html
    :return: Despliegue de la pagina about.html
    """
    return render(request, 'about.html')

def contact(request):
    """
    Despliega los responsables del proyecto y los medios para comunicarse con ellos.

    :param request: HttpRequest de los medios de contacto
    :return: Despliegue de la pagina contact.html
    """
    return render(request, 'contact.html')
