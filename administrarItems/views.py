#encoding:utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from administrarFases.views import workphase

from administrarItems.forms import itemForm, campoEnteroForm, campoImagenForm, campoTextoCortoForm, campoFileForm, modificarAtributosBasicosForm,\
    modificarDatosItemForm, campoTextoLargoForm, CustomInlineFormSet_NUM, CustomInlineFormSet_STR, \
    CustomInlineFormSet_TXT, CustomInlineFormSet_IMG, CustomInlineFormSet_FIL

from django.forms.models import inlineformset_factory
from administrarItems.models import ItemBase, CampoImagen, CampoNumero, CampoFile, CampoTextoCorto, CampoTextoLargo, ItemRelacion
from administrarLineaBase.views import generarCalculoImpacto, generarGrafo
from administrarRolesPermisos.decorators import *
import reversion
from administrarTipoItem.models import TipoItem, Atributo


@login_required()
@reversion.create_revision()
def createItem(request, id_fase):
    """
    *Vista para la creación de fases en el sistema.
    Opción válida para usuarios con los roles correspondientes.*

    :param request: HttpRequest necesario para crear fases dentro de los proyectos, es la solicitud de la acción.
    :param id_proyecto: Identificador del proyecto dentro del sistema al cual se le vincularán las fases creadas.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
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
                                                    'user': usuario}, )


def crearAtributos(item_id):
    """
    *Vista para la creación de atributos correspondientes según el tipo de ítem al que pertenece el ítem*

    :param item_id: Identificador del Item al cual se le vincularán los atributos creados
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: Los atributos son vinculados exitosamente al Item
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


def historialItemBase(request, id_fase, id_item):
    """
    *Funcion para visualizar el historial de versiones de los ítems. *
    Obs. Cada modificación realizada en el ítem es una nueva versión del ítem.

    :param request: HttpRequest necesario para visualizar las versiones de un ítem, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del proyecto a la cual pertenece el ítem.
    :param id_item: Identificador del Item al cual se esta consultando su historial de versiones
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: Regresa una lista de todas las versiones del ítem.
    """

    usuario = request.user
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto

    item = ItemBase.objects.get(pk=id_item)
    lista_versiones = reversion.get_unique_for_object(item)

    return render(request, 'item/historialitem.html', {'lista_versiones': lista_versiones, 'item': item,
                                              'proyecto': proyecto, 'fase': fase, 'user': usuario}, )


def reversionItemBase(request, id_item, id_fase, id_version):
    """
    *Funcion para realizar la reversión de un ítem. Una reversión consiste en recuperar todos los
    atributos definidos y la relación establecida para la versión a la cual se esta reversionando el item*

    :param request: HttpRequest necesario para establecer la reversión, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del proyecto a la cual pertenece el ítem.
    :param id_item: Identificador del Item al cual se desea realizar una reversion.
    :param id_version: Identificador de la versión a la cual se desea realizar una reversion.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: El ítem es reversionado exitosamente.
    """
    fase = Fase.objects.get(pk=id_fase)
    item = ItemBase.objects.get(pk=id_item)
    tipoitem = item.tipoitem
    atributos = Atributo.objects.filter(tipoDeItem=tipoitem)
    id_new_version = int('0'+id_version)
    campos = []
    lista_version = reversion.get_unique_for_object(item)

    relacion = ItemRelacion.objects.filter(itemHijo=item)

    if relacion:
        versionRelacion = reversion.get_for_object(relacion.get())
        for version_relacion in versionRelacion:
            if version_relacion.revision.id == id_new_version:
                version_relacion.revert()

        ItemPadre = ItemRelacion.objects.get(itemHijo=item).itemPadre
        padre = ItemBase.objects.get(nombre=ItemPadre)
        if padre.estado == 'DDB':
            print 'Padre en baja'
            relacion[0].itemPadre = None
            relacion[0].save()

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


    for version in lista_version:
        if version.revision.id == id_new_version:
            version.revert()
            mensaje = 'Item: ' + item.nombre + '. Reversionado correctamente.'
            error = 0
            mensajes = list(mensaje)
            request.session['messages'] = mensajes
            request.session['error'] = error
            return workphase(request, fase.id)


