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
from administrarRolesPermisos.decorators import lider_requerido2, lider_requerido3, lider_requerido4


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
            logger.info('El usuario {0} ha creado el tipo de ítem {1} dentro de la fase {2} en el proyecto: {3}'
                        .format(request.user.username, form["nombre"].value(), phase.nombre, project.nombre))

            return HttpResponseRedirect('/changephase/' + str(phase.id))
    else:
        form = NewItemTypeForm()
    return render(request, 'tipo_item/createitemtype.html', {'user': request.user, 'form': form, 'project': project, 'fase': phase})


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
            logger.info('El usuario {0} ha modificado el tipo de item {1} la fase {2} dentro del proyecto: {3}'
                        .format(request.user.username, itemtype.nombre, phase.nombre, project.nombre))

            return HttpResponseRedirect('/changephase/' + str(phase.id))

    else:
        form = ChangeItemTypeForm(instance=itemtype)
    return render(request, 'tipo_item/changeitemtype.html', {'user': request.user, 'form': form, 'itemtype': itemtype, 'project': project, 'atributos': atributos, 'fase': phase})


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
    logger.info('El usuario {0} ha eliminado el tipo de ítem {1} de la fase {2} dentro del proyecto: {3}'
                .format(request.user.username, itemtype.nombre, fase.nombre, fase.proyecto.nombre))

    return HttpResponseRedirect('/changephase/' + str(fase.id))


@login_required
@lider_requerido2
def itemTypeList(request, id_fase):
    """
    *Vista para la listar todos los tipos de ítem pertenecientes a alguna fase.*

    *Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase, a la cual pertenecen los tipos de ítems.
    :param args: Argumentos para el modelo ``TipoItem``.
    :param kwargs: Keyword Arguments para la el modelo ``TipoItem``.
    :return: Proporciona la pagina ``itemtypelist.html`` con la lista de tipos de ítem que perteneces a la fase especificada.
    """

    itemtypes = TipoItem.objects.all()
    fase = Fase.objects.get(pk=id_fase)
    project = fase.proyecto
    return render(request, "tipo_item/itemtypelist.html", {'user': request.user, 'itemtypes': itemtypes, 'id_fase': id_fase, 'project': project})


@login_required
@lider_requerido2
def importItemType(request, id_fase, id_itemtype):
    """
    *Vista para la listar todos los tipos de ítem pertenecientes a alguna fase.*

    *Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para visualizar los tipos de ítems dentro de alguna fase, es la solicitud de la acción.
    :param id_fase: Identificador de la fase, a la cual pertenecen los tipos de ítems.
    :param args: Argumentos para el modelo ``TipoItem``.
    :param kwargs: Keyword Arguments para la el modelo ``TipoItem``.
    :return: Proporciona la pagina ``itemtypelist.html`` con la lista de tipos de ítem que perteneces a la fase especificada.
    """


    tipoItemExistente = TipoItem.objects.get(id=id_itemtype)
    tipoItemNuevo = TipoItem.objects.get(id=id_itemtype)
    fase = Fase.objects.get(id=id_fase)

    tipoItemNuevo.id = None
    tipoItemNuevo.fase = fase
    tipoItemNuevo.save()

    for atributo in tipoItemExistente.atributo_set.all():
        atributo.id = None
        atributo.tipoDeItem = tipoItemNuevo
        atributo.save()

    logger.info('El usuario {0} ha importado el tipo de ítem {1} de la fase {2} del proyecto {3} a la fase {4} del proyecto {5}'
                .format(request.user.username, tipoItemExistente.nombre, tipoItemExistente.fase.nombre,
                 tipoItemExistente.fase.proyecto.nombre, fase.nombre, fase.proyecto.nombre))



    return HttpResponseRedirect('/changeitemtype/' + str(tipoItemNuevo.id))


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
            logger.info('El usuario {0} ha creado el atributo {1} perteneciente al tipo de item: {2}'
                        .format(request.user.username, atributo.nombre, itemtype.nombre))


        return HttpResponseRedirect('/changeitemtype/'+str(id_tipoitem))
    else:
        form = CreateAtributeForm()
    return render(request, 'tipo_item/createatribute.html', {'user': request.user, 'form': form, 'project': project,
                                                             'itemtype': itemtype, 'fase': phase})


@login_required()
@lider_requerido4
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
            logger.info('El usuario {0} ha modificado el atributo ATI- {1}:{2} perteneciente al tipo de ítem: {3}'
                        .format(request.user.username, atribute.id, atribute.nombre, itemtype.nombre))
            return HttpResponseRedirect('/changeitemtype/' + str(itemtype.id))
    else:
        form = ChangeAtributeForm(instance=atribute)
    return render(request, 'tipo_item/changeatribute.html', {'user': request.user, 'form': form, 'itemtype': itemtype,
                                                             'project': project, 'atributo': atribute, 'fase': phase})


@login_required()
@lider_requerido4
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
    logger = logging.getLogger(__name__)
    logger.info('El usuario {0} ha eliminado el atributo {1} perteneciente al tipo de ítem: {2}'
                        .format(request.user.username, attr.nombre, attr.tipoDeItem.nombre))
    return HttpResponseRedirect('/changeitemtype/' + str(id_tipoItem))