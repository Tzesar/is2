#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from administrarTipoItem.forms import NewItemTypeForm, ChangeItemTypeForm
from django.shortcuts import render_to_response, render, get_object_or_404
from administrarTipoItem.models import TipoItem
from administrarFases.models import Fase
from administrarProyectos.models import Proyecto
import logging

logger = logging.getLogger(__name__)


@login_required()
def createItemType(request, id_fase):
    """
    Vista para la creación de tipos de ítems en el sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request y el identificador de la fase de tal manera a identificar la fase a la cual pertencera el nuevo tipo de item creado.
    :return: Crea el tipo de ítem dentro de la fase especificada y luego regresa al menu principal
    """
    phase = Fase.objects.get(pk=id_fase)
    project = Proyecto.objects.get(pk=phase.proyecto)
    if request.method == 'POST':
        form = NewItemTypeForm(request.POST)
        if form.is_valid():
            tipoitem = form.save(commit=False)
            tipoitem.perteneceFase = id_fase
            tipoitem.save()
            logger.info('El usuario ' + request.user.username + ' ha creado el tipo de ítem: ' +
                        form["nombre"].value() + ' dentro de la fase: ' + project.nombre + '->' + phase.nombre)
            return HttpResponseRedirect('/base/')
    else:
        form = NewItemTypeForm()
    return render_to_response('tipo_item/createitemtype.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def changeItemTypeForm(request, id_tipoitem):
    """
    Vista para la modificacion de un tipo de ítem dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request y el identificador del tipo de item, de manera a identificar el tipo de ítem el cual deseamos modificar.
    :return: Modifica el tipo de ítem y luego regresa al menu principal
    """
    itemtype = TipoItem.objects.get(pk=id_tipoitem)
    phase = Fase.objects.get(pk=itemtype.perteneceFase)
    project = Proyecto.objects.get(pk=phase.proyecto)
    if request.method == 'POST':
        form = changeItemTypeForm(request.POST, instance=itemtype)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el tipo de ítem TI-' +
                        id_tipoitem + ' dentro del proyecto ' + project.nombre + '->' + phase.nombre)
            return HttpResponseRedirect('/base/')
    else:
        form = changeItemTypeForm(instance=itemtype)
    return render_to_response('tipo_item/changeitemtype.html', {'form': form}, context_instance=RequestContext(request))


def deleteItemType(request, id_tipoitem):
    """
    Vista para la eliminación de un tipo de ítem existente en el sistema.

    :param: Recibe la petición request y el identificador del tipo de ítem el cual deseamos eliminar.
    :return: Elimina el tipo de ítem especificado  y luego regresa al menu principal
    """
    itemtype = TipoItem.objects.get(pk=id_tipoitem)
    phase = Fase.objects.get(pk=itemtype.perteneceFase)
    project = Proyecto.objects.get(pk=phase.proyecto)
    logger.info(
        'El usuario {0} ha eliminado el tipo de ítem {1} dentro del proyecto {2}->{3}'.format(request.user.username,
                                                                                              itemtype.nombre,
                                                                                              project.nombre,
                                                                                              phase.nombre))
    itemtype.delete()
    return render(request, "base.html", )


@login_required
def itemtypeList(request, id_fase):
    """
    Vista para la listar todos los tipos de ítem pertenecientes a alguna fase .
    Opción válida para usuarios con los roles correspondientes.

    :param: Recibe la petición request y el identificador de la fase, para listar todos los tipos de ítems pertenecientes a dicha fase
    :return: Lista todos los tipos de ítems pertenecientes a la fase especificada
    """
    itemtype = TipoItem.objects.filter(perteneceFase=id_fase)
    return render(request, "tipo_item/itemtypelist.html", {'itemtype': itemtype}, )