@reversion.create_revision()
def relacionarItemBase(request, id_item_hijo, id_item_padre, id_fase):
    """
    *Funcion para establecer relaciones entre los items. Se pueden establecer relaciones del tipo Padre-Hijo
    cuando los ítems pertenecen a la misma fase y del tipo Antecesor-Sucesor cuando los ítem pertenecen a
    fases consecutivas.*

    :param request: HttpRequest necesario para establecer las relaciones entre ítems, es la solicitud de la acción.
    :param id_item_hijo: Identificador del ítem que cumplirá con el rol de Hijo/Sucesor en la relación.
    :param id_item_padre: Identificador del ítem que cumplirá con el rol de Padre/Antecesor en la relación.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: Relación establecida correctamente
    """
    item_hijo = ItemBase.objects.get(pk=id_item_hijo)
    item_padre = ItemBase.objects.get(pk=id_item_padre)
    mensajes = []

    try:
        ItemRelacion.objects.get(itemHijo=item_hijo)
    except:
        relacion = ItemRelacion()
        relacion.itemHijo = item_hijo
        relacion.itemPadre = item_padre
        relacion.save()
        item_hijo.fecha_modificacion = timezone.now()
        item_hijo.usuario_modificacion = request.user
        item_hijo.version = reversion.get_unique_for_object(item_hijo).__len__() + 1
        item_hijo.save()
        mensaje = 'Relacion establecida entre ' + item_hijo.nombre + ' y ' + item_padre.nombre + '.'
        mensajes.append(mensaje)
        error = 0
        request.session['messages'] = mensajes
        request.session['error'] = error
        return workphase(request, id_fase)

    relacion = ItemRelacion.objects.get(itemHijo=item_hijo)
    padre = relacion.itemPadre
    if padre == item_padre:
        mensaje = 'El item ' + item_hijo.nombre + ' ya cuenta con una relacion hacia el item especificado.'
        duplicado = 1
        mensajes.append(mensaje)
        request.session['messages'] = mensajes
        request.session['error'] = duplicado
        return workphase(request, id_fase)
    else:
        relacion.itemPadre = item_padre
        relacion.save()
        item_hijo.version = reversion.get_unique_for_object(item_hijo).__len__() + 1
        item_hijo.save()

        mensaje = 'Relacion establecida entre ' + item_hijo.nombre + ' y ' + item_padre.nombre + '.'
        error = 0
        mensajes.append(mensaje)
        request.session['messages'] = mensajes
        request.session['error'] = error
        return workphase(request, id_fase)


def relacionarItemBaseView(request, id_fase_actual, id_item_actual):
    """
    *Función que realiza el proceso de filtar los ítems disponibles para relacionar una relación, de tal forma,
    que se verifica que no se creen ciclos en las relaciones, ni tampoco relaciones inconsistentes con el sistema.

    :param request: HttpRequest necesario para filtrar los ítems dentro de las fases, es la solicitud de la acción.
    :param id_fase_actual: Identificador de la fase a la que pertenece el ítem que se desea establecer una relación.
    :param id_item_actual: Identificador del ítem al cual se le establecerá una nueva relación.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: Despliega una lista de todos los ítems habilitados para establecer una relación.
    """
    item = ItemBase.objects.get(pk=id_item_actual)
    tipoitem = item.tipoitem
    fase_actual = Fase.objects.get(pk=id_fase_actual)
    proyecto = fase_actual.proyecto
    item_hijos = ItemRelacion.objects.filter(itemPadre=id_item_actual).values_list('itemHijo', flat=True)
    item_lista_fase_actual = ItemBase.objects.filter(tipoitem=tipoitem).exclude(pk=id_item_actual).exclude(pk__in=item_hijos)
    mensajes = []

    if fase_actual.nro_orden == 1:
        if item_lista_fase_actual:
            return render(request, 'item/relacionaritemvista.html', {'item': item, 'fase': fase_actual, 'proyecto': proyecto,
                      'itemlista': item_lista_fase_actual, 'user': request.user}, )
        else:
            error=1
            mensaje= 'No existen items con los cuales relacionarse'
            mensajes.append(mensaje)
            request.session['messages'] = mensajes
            request.session['error'] = error
            return workphase(request, id_fase_actual)
    else:
        orden_anterior = fase_actual.nro_orden - 1
        fase_anterior = Fase.objects.get(proyecto=proyecto, nro_orden=orden_anterior)
        tipoitem_anterior = TipoItem.objects.filter(fase=fase_anterior)
        item_lista_fase_anterior = ItemBase.objects.filter(tipoitem__in=tipoitem_anterior, estado='ELB')

        return render(request, 'item/relacionaritemvista.html', {'item': item, 'fase': fase_actual, 'proyecto': proyecto,
                      'itemlistaanterior': item_lista_fase_anterior, 'fase_anterior': fase_anterior,
                      'itemlista': item_lista_fase_actual, 'user': request.user}, )


