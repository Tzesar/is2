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
    *Vista para la creación de tipos de ítems en el sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para crear los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del proyecto, a la cual se le vincularán los tipos de ítems.
    :param args: Argumentos para el modelo ``TipoItem``.
    :param kwargs: Keyword Arguments para la el modelo ``TipoItem``.
    :return: Proporciona la pagina ``createtypeitem.html`` con el formulario correspondiente.
            Crea el tipo de ítem dentro de la fase especificada y luego regresa al menu principal
    """

    phase = Fase.objects.get(pk=id_fase)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    if request.method == 'POST':
        form = NewItemTypeForm(request.POST)
        if form.is_valid():
            tipoitem = form.save(commit=False)
            tipoitem.pertenece_fase = phase
            tipoitem.save()
            logger.info('El usuario ' + request.user.username + ' ha creado el tipo de item: ' +
                        tipoitem.nombre + ' dentro de la fase: ' + project.nombre + '->' + phase.nombre)
            return HttpResponseRedirect('/itemtypelist/')
    else:
        form = NewItemTypeForm()
    return render_to_response('tipo_item/createitemtype.html', {'form': form}, context_instance=RequestContext(request))


@login_required()
def changeItemType(request, id_tipoitem):
    """
    *Vista para la modificacion de un tipo de ítem dentro del sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para modificar los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_tipoitem: Identificador del tipo de ítem dentro de la fase, a la cual se le vincularán los tipos de ítems.
    :param args: Argumentos para el modelo ``TipoItem``.
    :param kwargs: Keyword Arguments para la el modelo ``TipoItem``.
    :return: Proporciona la pagina ``changetypeitem.html`` con el formulario correspondiente.
            Modifica el tipo de ítem dentro de la fase especificada y luego regresa al menu principal
    """

    itemtype = TipoItem.objects.get(pk=id_tipoitem)
    phase = Fase.objects.get(pk=itemtype.pertenece_fase.id)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    if request.method == 'POST':
        form = ChangeItemTypeForm(request.POST, instance=itemtype)
        if form.is_valid():
            form.save()
            logger.info('El usuario ' + request.user.username + ' ha modificado el tipo de ítem TI-' +
                        id_tipoitem + ' dentro del proyecto ' + project.nombre + '->' + phase.nombre)
            return HttpResponseRedirect('/main/')
    else:
        form = ChangeItemTypeForm(instance=itemtype)
    return render_to_response('tipo_item/changeitemtype.html', {'form': form, 'itemtype': itemtype}, context_instance=RequestContext(request))


def deleteItemType(request, id_tipoitem):
    """
    *Vista para la eliminación de un tipo de ítem existente en el sistema.*

    :param request: HttpRequest necesario para eliminar los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_tipoitem: Identificador del tipo de ítem dentro de la fase, que se desea eliminar.
    :return: Elimina el tipo de ítem dentro de la fase especificada y luego regresa al menu principal.
    """
    itemtype = TipoItem.objects.get(pk=id_tipoitem)
    phase = Fase.objects.get(pk=itemtype.pertenece_fase)
    project = Proyecto.objects.get(pk=phase.proyecto)
    itemtype_copy = itemtype
    itemtype.delete()
    logger.info(
        'El usuario {0} ha eliminado el tipo de ítem {1} dentro del proyecto {2}->{3}'.format(request.user.username,
                                                                                              itemtype_copy.nombre,
                                                                                              project.nombre,
                                                                                              phase.nombre))

    return render(request, "tipo_item/itemtypelist.html", )


@login_required
def itemtypeList(request, id_fase):
    """
    *Vista para la listar todos los tipos de ítem pertenecientes a alguna fase.*

    *Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase, a la cual pertenecen los tipos de ítems.
    :param args: Argumentos para el modelo ``TipoItem``.
    :param kwargs: Keyword Arguments para la el modelo ``TipoItem``.
    :return: Proporciona la pagina ``itemtypelist.html`` con la lista de tipos de ítem que perteneces a la fase especificada.
    """

    itemtype = TipoItem.objects.filter(pertenece_fase=id_fase)
    return render(request, "tipo_item/itemtypelist.html", {'itemtype': itemtype})