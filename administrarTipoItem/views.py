#encoding:utf-8
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render

from administrarProyectos.models import Proyecto
from administrarFases.models import Fase
from administrarTipoItem.models import TipoItem, Atributo
from administrarTipoItem.forms import NewItemTypeForm, ChangeItemTypeForm, CreateAtributeForm, ChangeAtributeForm

from django.db import IntegrityError


# logger = logging.getLogger(__name__)


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
            tipoitem.fase = phase

            try:
                tipoitem.save()
            except IntegrityError as e:
                return render(request, "keyduplicate_tipoitem.html", {'phase': phase, "message": e.message},
                  context_instance=RequestContext(request))

            return HttpResponseRedirect('/changephase/' + str(phase.id))
    else:
        form = NewItemTypeForm()
    return render(request, 'tipo_item/createitemtype.html', {'user': request.user, 'form': form, 'project': project, 'fase': phase})


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
    phase = Fase.objects.get(pk=itemtype.fase.id)
    project = Proyecto.objects.get(pk=phase.proyecto.id)
    atributos = Atributo.objects.filter(tipoDeItem=id_tipoitem)
    if request.method == 'POST':
        form = ChangeItemTypeForm(request.POST, instance=itemtype)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/changephase/' + str(phase.id))

    else:
        form = ChangeItemTypeForm(instance=itemtype)
    return render(request, 'tipo_item/changeitemtype.html', {'user': request.user, 'form': form, 'itemtype': itemtype, 'project': project, 'atributos': atributos, 'fase': phase})


@login_required()
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

    itemtypes_phase = TipoItem.objects.filter(fase=id_fase)
    itemtypes_available = itemtypes_phase.values_list('id', flat=True)
    itemtypes = TipoItem.objects.exclude(pk__in=itemtypes_available)

    fase = Fase.objects.get(pk=id_fase)
    project = fase.proyecto
    return render(request, "tipo_item/itemtypelist.html", {'user': request.user, 'itemtypes': itemtypes, 'id_fase': id_fase, 'project': project})


@login_required
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

    try:
        tipoItemNuevo.save()
    except IntegrityError as e:
        return render(request, "keyduplicate_tipoitem.html", { 'phase': fase , 'itemtype': tipoItemNuevo, "message": e.message},
                  context_instance=RequestContext(request))

    for atributo in tipoItemExistente.atributo_set.all():
        atributo.id = None
        atributo.tipoDeItem = tipoItemNuevo
        atributo.save()

    # logger.info('El usuario '+request.user.username + ' ha importado el tipo de ítem ' +tipoItemExistente.nombre +
    #             ' de la fase ' +tipoItemExistente.fase.nombre + ' del proyecto ' +tipoItemExistente.fase.proyecto.nombre+
    #             ' a la fase' + fase.nombre +' del proyecto ' + fase.proyecto.nombre )



    return HttpResponseRedirect('/changeitemtype/' + str(tipoItemNuevo.id))


@login_required()
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

            try:
                atributo.save()
            except IntegrityError as e:
                return render(request, "keyduplicate_atributo.html", {'itemtype': itemtype, "message": e.message},
                  context_instance=RequestContext(request))

            # logger.info('El usuario '+request.user.username+'  ha creado el atributo ' + atributo.nombre +
            #             ' perteneciente al tipo de item: '+ itemtype.nombre )


        return HttpResponseRedirect('/changeitemtype/'+str(id_tipoitem))
    else:
        form = CreateAtributeForm()
    return render(request, 'tipo_item/createatribute.html', {'user': request.user, 'form': form, 'project': project,
                                                             'itemtype': itemtype, 'fase': phase})


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

            # logger.info('El usuario '+request.user.username+' ha modificado el atributo (ATI-' + atribute.id +') ' +
            #             atribute.nombre + ' perteneciente al tipo de ítem: ' + itemtype.nombre )

            return HttpResponseRedirect('/changeitemtype/' + str(itemtype.id))
    else:
        form = ChangeAtributeForm(instance=atribute)
    return render(request, 'tipo_item/changeatribute.html', {'user': request.user, 'form': form, 'itemtype': itemtype,
                                                             'project': project, 'atributo': atribute, 'fase': phase})


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

    # logger.info('El usuario '+ request.user.username +' ha eliminado el atributo '  + attr.nombre +
    #             ' perteneciente al tipo de ítem: ' + attr.tipoDeItem.nombre )

    return HttpResponseRedirect('/changeitemtype/' + str(id_tipoItem))