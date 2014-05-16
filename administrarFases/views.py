#encoding:utf-8
import logging

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render
from django.utils.html import format_html

from administrarFases.forms import NewPhaseForm, ChangePhaseForm
from administrarRolesPermisos.decorators import *
from django.db import IntegrityError
from administrarRolesPermisos.models import PermisoFase
from administrarItems.models import ItemBase, ItemRelacion


logger = logging.getLogger(__name__)


@login_required()
@lider_requerido
def createPhase(request, id_proyecto):
    """
    *Vista para la creación de fases en el sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para crear fases dentro de los proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema al cual se le vincularán las fases creadas.
    :param args: Argumentos para el modelo ``Fase``.
    :param kwargs: Keyword Arguments para la el modelo ``Fase``.
    :return: Proporciona la pagina ``createphase.html`` con el formulario correspondiente.
            Crea la fase dentro del proyecto especificando y luego regresa al menu principal
    """

    project = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = NewPhaseForm(request.POST, project)
        if form.is_valid():
            fase = form.save(commit=False)
            fase.proyecto = project


            try:
                fase.save()
            except IntegrityError:
                err = format_html('<b><i>Datos Erróneos:</b></i><br>'
                                  '<i>El nombre especificado de fase ya existe. Verifiquelo y vuelva a intentarlo</i>')
                return render(request, "fase/createphase.html", {'form': form, 'user': request.user,
                                                                 'proyecto': project, "error": err },
                                                                  context_instance=RequestContext(request) )

            logger.info('El usuario ' + request.user.username + ' ha creado la fase ' +
                        form["nombre"].value() + ' dentro del proyecto ' + project.nombre)

            generarPermisosFase(project, fase)

            return HttpResponseRedirect('/workproject/'+str(project.id))
    else:
        form = NewPhaseForm()
    return render(request, 'fase/createphase.html', {'form': form, 'proyecto': project, 'user': request.user,
                                                     'error': {} })


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