def validarItem(request, id_item):
    """
    *Función para realizar la validación correcta de un item. La validación consiste en realizar una entrevista
     con el cliente de tal manera ha explicar el desarrollo del ítem y que se encuentre aprobado por él.*
     Obs. Solo el Lider de Proyecto puede realizar esta operación.

    :param request: HttpRequest necesario para marcar el ítem que se desea validar, es la solicitud de la acción.
    :param id_item: Identificador del Item, el cual se desea Validar por el cliente.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: El ítem es validado exitosamente.

    """
    item = ItemBase.objects.get(pk=id_item)
    error = 0
    mensajes = []

    if item.estado == 'FIN':
        item.estado = 'VAL'
        item.fecha_modificacion = timezone.now()
        item.usuario_modificacion = request.user
        item.save()
        mensajes.append('Item validado correctamente y listo para pasar a Linea Base')
        error = 0

    else:
        mensajes.append('Item no puede ser validado. El mismo debe finalizarse primero.')
        error = 1

    request.session['messages'] = mensajes
    request.session['error'] = error
    return HttpResponseRedirect(reverse('administrarFases.views.workphase', kwargs={'id_fase': item.tipoitem.fase_id}))


def finalizarItem(request, id_item):
    """
    *Función para realizar la finalización correcta de un item. La finalización consiste en finalizar el
    desarrollo de un ítem, y luego espera a ser validado por parte del cliente.*
    Obs. Solo el Lider de Proyecto puede realizar esta operación.

    :param request: HttpRequest necesario para marcar el ítem que se desea finalizar, es la solicitud de la acción.
    :param id_item: Identificador del Item, el cual se desea Finalizar.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: El ítem es finalizado exitosamente.

    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase
    error = 0
    mensajes = []

    if item.estado == 'ACT':
        try:
            relacion = ItemRelacion.objects.get(itemHijo=item)
        except:
            relacion = None

        if relacion:
            if relacion.itemPadre == None and item.tipoitem.fase.nro_orden != 1:
                error = 1
                mensajes.append('No se puede Finalizar el item. Se precisa especificar su relacion con otro item')
        elif item.tipoitem.fase.nro_orden != 1:
            error = 1
            mensajes.append('No se puede Finalizar el item. Se precisa especificar su relacion con otro item')

    else:
        mensajes.append('Item: ' + item.nombre + ' no puede ser finalizado. Deberia tener un estado Activo.')
        error = 1

    if error == 0:
        item.estado = 'FIN'
        item.fecha_modificacion = timezone.now()
        item.usuario_modificacion = request.user
        item.save()
        mensajes.append('Item: ' + item.nombre + ', finalizado y listo para su validacion')

    request.session['messages'] = mensajes
    request.session['error'] = error
    return HttpResponseRedirect(reverse('administrarFases.views.workphase', kwargs={'id_fase': fase.id}))
    # return workphase(request, fase.id)


def dardebajaItem(request, id_item):
    """
    *Función para Dar de Baja un item. Dar de Baja consiste en el borrado lógico del ítem, es decir, este pasa
    a un estado de inactividad en donde el ítem ya no puede ser desarrollado. Y si se desea volver a trabajar con
    él se debe realizar una restauración. Cuando se Da de Baja un ítem, tambíen sucede con la relación que pasa
    a un estado inactivo.*
    Obs. No se pueden dar de baja ítems que poseen un rol de Padre/Antecesor en alguna relación.

    :param request: HttpRequest necesario para marcar el ítem que se desea Dar de Baja, es la solicitud de la acción.
    :param id_item: Identificador del Item, el cual se desea Dar de Baja.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: El ítem es dado de baja exitosamente.
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
                mensajes = list(mensaje)
                request.session['messages'] = mensajes
                request.session['error'] = error
                return workphase(request, fase.id)

            itemRelacion = ItemRelacion.objects.get(itemHijo=item)
            itemRelacion.estado = 'DES'
            itemRelacion.save()
            mensaje = 'Item: ' + item.nombre + '. Dado de Baja correctamente.'
            error = 0
            mensajes = list(mensaje)
            request.session['messages'] = mensajes
            request.session['error'] = error
            return workphase(request, fase.id)

    esPadre = ItemRelacion.objects.filter(itemPadre=item, estado='ACT')
    if esPadre:
        mensaje = 'Item no puede darse de baja, el item posse una relación de Padre con algún otro item. Favor verificar las relaciones del ítem '
        error = 1
        mensajes = list(mensaje)
        request.session['messages'] = mensajes
        request.session['error'] = error
        return workphase(request, fase.id)
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
            mensajes = list(mensaje)
            request.session['messages'] = mensajes
            request.session['error'] = error
            return workphase(request, fase.id)

        itemRelacion = ItemRelacion.objects.get(itemHijo=item)
        itemRelacion.estado = 'DES'
        itemRelacion.save()

        mensaje = 'Item: ' + item.nombre + '. Dado de Baja correctamente.'
        error = 0
        mensajes = list(mensaje)
        request.session['messages'] = mensajes
        request.session['error'] = error
        return workphase(request, fase.id)


