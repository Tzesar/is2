#encoding:utf-8
from django.template import RequestContext
from django.utils import timezone
import pydot
from django.shortcuts import render

from administrarFases.models import Fase
from administrarFases.views import workphase
from administrarItems.models import ItemBase, ItemRelacion
from administrarLineaBase.forms import createLBForm
from administrarLineaBase.models import LineaBase
from administrarTipoItem.models import TipoItem
from is2.settings import MEDIA_ROOT


def createLB(request, id_fase):
    """
    Esta es la vista para la creación de Linea Base
    """
    fase = Fase.objects.get(pk=id_fase)
    tipoitem = TipoItem.objects.filter(fase=fase)
    items = ItemBase.objects.filter(tipoitem=tipoitem)
    proyecto = fase.proyecto
    itemsVAL = items.filter(estado='VAL')

    if itemsVAL:
        if request.method == 'POST':
            form = createLBForm(request.POST)
            if form.is_valid():
                lineaBase = form.save(commit=False)
                lineaBase.fase = fase
                lineaBase.fecha_creacion = timezone.now()
                lineaBase.fecha_modificacion = timezone.now()
                lineaBase.save()
                for item in itemsVAL:
                    item.estado = 'ELB'
                    item.linea_base = LineaBase.objects.get(pk=lineaBase.id, fase=fase)
                    item.save()


                # Activamos la siguiente fase al crear la primera linea base
                cantFases = Fase.objects.filter(proyecto=proyecto).count()
                if fase.nro_orden != cantFases:
                    ordenNext = fase.nro_orden + 1
                    faseSgte = Fase.objects.get(proyecto=proyecto, nro_orden=ordenNext)
                    if faseSgte.estado == 'PEN':
                        faseSgte.estado = 'DES'
                        faseSgte.save()

                mensaje = 'Linea Base establecida'
                error = 0
                request.method = 'GET'
                return workphase(request, id_fase, error=error, message=mensaje)
        else:
            form = createLBForm()
        return render(request, 'createLineaBase.html', {'form': form, 'proyecto': proyecto,
                                                        'user': request.user, 'fase':fase, })
    else:
        mensaje = 'Error al crear Linea Base. No existen items VALIDADOS en la fase'
        error = 1
        return workphase(request, id_fase, error=error, message=mensaje)


def calculoImpacto(padres, hijos, costo, tiempo, grafo):
    """
    Vista para realizar el calculo de impacto
    """

    if padres:
        padre = padres.pop()
        item = ItemBase.objects.get(pk=padre)
        costo.append(item.costo)
        tiempo.append(item.tiempo)

        item_hijos = list(ItemRelacion.objects.filter(itemPadre=padre).values_list('itemHijo', flat=True))
        hijos.extend(item_hijos)
        padres.extend(item_hijos)

        for articulo in item_hijos:
            arista = pydot.Edge(padre, articulo )
            grafo.add_edge(arista)

        calculoImpacto(padres, hijos, costo, tiempo, grafo )

    else:
        return (costo, tiempo)


def generarCalculoImpacto(request, id_item):
    """
    Vista para la creación del resumen del calculo de impacto de relaciones
    """
    usuario = request.user
    item = ItemBase.objects.get(pk=id_item)
    tipoitem = item.tipoitem
    fase = tipoitem.fase
    proyecto = fase.proyecto

    grafo = pydot.Dot(graph_type='graph')
    costo = []
    tiempo = []
    padres = [id_item]
    hijos = []

    calculoImpacto(padres, hijos, costo, tiempo, grafo)
    costo = sum(costo)
    tiempo = sum(tiempo)
    direccion = MEDIA_ROOT + 'grafos/' + item.nombre + '.png'
    graph = grafo.write(direccion, format='png')


    return render(request, 'lineabase/calculoimpacto.html', {'user':usuario, 'fase':fase, 'item':item, 'proyecto':proyecto,
                                                            'costo': costo, 'tiempo':tiempo, 'grafo':graph, 'direccion':direccion },
                                                            context_instance=RequestContext(request))



