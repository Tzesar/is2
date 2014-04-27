#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.utils.safestring import mark_safe
from administrarFases.forms import NewPhaseForm, ChangePhaseForm
from django.core.urlresolvers import reverse
from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
from administrarRolesPermisos.models import PermisoFase
import logging

logger = logging.getLogger(__name__)


@login_required()
def createPhase(request, id_proyecto):
    """
    *Vista para la creación de fases en el sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para crear fases dentro de los proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema al cual se le vincularán las fases creadas.
    :return: Proporciona la pagina ``createphase.html`` con el formulario correspondiente.
            Crea la fase dentro del proyecto especificando y luego regresa al menu principal
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = NewPhaseForm(request.POST, project)
        if form.is_valid():
            fase = form.save(commit=False)
            fase.proyecto = project
            fase.save()
            logger.info('El usuario ' + request.user.username + ' ha creado la fase ' +
                        form["nombre"].value() + ' dentro del proyecto ' + project.nombre)

            generarPermisosFase(project, fase)

            return HttpResponseRedirect('/main/')
    else:
        form = NewPhaseForm()
    return render_to_response('fase/createphase.html', {'form': form}, context_instance=RequestContext(request))


def generarPermisosFase(project, fase):
    """
    *Vista para generación de permisos correspondientes a la fase*

    :param project: Recibe la instancia del proyecto al cual pertenece la fase.
    :param fase: Recibe la instancia de la fase en la cual se crearán los permisos.
    :return: Los permisos generados se vinculan correctamente a la fase creada.
    """

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
    *Vista para la modificacion de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para modificar la fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea modificar.
    :return: Proporciona la pagina ``changephase.html`` con el formulario correspondiente.
             Modifica la fase especifica  y luego regresa al menu principal
    """

    try:
        Fase.objects.get(pk=id_fase)
    except Fase.DoesNotExist:
        print 'La fase especificada no existe'
        return

    phase = Fase.objects.get(pk=id_fase)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    if request.method == 'POST':
        form = ChangePhaseForm(request.POST, instance=phase)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado la fase con codigo ' +phase.codigo + '-'
                        + str(id_fase) + ' dentro del proyecto: ' + project.nombre)
            return HttpResponseRedirect('/base/')
    else:
        form = ChangePhaseForm(instance=phase)
    return render_to_response('fase/changephase.html', {'form': form, 'phase': phase, 'project': project},
                              context_instance=RequestContext(request))


def deletePhase(request, id_fase):
    """
    *Vista para la eliminación de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para eliminar fases de un proyectos, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea eliminar.
    :return: Elimina la fase especifica  y luego regresa al menu de fases.
    """
    phase = Fase.objects.get(pk=id_fase)
    eliminarPermisos(phase)
    phase_copy = phase
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    phase.delete()
    logger.info('El usuario {0} ha eliminado la fase {1}{2} dentro del proyecto: {3}'.format(request.user.username,
                                                                                             phase_copy.proyecto,
                                                                                             phase_copy.nombre,
                                                                                             project.nombre))

    return HttpResponseRedirect('/main/')


def eliminarPermisos(phase):
    """
    *Vista para la eliminacion de permisos correspondientes a la fase*

    :param fase: Recibe la instancia de la fase que se eliminará.
    :return: Los permisos vinculados son eliminados correctamente.
    """
    perm_list = PermisoFase.objects.filter(fase=phase)
    for p in perm_list:
        p.delete()



@login_required
def phaseList(request, id_proyecto):
    """
    *Vista para la listar todas las fases dentro de algún proyecto.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar las fases dentro de los proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema.
    :return: Proporciona la pagina ``phaselist.html`` con la lista todas las fases pertenecientes al proyecto especificado
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    phase = Fase.objects.filter(proyecto=id_proyecto)
    return render(request, "fase/phaselist.html", {'phase': phase, 'project':project },
                  context_instance=RequestContext(request) )