#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.utils import timezone

from administrarItems.forms import itemForm, campoEnteroForm, campoImagenForm, campoTextoCortoForm, campoFileForm
from administrarItems.models import ItemBase, CampoImagen, CampoNumero, CampoFile, CampoTextoCorto, CampoTextoLargo, ItemRelacion
from administrarRolesPermisos.decorators import *
import reversion

@login_required()
@reversion.create_revision()
def createItem(request, id_fase):
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
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    if request.method == 'POST':
        form = itemForm(request.POST)
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=id_fase)
        if form.is_valid():
            item = form.save(commit=False)
            item.fecha_modificacion = timezone.now()
            item.usuario = usuario
            item.usuario_modificacion = usuario

            item.save()

            return HttpResponseRedirect('/workproject/' + str(proyecto.id))
    else:
        form = itemForm()
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=id_fase)
    return render(request, 'item/createitem.html', {'form': form, 'fase': fase, 'proyecto': proyecto,
                                                    'user': usuario}, context_instance=RequestContext(request))


@login_required()
@reversion.create_revision()
def changeItem(request, id_item):
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

    item = ItemBase.objects.get(pk=id_item)
    tipoItem = item.tipoitem
    phase = tipoItem.fase
    project = phase.proyecto
    numero = CampoNumero.objects.get(item=item)
    if request.method == 'POST':
        form = itemForm(request.POST, instance=item)
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=phase.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.fecha_modificacion = timezone.now()
            item.usuario_modificacion = request.user
            item.save()

            reversion.create_revision(numero)

            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = itemForm(instance=item)
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=phase.id)
    return render(request, 'item/changeitem.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user},
                                                    context_instance=RequestContext(request))

@reversion.create_revision()
def completarEnteros(request, id_atributo, id_item):
    """
    Vista para completar el atributo de numeros
    :rtype : object
    """
    id_atributo = 10
    atributo = Atributo.objects.get(pk=id_atributo)
    tipoItem = atributo.tipoDeItem
    item = ItemBase.objects.get(pk=id_item)

    phase = tipoItem.fase
    project = phase.proyecto
    if request.method == 'POST':
        form = campoEnteroForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.item = item
            articulo.atributo = atributo
            articulo.save()


            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = campoEnteroForm()
    return render(request, 'item/fillatributos.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user, 'attr':atributo},
                                                    context_instance=RequestContext(request))

@reversion.create_revision()
def completarTexto(request, id_atributo, id_item):
    """
    Vista para completar el atributo de numeros
    :rtype : object
    """
    id_atributo = 12
    atributo = Atributo.objects.get(pk=id_atributo)
    tipoItem = atributo.tipoDeItem
    item = ItemBase.objects.get(pk=id_item)

    phase = tipoItem.fase
    project = phase.proyecto
    if request.method == 'POST':
        form = campoTextoCortoForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.item = item
            articulo.atributo = atributo
            articulo.save()



            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = campoTextoCortoForm()
    return render(request, 'item/fillatributos.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user, 'attr':atributo},
                                                    context_instance=RequestContext(request))

@reversion.create_revision()
def completarArchivo(request, id_atributo, id_item):
    """
    Vista para completar el atributo de numeros
    :rtype : object
    """
    id_atributo = 13
    atributo = Atributo.objects.get(pk=id_atributo)
    tipoItem = atributo.tipoDeItem
    item = ItemBase.objects.get(pk=id_item)

    phase = tipoItem.fase
    project = phase.proyecto
    if request.method == 'POST':
        form = campoFileForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.item = item
            articulo.atributo = atributo
            articulo.save()
            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = campoFileForm()
    return render(request, 'item/filesatributos.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user, 'attr':atributo},
                                                    context_instance=RequestContext(request))

@reversion.create_revision()
def completarImagen(request, id_atributo, id_item):
    """
    Vista para completar el atributo de numeros
    :rtype : object
    """
    id_atributo = 14
    id_item = 5
    atributo = Atributo.objects.get(pk=id_atributo)
    item = ItemBase.objects.get(pk=id_item)
    tipoItem = atributo.tipoDeItem
    phase = tipoItem.fase
    project = phase.proyecto

    if request.method == 'POST':
        form = campoImagenForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.item = item
            imagen.atributo = atributo
            imagen.save()
            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = campoImagenForm()
    return render_to_response('item/filesatributos.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user, 'attr':atributo},
                                                    context_instance=RequestContext(request))


def historial_ItemBase(request, id_fase, id_item):
    """
    Vista para el historial de versiones
    """

    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    item = ItemBase.objects.get(pk=id_item)
    lista_versiones = reversion.get_unique_for_object(item)
    return render('item/historial_item.html', {'lista_versiones': lista_versiones, 'item': item,
                                              'proyecto': proyecto, 'fase': fase, 'user': usuario},
                                               context_instance=RequestContext(request))


def reversion_ItemBase(request, id_item, id_fase, id_version):
    """
    Vista para la reversión de ítem
    """
    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto
    item = ItemBase.objects.get(pk=id_item)
    lista_version = reversion.get_unique_for_object(item)
    id_new_version = int('0'+id_version)
    lista_item = ItemBase.objects.filter(fase=fase)


    for version in lista_version:
        if version.id == id_new_version:
            version.revert()
            return render('item/historial_item.html', {'item': item, 'exito': 0, 'message': 'La version se ha recuperado exitosamente',
                                              'proyecto': proyecto, 'fase': fase, 'user': usuario, 'version': version},
                                               context_instance=RequestContext(request))


def relacionar_item(request, id_proyecto, id_item_hijo, id_item_padre, id_fase_padre, id_fase_hijo):
    """
    Vista para relaciones los items
    """
    usuario = request.user
    #TODO: añadir la numeracion a las fases/ solo listar items de la fase actual y la fase inmediante anterior con estado ELB
    item_hijo = ItemBase.objects.get(pk=id_item_hijo)
    item_padre = ItemBase.objects.get(pk=id_item_padre)
    fase_padre = Fase.objects.get(pk=id_fase_padre)
    fase_hijo = Fase.objects.get(pk=id_fase_hijo)
    ItemRelacion.objects.get(itemHijo=item_hijo)

    #TODO: Check si funciona
    ItemRelacion.save(item_hijo, item_padre)

  # ItemRelacion.itemHijo = item_hijo
  # ItemRelacion.itemPadre = item_padre
  #
  #  ItemRelacion.estado = 'ACT'

        #TODO: Regresar a workphase con un mensaje de exito