#TODO: Botones Iniciar Fase - Finalizar Fase
@login_required()
@lider_requerido2
def changePhase(request, id_fase):
    """
    *Vista para la modificacion de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para modificar la fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea modificar.
    :param args: Argumentos para el modelo ``Fase``.
    :param kwargs: Keyword Arguments para la el modelo ``Fase``.
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
    tiposDeItem = TipoItem.objects.filter(fase=phase)
    if request.method == 'POST':
        form = ChangePhaseForm(request.POST, instance=phase)
        if form.is_valid():
            form.save()

            logger.info('El usuario ' + request.user.username + ' ha modificado la fase PH-' +
                        id_fase + ': ' + form["nombre"].value() + ' dentro del proyecto' + project.nombre + 'en el sistema.')

            return HttpResponseRedirect('/workproject/'+str(project.id))
    else:
        form = ChangePhaseForm(instance=phase)
    return render(request, 'fase/changephase.html', {'phaseForm': form, 'phase': phase, 'project': project, 'tiposItem': tiposDeItem, 'user': request.user},
                              context_instance=RequestContext(request))


@login_required()
@lider_requerido2
def confirmar_eliminacion_fase(request, id_fase):
    """
    *Vista para la confirmar la eliminación definitiva de una fase del proyecto.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest - Solicitud de eliminación.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea eliminar.
    :return: Elimina la fase especifica  y luego regresa al menu de fases.
    """
    faseAEliminar = Fase.objects.get(pk=id_fase)
    tiposItem = TipoItem.objects.filter(fase=faseAEliminar)
    return render(request, 'fase/confirmar_eliminacion.html', {'fase': faseAEliminar,
                                                               'tipos': tiposItem},)

@login_required
def deletePhase(request, id_fase):
    """
    *Vista para la eliminación de una fase dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para eliminar fases de un proyectos, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del sistema la cual se desea eliminar.
    :return: Elimina la fase especifica  y luego regresa al menu de fases.
    """

    phase = Fase.objects.get(pk=id_fase)
    tiposItem = TipoItem.objects.filter(fase=phase)

    eliminarPermisos(phase)

    for ti in tiposItem:
        attrs = Atributo.objects.filter(tipoDeItem=ti)
        for attr in attrs:
            attr.delete()
        ti.delete()

    phase_copy = phase
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    phase.delete()

    logger.info('El usuario '+ request.user.username +' ha eliminado la fase '+ phase_copy.nombre +
                ' dentro del proyecto: ' + project.nombre)

    return HttpResponseRedirect('/workproject/'+str(project.id))


def eliminarPermisos(phase):
    """
    *Vista para la eliminacion de permisos correspondientes a la fase*

    :param phase: Recibe la instancia de la fase que se eliminará.
    :return: Los permisos vinculados son eliminados correctamente.
    """
    perm_list = PermisoFase.objects.filter(fase=phase)
    for p in perm_list:
        p.delete()


@login_required
@lider_requerido
def phaseList(request, id_proyecto):
    """
    *Vista para la listar todas las fases dentro de algún proyecto.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar las fases dentro de los proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema.
    :param args: Argumentos para el modelo ``Fase``.
    :param kwargs: Keyword Arguments para la el modelo ``Fase``.
    :return: Proporciona la pagina ``phaselist.html`` con la lista todas las fases pertenecientes al proyecto especificado
    """
    project = Proyecto.objects.get(pk=id_proyecto)
    phase_actual_project = Fase.objects.filter(proyecto=id_proyecto)
    phase_available = phase_actual_project.values_list('id', flat=True)

    phase = Fase.objects.exclude(pk__in=phase_available)
    return render(request, "fase/phaselist.html", {'phase': phase, 'project': project },
                  context_instance=RequestContext(request) )


#TODO: No debería existir caso particular de importar multiples fases
@login_required
@lider_requerido
def importPhase(request, id_fase, id_proyecto_destino):
    """
    *Vista para la importación de un tipo de ítem a otra fase*
    """

    phase = Fase.objects.get(pk=id_fase)
    phase.id = None
    phase.proyecto = Proyecto.objects.get(pk=id_proyecto_destino)
    project = phase.proyecto

    try:
        phase.save()
    except IntegrityError as e:
        return render(request, "keyduplicate_fase.html", {'project': project, "message": e.message },
          context_instance=RequestContext(request) )

    logger.info('El usuario '+ request.user.username +' ha importado la fase '+  phase.nombre +
                ' al proyecto destino: ' + phase.proyecto.nombre)


    return HttpResponseRedirect('/changephase/' + str(phase.id))


#TODO: Revisar funcional pero ineficiente

def importMultiplePhase(request, id_fase, id_proyecto_destino):
    """
    *Vista para la importación de un tipo de ítem a otra fase*
    """

    phase = Fase.objects.get(pk=id_fase)
    phase.id = None
    phase.proyecto = Proyecto.objects.get(pk=id_proyecto_destino)
    project = phase.proyecto

    try:
        phase.save()
    except IntegrityError as e:
        return render(request, "keyduplicate_fase.html", {'project': project, "message": e.message },
          context_instance=RequestContext(request) )

    logger.info('El usuario '+ request.user.username +' ha importado la fase '+  phase.nombre +
                ' al proyecto destino: ' + phase.proyecto.nombre)

    return HttpResponseRedirect('/phaselist/' + str(project.id))


def workphase(request, id_fase):
    """
    *Vista para el trabajo sobre una fase de un proyecto.
    Opción válida para usuarios asociados a un proyecto, con permisos de trabajo sobre items de la fase en cuestion*

    :param request: HttpRequest necesario para visualizar el área de trabajo de los usuarios en la fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase sobre la cual se trabaja.
    :return: Proporciona la pagina ``workPhase.html``, página dedicada al desarrollo de la fase.
             Vista para el desarrollo de fases
    """

    if request.method == 'GET':
        faseTrabajo = Fase.objects.get(pk=id_fase)
        proyectoTrabajo = faseTrabajo.proyecto
        ti = TipoItem.objects.filter(fase=faseTrabajo)
        itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

        relaciones = {}
        for i in itemsFase:
            try:
                itemRelacionado = ItemRelacion.objects.get(itemHijo=i).itemPadre
                relaciones[i] = itemRelacionado
            except:
                relaciones[i] = None

        return render(request, 'fase/workPhase.html', {'proyecto': proyectoTrabajo, 'fase': faseTrabajo,
                                                       'listaItems': itemsFase, 'relaciones': relaciones.items(),})