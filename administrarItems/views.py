#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.utils import timezone
from administrarFases.views import workphase

from administrarItems.forms import itemForm, campoEnteroForm, campoImagenForm, campoTextoCortoForm, campoFileForm, modificarAtributosBasicosForm,\
    modificarDatosItemForm, campoTextoLargoForm, CustomInlineFormSet_NUM, CustomInlineFormSet_STR, \
    CustomInlineFormSet_TXT, CustomInlineFormSet_IMG, CustomInlineFormSet_FIL

from django.forms.models import  inlineformset_factory
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

            crearAtributos(item.id)

            return HttpResponseRedirect('/workphase/' + str(fase.id))

    else:
        form = itemForm()
        form.fields['tipoitem'].queryset = TipoItem.objects.filter(fase=id_fase)
    return render(request, 'item/createitem.html', {'form': form, 'fase': fase, 'proyecto': proyecto,
                                                    'user': usuario}, context_instance=RequestContext(request))


def crearAtributos(item_id):
    """
    *Vista para la creación de atributos correspondientes según el tipo de ítem al que pertenece el ítem*
    """

    nuevoItem = ItemBase.objects.get(pk=item_id)
    atributosNumericos = Atributo.objects.filter(tipoDeItem=nuevoItem.tipoitem, tipo='NUM')
    atributosTextoLargo = Atributo.objects.filter(tipoDeItem=nuevoItem.tipoitem, tipo='TXT')
    atributosTextoCorto = Atributo.objects.filter(tipoDeItem=nuevoItem.tipoitem, tipo='STR')
    atributosArchivo = Atributo.objects.filter(tipoDeItem=nuevoItem.tipoitem, tipo='FIL')
    atributosImagen = Atributo.objects.filter(tipoDeItem=nuevoItem.tipoitem, tipo='IMG')

    for a in atributosNumericos:
        nuevoAtributo = CampoNumero(atributo=a, item=nuevoItem, valor=0)
        nuevoAtributo.save()

    for a in atributosTextoCorto:
        nuevoAtributo = CampoTextoCorto(atributo=a, item=nuevoItem, valor='<default>')
        nuevoAtributo.save()

    for a in atributosTextoLargo:
        nuevoAtributo = CampoTextoLargo(atributo=a, item=nuevoItem, valor='<default>')
        nuevoAtributo.save()

    for a in atributosArchivo:
        nuevoAtributo = CampoFile(atributo=a, item=nuevoItem)
        nuevoAtributo.save()

    for a in atributosImagen:
        nuevoAtributo = CampoImagen(atributo=a, item=nuevoItem)
        nuevoAtributo.save()

#TODO: Eliminar si no se usa
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

#TODO: Eliminar si no se usa
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

#TODO: Eliminar si no se usa
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

