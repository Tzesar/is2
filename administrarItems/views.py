#encoding:utf-8
import logging

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, render_to_response

from administrarItems.forms import itemForm, campoEnteroForm, campoImagenForm, campoTextoCortoForm, campoFileForm, \
    campoTextoLargoForm
from administrarItems.models import ItemBase
from administrarTipoItem.models import Atributo, TipoItem
from administrarRolesPermisos.decorators import *


@login_required()
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

    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    if request.method == 'POST':
        form = itemForm(request.POST)
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=id_fase)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/workproject/' + str(proyecto.id))
    else:
        form = itemForm()
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=id_fase)
    return render(request, 'item/createitem.html', {'form': form, 'fase': fase, 'proyecto': proyecto,
                                                    'user': request.user}, context_instance=RequestContext(request))


@login_required()
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
    if request.method == 'POST':
        form = itemForm(request.POST, instance=item)
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=phase.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = itemForm(instance=item)
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=phase.id)
    return render(request, 'item/changeitem.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user},
                                                    context_instance=RequestContext(request))


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
    return render(request, 'item/fillatributos.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user, 'attr':atributo},
                                                    context_instance=RequestContext(request))


def completarImagen(request, id_atributo, id_item):
    """
    Vista para completar el atributo de numeros
    :rtype : object
    """
    id_atributo = 14
    atributo = Atributo.objects.get(pk=id_atributo)
    tipoItem = atributo.tipoDeItem
    item = ItemBase.objects.get(pk=id_item)
    phase = tipoItem.fase
    project = phase.proyecto
    if request.method == 'POST':
        form = campoImagenForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.item = item
            articulo.atributo = atributo
            articulo.save()
            return HttpResponseRedirect('/workproject/' + str(project.id))
    else:
        form = campoImagenForm()
    return render(request, 'item/fillatributos.html', {'form': form, 'item': item, 'phase': phase, 'project': project,
                                                    'tiposItem': tipoItem, 'user': request.user, 'attr':atributo},
                                                    context_instance=RequestContext(request))