def restaurarItem(request, id_item):
    """
    *Función para Restaurar un item que fue Dado de Baja. Restaurar consiste en realizar una activación del
    ítem que fue dado de baja anteriormente de tal manera a recuperar la realción que y los atributos del ítem.
    En caso de ocurrir una inconsistencia al realizar una recuperación, el sistema automaticamento lo relacionará
    con el ancestro más próximo.*
    Obs. No se pueden dar de baja ítems que poseen un rol de Padre/Antecesor en alguna relación.

    :param request: HttpRequest necesario para marcar el ítem que se desea Restaurar, es la solicitud de la acción.
    :param id_item: Identificador del Item, el cual se desea Dar de Baja.
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: El ítem es restaurado correctamente.

    """
    item = ItemBase.objects.get(pk=id_item)
    fase = item.tipoitem.fase

    try:
        ItemRelacion.objects.get(itemHijo=item)
    except:
        item.estado = 'ACT'
        item.save()

        mensaje = 'Item ' + item.nombre + ' restaurado exitosamente'
        error = 0
        mensajes = list(mensaje)
        request.session['messages'] = mensajes
        request.session['error'] = error
        return workphase(request, fase.id)

    padres = []
    hijos = [id_item]
    restaurarItemRelacion(padres, hijos)
    for padre in padres:
        itemPadre = ItemBase.objects.get(pk=padre)
        if itemPadre.estado != 'DDB':
            relacion = ItemRelacion.objects.get(itemHijo=item)
            relacion.itemPadre = itemPadre
            relacion.save()
            item.estado = 'ACT'
            item.save()

    mensaje = 'Item ' + item.nombre + ' restaurado exitosamente'
    error = 0
    mensajes = list(mensaje)
    request.session['messages'] = mensajes
    request.session['error'] = error
    return workphase(request, fase.id)


