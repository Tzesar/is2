#encoding:utf-8
import logging

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render

from administrarTipoItem.forms import NewItemTypeForm, ChangeItemTypeForm, CreateAtributeForm, ChangeAtributeForm

from administrarTipoItem.models import TipoItem, Atributo
from administrarFases.models import Fase
from administrarProyectos.models import Proyecto
from administrarRolesPermisos.decorators import lider_requerido2, lider_requerido3


logger = logging.getLogger(__name__)


@login_required()
@lider_requerido2
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
            tipoitem.fase = phase
            tipoitem.save()

            return HttpResponseRedirect('/changephase/' + str(phase.id))
    else:
        form = NewItemTypeForm()
    return render(request, 'tipo_item/createitemtype.html', {'form': form, 'project': project}, context_instance=RequestContext(request))


@login_required()
@lider_requerido3
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
    phase = Fase.objects.get(pk=itemtype.fase.id)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    atributos = Atributo.objects.filter(tipoDeItem=id_tipoitem)
    if request.method == 'POST':
        form = ChangeItemTypeForm(request.POST, instance=itemtype)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/changeitemtype/' + str(id_tipoitem))
    else:
        form = ChangeItemTypeForm(instance=itemtype)
    return render(request, 'tipo_item/changeitemtype.html', {'form': form, 'itemtype': itemtype, 'project': project, 'atributos': atributos, 'fase': phase}, context_instance=RequestContext(request))


@login_required()
@lider_requerido3
def deleteItemType(request, id_tipoitem):
    """
    *Vista para la eliminación de un tipo de ítem existente en el sistema.*

    :param request: HttpRequest necesario para eliminar los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_tipoitem: Identificador del tipo de ítem dentro de la fase, que se desea eliminar.
    :return: Elimina el tipo de ítem dentro de la fase especificada y luego regresa al menu principal.
    """
    itemtype = TipoItem.objects.get(pk=id_tipoitem)
    fase = itemtype.fase
    atributos = Atributo.objects.filter(tipoDeItem=itemtype)

    for attr in atributos:
        attr.delete()

    itemtype.delete()

    return HttpResponseRedirect('/changephase/' + str(fase.id))


@login_required
@lider_requerido2
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

    itemtype = TipoItem.objects.filter(fase=id_fase)
    return render(request, "tipo_item/itemtypelist.html", {'itemtype': itemtype})


@login_required()
@lider_requerido3
def createAtribute(request, id_tipoitem):
    """
    *Vista para la creación de ``Atributos`` en los ``Tipos de ítems`` en el sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para crear los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del proyecto, a la cual se le vincularán los tipos de ítems.
    :param args: Argumentos para el modelo ``Atributo``.
    :param kwargs: Keyword Arguments para la el modelo ``Atributo``.
    :return: Proporciona la pagina ``createtypeitem.html`` con el formulario correspondiente.
            Crea el tipo de ítem dentro de la fase especificada y luego regresa al menu principal
    """

    itemtype = TipoItem.objects.get(pk=id_tipoitem)
    phase = itemtype.fase
    project = phase.proyecto
    if request.method == 'POST':
        form = CreateAtributeForm(request.POST)
        if form.is_valid():
            atributo = form.save(commit=False)
            atributo.tipoDeItem = itemtype
            atributo.save()

            return HttpResponseRedirect('/changeitemtype/'+str(id_tipoitem))
    else:
        form = CreateAtributeForm()
    return render(request, 'tipo_item/createatribute.html', {'form': form, 'project': project, 'itemtype': itemtype}, context_instance=RequestContext(request))


@login_required()
def changeAtribute(request, id_atribute):
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

    atribute = Atributo.objects.get(pk=id_atribute)
    itemtype = atribute.tipoDeItem
    phase = itemtype.fase
    project = phase.proyecto
    if request.method == 'POST':
        form = ChangeAtributeForm(request.POST, instance=atribute)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/changeitemtype/' + str(itemtype.id))
    else:
        form = ChangeAtributeForm(instance=atribute)
    return render(request, 'tipo_item/changeatribute.html', {'form': form, 'itemtype': itemtype, 'project': project, 'atributo': atribute}, context_instance=RequestContext(request))


@login_required()
def deleteAtribute(request, id_atribute):
    """
    *Vista para la eliminación de un tipo de ítem existente en el sistema.*

    :param request: HttpRequest necesario para eliminar los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_tipoitem: Identificador del tipo de ítem dentro de la fase, que se desea eliminar.
    :return: Elimina el tipo de ítem dentro de la fase especificada y luego regresa al menu principal.
    """
    attr = Atributo.objects.get(pk=id_atribute)
    id_tipoItem = attr.tipoDeItem.id
    attr.delete()

    return HttpResponseRedirect('/changeitemtype/' + str(id_tipoItem))