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

            return HttpResponseRedirect('/workphase/' + str(fase.id))

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
    items = ItemBase.objects.filter(pk=id_item)
    if items:
        print 'Inicio de Proceso de Modificacion'
    else:
        return

    item = ItemBase.objects.get(pk=id_item)
    tipoItem = item.tipoitem
    phase = tipoItem.fase
    project = phase.proyecto

    if request.method == 'POST':
        form = itemForm(request.POST, instance=item)
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=phase.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.fecha_modificacion = timezone.now()
            item.usuario_modificacion = request.user
            item.version = reversion.get_unique_for_object(item).__len__() + 1
            item.save()

            return HttpResponseRedirect('/workphase/' + str(phase.id))
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


def historialItemBase(request, id_fase, id_item):
    """
    Vista para el historial de versiones
    """

    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    item = ItemBase.objects.get(pk=id_item)
    lista_versiones = reversion.get_unique_for_object(item)
    return render_to_response('item/historialitem.html', {'lista_versiones': lista_versiones, 'item': item,
                                              'proyecto': proyecto, 'fase': fase, 'user': usuario},
                                               context_instance=RequestContext(request))


def reversionItemBase(request, id_item, id_fase, id_version):
    """
    Vista para la reversión de ítem
    """
    fase = Fase.objects.get(pk=id_fase)
    item = ItemBase.objects.get(pk=id_item)
    lista_version = reversion.get_unique_for_object(item)
    id_new_version = int('0'+id_version)
    ti = TipoItem.objects.filter(fase=fase)
    itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

    for version in lista_version:
        if version.id == id_new_version:
            version.revert()
            mensaje = 'El item fue Reversionado correctamente.'
            error = 0
            return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'error': error,
                                                        'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                        context_instance=RequestContext(request))


#TODO: Insertar en workitem
def relacionarItemBase(request, id_item_hijo, id_item_padre, id_fase):
    """
    Vista para relaciones los items
    """
    fase = Fase.objects.get(pk=id_fase)
    item_hijo = ItemBase.objects.get(pk=id_item_hijo)
    item_padre = ItemBase.objects.get(pk=id_item_padre)
    ti = TipoItem.objects.filter(fase=fase)
    itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

    try:
        ItemRelacion.objects.get(itemHijo=item_hijo)
    except:
        relacion = ItemRelacion()
        relacion.itemHijo = item_hijo
        relacion.itemPadre = item_padre
        relacion.save()
        mensaje = 'Exito al crear la relacion'
        error = 0
        return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item_hijo, 'error': error,
                                                    'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))

    mensaje = 'Ud ya tiene un Padre.'
    error = 1
    return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item_hijo, 'duplicado': error,
                                                       'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                        context_instance=RequestContext(request))

#TODO: Insertar en workitem
def relacionarItemBaseView(request, id_fase_actual, id_item_actual):
    """
    Vista para relacionar items
    """
    item = ItemBase.objects.get(pk=id_item_actual)
    tipoitem = item.tipoitem
    fase_actual = Fase.objects.get(pk=id_fase_actual)
    proyecto = fase_actual.proyecto
    item_hijos = ItemRelacion.objects.filter(itemPadre=id_item_actual).values_list('itemHijo', flat=True)
    item_lista_fase_actual = ItemBase.objects.filter(tipoitem=tipoitem).exclude(pk=id_item_actual).exclude(pk__in=item_hijos)

    if fase_actual.nro_orden == 1:
        return render(request, 'item/relacionaritemvista.html', {'item': item, 'fase': fase_actual, 'proyecto': proyecto,
                      'itemlista': item_lista_fase_actual, 'user': request.user}, context_instance=RequestContext(request))

    else:
        orden_anterior = fase_actual.nro_orden - 1
        fase_anterior = Fase.objects.get(nro_orden=orden_anterior)
        tipoitem_anterior = TipoItem.objects.get(fase=fase_anterior)
        item_lista_fase_anterior = ItemBase.objects.filter(tipoitem=tipoitem_anterior, estado='ELB')
        return render(request, 'item/relacionaritemvista.html', {'item': item, 'fase': fase_actual, 'proyecto': proyecto,
                      'itemlistaanterior': item_lista_fase_anterior, 'fase_anterior': fase_anterior,
                      'itemlista': item_lista_fase_actual, 'user': request.user}, context_instance=RequestContext(request))