def restaurarItemRelacion(padres, hijos):
    """
    *Función auxiliar de la restauración de ítems que permite restaurar la relación del mismo.
    Cumple con la función de realizar el recorrido entre todos los ancestros de un ítem en caso de que
    el padre no se encuentre en estado disponible para establecer una nueva relación.*

    :param padres: Lista que contiene el identificador de los ítems que cumplen con el rol de Padre en la relación.
    :param hijos: Lista que contiene el identificador de los ítems que cumplen con el rol de Hijo en la relación.
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
def workItem(request, id_item):
    """
    *Vista para el desarrollo de ítems creados en una Fase de un Proyecto.
    Opción válida para usuarios asociados a un proyecto, con permisos de creación
    y modificación de ítems en la Fase en cuestión*

    *En caso de que el método de la solicitud HTTP sea GET, gestiona un formulario
    con los datos actueles del ítem y sus atributos. En el caso de que el método sea POST,
    gestiona la actualización de los datos del ítem y sus atributos en la base de datos.*

    :param request: Solicitud HTTP relacionada a la ejecución de esta vista.
    :param id_item: Identificador del ítem sobre el cual se desea trabajar.
    :param error: Indicador de la existencia de errores en los formularios.
    :param message: Mensaje de error o de éxito a ser desplegado según corresponda.
    :return: Proporciona la pagina ``workitem.html``, página dedicada al desarrollo del ítem especificado.
    """
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
            if item.estado != 'REV':
                item.estado = 'ACT'
            item.version = reversion.get_unique_for_object(item).__len__() +1
            item.save()

            no_error = 0
            mensaje = 'Item: ' + item.nombre + '. Modificacion exitosa.'
            mensajes = list(mensaje)
            request.session['messages'] = mensajes
            request.session['error'] = no_error
            return HttpResponseRedirect(reverse('administrarFases.views.workphase',
                                                kwargs={'id_fase': faseActual.id}))
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
                                                  'formTXT': formTXT_list, 'formSTR': formSTR_list,
                                                  'formFile': formFile_list, 'formIMG': formIMG_list,
                                                  'existen_formNumericos': existen_NUM, 'existen_formSTR': existen_STR,
                                                  'existen_formTXT': existen_TXT, 'existen_formIMG': existen_IMG,
                                                  'existen_formFile': existen_FIL},)


def formsValidos(formDatosItem, formAtributosBasicos, formNum_list, formSTR_list, formTXT_list,
                        formIMG_list, formFile_list, existen_FIL, existen_TXT, existen_NUM, existen_IMG, existen_STR):
    """
    *Función que verifica la validez de los formularios y conjuntos de formularios* - ``formsets`` -
    que son cargados durante el trabajo sobre un ítem*

    :param formDatosItem: Formulario de modificación de datos generales de un ítem.
                          Incluye datos tales como el Nombre y la Descripción del ítem en cuestión.
    :param formAtributosBasicos: Formulario de modificación de los atributos básicos asociados
                          a cada ítem. Incluye: Complejidad, Costo y Tiempo.
    :param existen_NUM: Indicador booleano de la existencia de atributos numéricos en el ítem considerado.
    :param formNum_list: Conjunto de formularios destinados a modificar atributos de tipo numérico
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_STR: Indicador booleano de la existencia de atributos de texto cortos en el ítem
                          que se considera.
    :param formSTR_list: Conjunto de formularios destinados a modificar atributos de tipo texto corto
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_TXT: Indicador booleano de la existencia de atributos de texto largos en el ítem
                          que se considera.
    :param formTXT_list: Conjunto de formularios destinados a modificar atributos de tipo texto largo
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_IMG: Indicador booleano de la existencia de atributos de tipo Imagen en el ítem
                          que se considera.
    :param formIMG_list: Conjunto de formularios destinados a modificar atributos de tipo Imagen
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_FIL: Indicador booleano de la existencia de atributos de tipo Archivo en el ítem
                          que se considera.
    :param formFile_list: Conjunto de formularios destinados a modificar atributos de tipo Archivo
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :rtype: bool
    :return: Indicador booleano de la validez o no de la totalidad de los formularios con los que se trabaja
             en el ítem indicado.
    """
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


def saveForms(formDatosItem, formAtributosBasicos, formNum_list, formSTR_list, formTXT_list,
                        formIMG_list, formFile_list, existen_FIL, existen_TXT, existen_NUM, existen_IMG, existen_STR):
    """
    *Función que almacena los datos que se recibieron a través de los formularios de trabajo con un ítem
    una vez los mismos hayan pasado por la prueba de validez*

    :param formDatosItem: Formulario de modificación de datos generales de un ítem.
                          Incluye datos tales como el Nombre y la Descripción del ítem en cuestión.
    :param formAtributosBasicos: Formulario de modificación de los atributos básicos asociados
                          a cada ítem. Incluye: Complejidad, Costo y Tiempo.
    :param existen_NUM: Indicador booleano de la existencia de atributos numéricos en el ítem considerado.
    :param formNum_list: Conjunto de formularios destinados a modificar atributos de tipo numérico
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_STR: Indicador booleano de la existencia de atributos de texto cortos en el ítem
                          que se considera.
    :param formSTR_list: Conjunto de formularios destinados a modificar atributos de tipo texto corto
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_TXT: Indicador booleano de la existencia de atributos de texto largos en el ítem
                          que se considera.
    :param formTXT_list: Conjunto de formularios destinados a modificar atributos de tipo texto largo
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_IMG: Indicador booleano de la existencia de atributos de tipo Imagen en el ítem
                          que se considera.
    :param formIMG_list: Conjunto de formularios destinados a modificar atributos de tipo Imagen
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    :param existen_FIL: Indicador booleano de la existencia de atributos de tipo Archivo en el ítem
                          que se considera.
    :param formFile_list: Conjunto de formularios destinados a modificar atributos de tipo Archivo
                          asociados al ítem con el que se trabaja, en caso de que exista al menos uno
                          de este tipo.
    """
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


def changeItem(request, id_item):
    """
        *Vista para la modificacion de una fase dentro del sistema.*
        *Opción válida para usuarios con los roles correspondientes.*

        :param request: HttpRequest necesario para modificar la fase, es la solicitud de la acción.
        :param id_fase: Identificador de la fase dentro del sistema la cual se desea modificar.
        :param args: Argumentos para el modelo ``Fase``.
        :param kwargs: Keyword Arguments para la el modelo ``Fase``.
        :return: Proporciona la pagina ``changephase.html`` con el formulario correspondiente.
                 Modifica la fase especifica y luego regresa al menu principal

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
                                                    'tiposItem': tipoItem, 'user': request.user}, )