#TODO: Eliminar si no se usa
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
    *Vista para el historial de versiones de los ítems*
    Obs. Cada modificación realizada en el ítem es una nueva versión del ítem.
    """

    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    item = ItemBase.objects.get(pk=id_item)
    lista_versiones = reversion.get_unique_for_object(item)

    return render(request, 'item/historialitem.html', {'lista_versiones': lista_versiones, 'item': item,
                                              'proyecto': proyecto, 'fase': fase, 'user': usuario},
                                               context_instance=RequestContext(request))


def reversionItemBase(request, id_item, id_fase, id_version):
    """
    *Vista para realizar la reversión de un ítem*
    """
    fase = Fase.objects.get(pk=id_fase)
    item = ItemBase.objects.get(pk=id_item)
    tipoitem = item.tipoitem
    atributos = Atributo.objects.filter(tipoDeItem=tipoitem)
    id_new_version = int('0'+id_version)
    campos = []
    campos.extend(CampoTextoLargo.objects.filter(atributo__in=atributos, item=item))
    campos.extend(CampoTextoCorto.objects.filter(atributo__in=atributos, item=item))
    campos.extend(CampoNumero.objects.filter(atributo__in=atributos, item=item))
    campos.extend(CampoFile.objects.filter(atributo__in=atributos, item=item))
    campos.extend(CampoImagen.objects.filter(atributo__in=atributos, item=item))

    for campo in campos:
        versionAttr = reversion.get_unique_for_object(campo)
        for version_attr in versionAttr:
            if version_attr.revision.id == id_new_version:
                version_attr.revert()


    lista_version = reversion.get_unique_for_object(item)
    print id_new_version
    for version in lista_version:
        if version.revision.id == id_new_version:
            version.revert()

            mensaje = 'Item: ' + item.nombre + '. Reversionado correctamente.'
            error = 0
            return workphase(request, fase.id, error=error, message=mensaje)


def relacionarItemBase(request, id_item_hijo, id_item_padre, id_fase):
    """
    Vista para relaciones los items
    """
    item_hijo = ItemBase.objects.get(pk=id_item_hijo)
    item_padre = ItemBase.objects.get(pk=id_item_padre)

    try:
        ItemRelacion.objects.get(itemHijo=item_hijo)
    except:
        relacion = ItemRelacion()
        relacion.itemHijo = item_hijo
        relacion.itemPadre = item_padre
        relacion.save()
        item_hijo.fecha_modificacion = timezone.now()
        item_hijo.usuario_modificacion = request.user
        item_hijo.save()
        mensaje = 'Relacion establecida entre ' + item_hijo.nombre + ' y ' + item_padre.nombre + '.'
        error = 0
        return workphase(request, id_fase, error=error, message=mensaje)

    relacion = ItemRelacion.objects.get(itemHijo=item_hijo)
    padre = relacion.itemPadre
    if padre == item_padre:
        mensaje = 'El item ' + item_hijo.nombre + ' ya cuenta con una relacion hacia el item especificado.'
        duplicado = 1
        return workphase(request, id_fase, error=duplicado, message=mensaje)
    else:
        relacion = ItemRelacion.objects.get(itemHijo=item_hijo)
        relacion.delete()

        nueva_relacion = ItemRelacion(itemHijo=item_hijo, itemPadre=item_padre)
        nueva_relacion.save()

        mensaje = 'Relacion establecida entre ' + item_hijo.nombre + ' y ' + item_padre.nombre + '.'
        error = 0
        return workphase(request, id_fase, error=error, message=mensaje)


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
        if item_lista_fase_actual:
            return render(request, 'item/relacionaritemvista.html', {'item': item, 'fase': fase_actual, 'proyecto': proyecto,
                      'itemlista': item_lista_fase_actual, 'user': request.user}, context_instance=RequestContext(request))
        else:
            error=1
            mensaje= 'No existen items con los cuales relacionarse'
            return workphase(request, id_fase_actual, error=error, message=mensaje)
    else:
        orden_anterior = fase_actual.nro_orden - 1
        fase_anterior = Fase.objects.get(proyecto=proyecto, nro_orden=orden_anterior)
        tipoitem_anterior = TipoItem.objects.filter(fase=fase_anterior)
        item_lista_fase_anterior = ItemBase.objects.filter(tipoitem__in=tipoitem_anterior, estado='ELB')
        return render(request, 'item/relacionaritemvista.html', {'item': item, 'fase': fase_actual, 'proyecto': proyecto,
                      'itemlistaanterior': item_lista_fase_anterior, 'fase_anterior': fase_anterior,
                      'itemlista': item_lista_fase_actual, 'user': request.user}, context_instance=RequestContext(request))


def validarItem(request, id_item):
    """
    Vista para validar un item, previa aprovación del cliente
    """
    item = ItemBase.objects.get(pk=id_item)

    if item.estado == 'FIN':
        item.estado = 'VAL'
        item.fecha_modificacion = timezone.now()
        item.usuario_modificacion = request.user
        item.save()
        mensaje = 'Item validado correctamente y listo para pasar a Linea Base'
        error = 0
        return workphase(request, item.tipoitem.fase.id, error=error, message=mensaje)

    else:
        mensaje = 'Item no puede ser validado. El mismo debe finalizarse primero.'
        error = 1
        return workphase(request, item.tipoitem.fase.id, error=error, message=mensaje)


def finalizarItem(request, id_item):
    """
    Vista para validar un item, previa aprovación del cliente
    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase
    error = 0

    if item.estado == 'ACT':
        try:
            itemPadre = ItemRelacion.objects.get(itemHijo=item)
        except:
            itemPadre = None

        if not itemPadre and item.tipoitem.fase.nro_orden != 1:
            error = 1
            mensaje = 'No se puede Finalizar el item. Se precisa especificar su relacion con otro item'
    else:
        mensaje = 'Item: ' + item.nombre + ' no puede ser finalizado. Deberia tener un estado Activo.'
        error = 1

    if error == 0:
        item.estado = 'FIN'
        item.fecha_modificacion = timezone.now()
        item.usuario_modificacion = request.user
        item.save()
        mensaje = 'Item: ' + item.nombre + ', finalizado y listo para su validacion'

    return workphase(request, fase.id, error=error, message=mensaje)