#TODO: Insertar en workitem
def validarItem(request, id_item):
    """
    Vista para validar un item, previa aprovación del cliente
    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase
    ti = TipoItem.objects.filter(fase=fase)
    itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

    if item.estado == 'FIN':
        item.estado = 'VAL'
        item.save()
        mensaje = 'Item validado correctamente y listo para pasar a Linea Base'
        error = 0
        return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'duplicado': error,
                                                    'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))

    else:
        mensaje = 'Item no puede ser validado, deberia tener un estado Finalizado antes de ser Validado '
        error = 1
        return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'duplicado': error,
                                                    'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))

#TODO: Insertar en workitem
def finalizarItem(request, id_item):
    """
    Vista para validar un item, previa aprovación del cliente
    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase
    ti = TipoItem.objects.filter(fase=fase)
    itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

    if item.estado == 'ACT':
        item.estado = 'FIN'
        item.save()
        mensaje = 'Item finalizado correctamente y listo para ser verificado por el cliente'
        error = 0
        return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'error': error,
                                                    'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))

    else:
        mensaje = 'Item no puede ser finalizado, deberia tener un estado Activo antes de ser Finalizado '
        error = 1
        return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'error': error,
                                                    'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))


def dardebajaItem(request, id_item):
    """
    Vista para dar de baja un item
    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase
    ti = TipoItem.objects.filter(fase=fase)
    itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

    try:
        ItemRelacion.objects.get(itemPadre=item)
    except:
        if item.estado != 'ELB':
            item.estado = 'DDB'
            item.save()
            try:
                ItemRelacion.objects.get(itemHijo=item)
            except:
                mensaje = 'El item fue Dado de Baja correctamente.'
                error = 0
                return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'error': error,
                                                            'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                            context_instance=RequestContext(request))
            itemRelacion = ItemRelacion.objects.get(itemHijo=item)
            itemRelacion.estado = 'DES'
            itemRelacion.save()
            mensaje = 'El item fue Dado de Baja correctamente.'
            error = 0
            return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'error': error,
                                                        'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                        context_instance=RequestContext(request))

    existePadre = ItemRelacion.objects.get(itemPadre=item)
    if existePadre:
        mensaje = 'Item no puede darse de baja, el item posse una relación de Padre con algún otro item. Favor verificar las relaciones del ítem '
        error = 1
        return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'error': error,
                                                    'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))


    else:
        mensaje = 'Item no puede darse de baja, el item forma parte de una Linea Base. '
        error = 1
        return render(request, 'fase/workPhase.html', {'mensaje':mensaje, 'user':request.user, 'item':item, 'error': error,
                                                    'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))


def restaurarItem(request, id_item):
    """
    Vista para restaurar un item que fue dado de baja
    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase
    ti = TipoItem.objects.filter(fase=fase)
    itemsFase = ItemBase.objects.filter(tipoitem__in=ti).order_by('fecha_creacion')

    try:
        ItemRelacion.objects.get(itemHijo=item)
    except:
        print 'El item no posee padre'
        item.estado = 'ACT'
        item.save()
        mensaje = 'Item restaurado exitosamente'
        error = 0
        return render(request, 'fase/workPhase.html', {'mensaje': mensaje, 'user':request.user, 'item':item, 'duplicado': error,
                                                   'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))


    padres = []
    hijos = [id_item]
    restaurarItemRelacion(padres, hijos)
    print padres
    for padre in padres:
        itemPadre = ItemBase.objects.get(pk=padre)
        if itemPadre.estado != 'DDB':
            relacion = ItemRelacion.objects.get(itemHijo=item)
            relacion.itemPadre = itemPadre
            relacion.save()
            item.estado = 'ACT'
            item.save()


    mensaje = 'Item restaurado exitosamente'
    error = 0
    return render(request, 'fase/workPhase.html', {'mensaje': mensaje, 'user':request.user, 'item':item, 'duplicado': error,
                                                   'fase':fase, 'proyecto':fase.proyecto, 'listaItems': itemsFase},
                                                    context_instance=RequestContext(request))

def restaurarItemRelacion(padres, hijos):
    """
    Vista para realizar el calculo de impacto
    """

    if hijos:
        hijo = hijos.pop()
        item = ItemBase.objects.get(pk=hijo)

        itemPadres = ItemRelacion.objects.get(itemHijo=hijo)
        itemPadre = itemPadres.itemPadre

        item_hijos = list(ItemRelacion.objects.filter(itemHijo=itemPadre).values_list('itemHijo', flat=True))
        hijos.extend(item_hijos)
        padres.extend(item_hijos)
        restaurarItemRelacion(padres, hijos)

    else:
        return