def verItem(request, id_item):
    """
    *Función que permite visualizar un ítem junto con sus atributos y su grafo de relaciones.*

    :param request: HttpRequest necesario para seleccionar el ítem que se desea visualizar, es la solicitud de la acción.
    :param id_item: Identificador del ítem el cual se desea visualizar.
    :return: Regresa el los datos del ítem para su consulta.
    """
    item = ItemBase.objects.get(pk=id_item)
    tipoItem = item.tipoitem
    fase = tipoItem.fase
    proyecto = fase.proyecto

    numericos = CampoNumero.objects.filter(item=item)
    cadenas = CampoTextoCorto.objects.filter(item=item)
    textos = CampoTextoLargo.objects.filter(item=item)
    imagenes = CampoImagen.objects.filter(item=item)
    archivos = CampoFile.objects.filter(item=item)

    generarGrafo(id_item)
    grafoRelaciones = '/static/grafos/' + item.nombre

    return render(request, 'item/veritem.html', {'proyecto': proyecto, 'fase': fase, 'item': item, 'user': request.user,
                                                 'numericos': numericos, 'cadenas': cadenas, 'textosextensos': textos,
                                                 'imagenes': imagenes, 'archivos': archivos, 'grafo': grafoRelaciones})


def finRevisionItem(request, id_fase, id_item):
    """
    *Función para Finalizar de un ítem que ha entrado en una estado de Revision.
     Obs. Solo el Lider de Proyecto puede realizar esta operación. *

    :param request: HttpRequest necesario para visualizar las versiones de un ítem, es la solicitud de la acción.
    :param id_fase: Identificador de la fase dentro del proyecto a la cual pertenece el ítem.
    :param id_item: Identificador del Item al cual se esta consultando su historial de versiones
    :param args: Argumentos para el modelo ``Item``.
    :param kwargs: Keyword Arguments para la el modelo ``Item``.
    :return: Regresa una lista de todos los ítems, con el ítem finalizado correctamente e incluido nuevamente en la Base de Datos.

    """
    item = ItemBase.objects.get(pk=id_item)
    mensajes = []

    item.estado = 'ELB'
    item.save()

    message = 'Revision Finalizada para el Item:' + item.nombre
    error = 0
    mensajes.append(message)
    request.session['messages'] = mensajes
    request.session['error'] = error
    return HttpResponseRedirect(reverse('administrarFases.views.workphase', kwargs={'id_fase': id_fase}))