def dardebajaItem(request, id_item):
    """
    Vista para dar de baja un item
    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase
    ti = TipoItem.objects.filter(fase=fase)

    try:
        ItemRelacion.objects.get(itemPadre=item)
    except:
        if item.estado != 'ELB':
            item.fecha_modificacion = timezone.now()
            item.usuario_modificacion = request.user
            item.estado = 'DDB'
            item.save()
            try:
                ItemRelacion.objects.get(itemHijo=item)
            except:
                mensaje = 'Item: ' + item.nombre + '. Dado de Baja correctamente.'
                error = 0
                return workphase(request, fase.id, error=error, message=mensaje)

            itemRelacion = ItemRelacion.objects.get(itemHijo=item)
            itemRelacion.estado = 'DES'
            itemRelacion.save()
            mensaje = 'Item: ' + item.nombre + '. Dado de Baja correctamente.'
            error = 0
            return workphase(request, fase.id, error=error, message=mensaje)

    esPadre = ItemRelacion.objects.filter(itemPadre=item, estado='ACT')
    if esPadre:
        mensaje = 'Item no puede darse de baja, el item posse una relación de Padre con algún otro item. Favor verificar las relaciones del ítem '
        error = 1
        return workphase(request, fase.id, error=error, message=mensaje)
    else:
        item.fecha_modificacion = timezone.now()
        item.usuario_modificacion = request.user
        item.estado = 'DDB'
        item.save()
        try:
            ItemRelacion.objects.get(itemHijo=item)
        except:
            mensaje = 'Item: ' + item.nombre + '. Dado de Baja correctamente.'
            error = 0
            return workphase(request, fase.id, error=error, message=mensaje)

        itemRelacion = ItemRelacion.objects.get(itemHijo=item)
        itemRelacion.estado = 'DES'
        itemRelacion.save()
        mensaje = 'Item: ' + item.nombre + '. Dado de Baja correctamente.'
        error = 0
        return workphase(request, fase.id, error=error, message=mensaje)


def restaurarItem(request, id_item):
    """
    Vista para restaurar un item que fue dado de baja
    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase

    try:
        ItemRelacion.objects.get(itemHijo=item)
    except:
        item.estado = 'ACT'
        item.save()
        mensaje = 'Item ' + item.nombre +' restaurado exitosamente'
        error = 0
        return workphase(request, fase.id, error=error, message=mensaje)

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

    mensaje = 'Item ' + item.nombre +' restaurado exitosamente'
    error = 0
    return workphase(request, fase.id, error=error, message=mensaje)


