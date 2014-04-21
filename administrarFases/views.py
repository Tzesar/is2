#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from administrarFases.forms import NewPhaseForm, ChangePhaseForm
from django.shortcuts import render_to_response, render, get_object_or_404
from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
from gestionRolesPermisos.models import PermisoFase
import logging

logger = logging.getLogger(__name__)


@login_required()
def createPhase(request, id_proyecto):
    """
    Vista para la creación de fases en el sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param request:
    :return:
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = NewPhaseForm(request.POST, project)
        if form.is_valid():
            fase = form.save(commit=False)
            fase.proyecto = project
            fase.save()

            logger.info('El usuario ' + request.user.username + ' ha creado la fase: ' +
                        form["nombre"].value() + ' dentro del proyecto: ' + project.nombre)

            generarPermisosFase(project, fase)

            return HttpResponseRedirect('/base/')
    else:
        form = NewPhaseForm()
    return render_to_response('fase/createphase.html', {'form': form}, context_instance=RequestContext(request))


def generarPermisosFase(project, fase):

    #Permiso de creación de items
    codigoPermiso = "CRE_ITEM_FASE:" + fase.nombre
    nombrePermiso = "Crear Item - Fase: " + fase.nombre
    descripcionPermiso = "Permite la creacion de items en la fase " + fase.nombre + " del proyecto " + project.nombre
    p = PermisoFase(code=codigoPermiso.upper(), nombre=nombrePermiso, descripcion=descripcionPermiso)
    p.fase = fase
    p.save()

    #Permiso de modificación de items
    codigoPermiso = "ALT_ITEM_FASE:" + fase.nombre
    nombrePermiso = "Modificar Items - Fase: " + fase.nombre
    descripcionPermiso = "Permite la modificacion de items en la fase " + fase.nombre + " del proyecto " + project.nombre
    p = PermisoFase(code=codigoPermiso.upper(), nombre=nombrePermiso, descripcion=descripcionPermiso)
    p.fase = fase
    p.save()

    #Permiso de baja de items
    codigoPermiso = "DDB_ITEM_FASE:" + fase.nombre
    nombrePermiso = "Dar de baja Items - Fase: " + fase.nombre
    descripcionPermiso = "Permite la baja de items en la fase " + fase.nombre + " del proyecto " + project.nombre
    p = PermisoFase(code=codigoPermiso.upper(), nombre=nombrePermiso, descripcion=descripcionPermiso)
    p.fase = fase
    p.save()

    #Permiso de consulta de items
    codigoPermiso = "VER_ITEM_FASE:" + fase.nombre
    nombrePermiso = "Visualizar Items - Fase: " + fase.nombre
    descripcionPermiso = "Permite la visualizacion de items en la fase " + fase.nombre + " del proyecto " + project.nombre
    p = PermisoFase(code=codigoPermiso.upper(), nombre=nombrePermiso, descripcion=descripcionPermiso)
    p.fase = fase
    p.save()

    #Permiso de restauracion de items
    codigoPermiso = "RVV_ITEM_FASE:" + fase.nombre
    nombrePermiso = "Restaurar Item - Fase: " + fase.nombre
    descripcionPermiso = "Permite la restauracion de items en la fase " + fase.nombre + " del proyecto " + project.nombre + " previamente eliminados"
    p = PermisoFase(code=codigoPermiso.upper(), nombre=nombrePermiso, descripcion=descripcionPermiso)
    p.fase = fase
    p.save()

    #Permiso de reversion de items
    codigoPermiso = "REV_ITEM_FASE:" + fase.nombre
    nombrePermiso = "Reversionar Item - Fase: " + fase.nombre
    descripcionPermiso = "Permite volver a la version anterior de items en la fase " + fase.nombre + " del proyecto " + project.nombre
    p = PermisoFase(code=codigoPermiso.upper(), nombre=nombrePermiso, descripcion=descripcionPermiso)
    p.fase = fase
    p.save()

    #Permiso de creación solicitudes de cambio
    codigoPermiso = "CRE_SOLCAMBIO_FASE:" + fase.nombre
    nombrePermiso = "Crear Solicitud de Cambios - Fase: " + fase.nombre
    descripcionPermiso = "Permite la creacion de solicitudes de cambios para items en linea base de la fase " + fase.nombre + " del proyecto " + project.nombre
    p = PermisoFase(code=codigoPermiso.upper(), nombre=nombrePermiso, descripcion=descripcionPermiso)
    p.fase = fase
    p.save()


@login_required()
def changePhase(request, id_fase):
    """
    Vista para la modificacion de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param request:
    :return:
    """

    phase = Fase.objects.get(pk=id_fase)
    if request.method == 'POST':
        form = ChangePhaseForm(request.POST, instance=phase)
        if form.is_valid():
            logger.info('El usuario ' + request.user.username + ' ha modificado la fase ' +
                        phase.nombre + ' dentro del proyecto: ' + phase.proyecto)
            form.save()
            return HttpResponseRedirect('/base/')
    else:
        form = ChangePhaseForm(instance=phase)
    return render_to_response('fase/changephase.html', {'form': form}, context_instance=RequestContext(request))


def deletePhase(request, id_fase):
    phase = Fase.objects.get(pk=id_fase)
    phase_copy = phase

    eliminarPermisos(phase)
    phase.delete()

    #LOG

    return render(request, "base.html",)


def eliminarPermisos(phase):

    perm_list = PermisoFase.objects.filter(fase=phase)
    for p in perm_list:
        p.delete()



@login_required
def phaseList(request):
    phase = Fase.objects.all()
    return render(request, "fase/phaselist.html", {'phase': phase}, )