def restaurarItemRelacion(padres, hijos):
    """
    Vista para realizar el calculo de impacto
    """

    if hijos:
        hijo = hijos.pop()

        itemPadres = ItemRelacion.objects.get(itemHijo=hijo)
        itemPadre = itemPadres.itemPadre
        padres.append(itemPadre.id)

        item_hijos = list(ItemRelacion.objects.filter(itemHijo=itemPadre).values_list('itemHijo', flat=True))
        hijos.extend(item_hijos)
        restaurarItemRelacion(padres, hijos)

    else:
        return


@reversion.create_revision()
def workItem(request, id_item, error=None, message=None):

    item = ItemBase.objects.get(pk=id_item)
    tipoItem = item.tipoitem
    faseActual = tipoItem.fase
    proyectoActual = faseActual.proyecto
    atributos = Atributo.objects.filter(tipoDeItem=tipoItem)

    formNum_list = None
    formSTR_list = None
    formTXT_list = None
    formIMG_list = None
    formFile_list = None

    CampoNumeroFormset = inlineformset_factory(ItemBase, CampoNumero, formset=CustomInlineFormSet_NUM, form=campoEnteroForm, extra=0, can_delete=False)
    atributosNumericos = atributos.filter(tipo='NUM')
    camposNumericos = CampoNumero.objects.filter(item=item, atributo__in=atributosNumericos).order_by('id')
    existen_NUM = False
    if camposNumericos:
        existen_NUM = True

    CampoSTRFormset = inlineformset_factory(ItemBase, CampoTextoCorto, formset=CustomInlineFormSet_STR, form=campoTextoCortoForm, extra=0, can_delete=False)
    atributosSTR = atributos.filter(tipo='STR')
    camposSTR = CampoTextoCorto.objects.filter(item=item, atributo__in=atributosSTR).order_by('id')
    existen_STR = False
    if camposSTR:
        existen_STR = True

    CampoTXTFormset = inlineformset_factory(ItemBase, CampoTextoLargo, formset=CustomInlineFormSet_TXT, form=campoTextoLargoForm, extra=0, can_delete=False)
    atributosTXT = atributos.filter(tipo='TXT')
    camposTXT = CampoTextoLargo.objects.filter(item=item, atributo__in=atributosTXT).order_by('id')
    existen_TXT = False
    if camposTXT:
        existen_TXT = True

    CampoIMGFormset = inlineformset_factory(ItemBase, CampoImagen, formset=CustomInlineFormSet_IMG, form=campoImagenForm, extra=0, can_delete=False)
    atributosIMG = atributos.filter(tipo='IMG')
    camposIMG = CampoImagen.objects.filter(item=item, atributo__in=atributosIMG).order_by('id')
    existen_IMG = False
    if camposIMG:
        existen_IMG = True

    CampoFILFormset = inlineformset_factory(ItemBase, CampoFile, formset=CustomInlineFormSet_FIL, form=campoFileForm, extra=0, can_delete=False)
    atributosFIL = atributos.filter(tipo='FIL')
    camposFIL = CampoFile.objects.filter(item=item, atributo__in=atributosFIL).order_by('id')
    existen_FIL = False
    if camposFIL:
        existen_FIL = True

    if request.method == 'POST':
        formDatosItem = modificarDatosItemForm(request.POST, instance=item)
        formAtributosBasicos = modificarAtributosBasicosForm(request.POST, instance=item)

        if existen_NUM:
            formNum_list = CampoNumeroFormset(request.POST, queryset=camposNumericos, instance=item, prefix='formularios_NUM')

        if existen_STR:
            formSTR_list = CampoSTRFormset(request.POST, queryset=camposSTR, instance=item, prefix='formularios_STR')

        if existen_TXT:
            formTXT_list = CampoTXTFormset(request.POST, queryset=camposTXT, instance=item, prefix='formularios_TXT')

        if existen_IMG:
            formIMG_list = CampoIMGFormset(request.POST, request.FILES, queryset=camposIMG, instance=item, prefix='formularios_IMG')

        if existen_FIL:
            formFile_list = CampoFILFormset(request.POST, request.FILES, queryset=camposFIL, instance=item, prefix='formularios_FIL')


        if formsValidos(formDatosItem, formAtributosBasicos, formNum_list, formSTR_list, formTXT_list,
                        formIMG_list, formFile_list, existen_FIL, existen_TXT, existen_NUM, existen_IMG, existen_STR):
            reversion.create_revision()
            saveForms(formDatosItem, formAtributosBasicos, formNum_list, formSTR_list, formTXT_list,
                        formIMG_list, formFile_list, existen_FIL, existen_TXT, existen_NUM, existen_IMG, existen_STR)

            item.fecha_modificacion = timezone.now()
            item.usuario_modificacion = request.user
            item.estado = 'ACT'
            item.version = reversion.get_unique_for_object(item).__len__() +1
            item.save()

            request.method = 'GET'
            no_error = 0
            mensaje = 'Item: ' + item.nombre + '. Modificacion exitosa.'
            return workphase(request, faseActual.id, error=no_error, message=mensaje)
    else:
        formAtributosBasicos = modificarAtributosBasicosForm(instance=item)
        formDatosItem = modificarDatosItemForm(instance=item)

        if existen_NUM:
            formNum_list = CampoNumeroFormset(queryset=camposNumericos, instance=item, prefix='formularios_NUM')

        if existen_STR:
            formSTR_list = CampoSTRFormset(queryset=camposSTR, instance=item, prefix='formularios_STR')

        if existen_TXT:
            formTXT_list = CampoTXTFormset(queryset=camposTXT, instance=item, prefix='formularios_TXT')

        if existen_IMG:
            formIMG_list = CampoIMGFormset(queryset=camposIMG, instance=item, prefix='formularios_IMG')

        if existen_FIL:
            formFile_list = CampoFILFormset(queryset=camposFIL, instance=item, prefix='formularios_FIL')

    return render(request, 'item/workItem.html', {'user': request.user, 'fase': faseActual, 'proyecto': proyectoActual,
                                                  'item': item, 'formAtributosBasicos': formAtributosBasicos,
                                                  'formDatosItem': formDatosItem, 'formNumericos': formNum_list,
                                                  'formTXT': formTXT_list, 'formSTR': formSTR_list, 'formFile': formFile_list,
                                                  'formIMG': formIMG_list, 'existen_formNumericos': existen_NUM, 'existen_formSTR': existen_STR,
                                                  'existen_formTXT': existen_TXT, 'existen_formIMG': existen_IMG, 'existen_formFile': existen_FIL},
                  context_instance=RequestContext(request))


def formsValidos(formDatosItem, formAtributosBasicos, formNum_list, formSTR_list, formTXT_list,
                        formIMG_list, formFile_list, existen_FIL, existen_TXT, existen_NUM, existen_IMG, existen_STR):

    valido = True
    if formDatosItem.is_valid():
        pass
    else:
        valido = False

    if formAtributosBasicos.is_valid():
        pass
    else:
        valido = False

    if existen_NUM:
        if formNum_list.is_valid():
            pass
        else:
           valido = False

    if existen_STR:
        if formSTR_list.is_valid():
            pass
        else:
           valido = False

    if existen_TXT:
        if formTXT_list.is_valid():
            pass
        else:
           valido = False

    if existen_IMG:
        if formIMG_list.is_valid():
            pass
        else:
           valido = False

    if existen_FIL:
        if formFile_list.is_valid():
            pass
        else:
           valido = False

    return valido


#TODO: No se guardan ni las imágenes ni los archivos.
def saveForms(formDatosItem, formAtributosBasicos, formNum_list, formSTR_list, formTXT_list,
                        formIMG_list, formFile_list, existen_FIL, existen_TXT, existen_NUM, existen_IMG, existen_STR):
    formDatosItem.save()
    formAtributosBasicos.save()

    if existen_NUM:
        formNum_list.save()

    if existen_STR:
        formSTR_list.save()

    if existen_TXT:
        formTXT_list.save()

    if existen_IMG:
        formIMG_list.save()

    if existen_FIL:
        formFile_list.save()


