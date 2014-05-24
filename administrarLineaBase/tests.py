#encoding:utf-8
from django.utils import timezone
from django.test import TestCase
from django.test.client import RequestFactory
import factory
from administrarItems.models import ItemBase
from administrarLineaBase.forms import createLBForm, createSCForm
from administrarLineaBase.models import LineaBase, SolicitudCambios

from administrarProyectos.models import Proyecto
from administrarTipoItem.models import TipoItem
from autenticacion.models import Usuario
from administrarItems.views import createItem
from administrarFases.models import Fase
from administrarLineaBase.views import createLB, crearSolicitudCambios


class UsuarioFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Usuario

    username = 'admin'
    password = factory.PostGenerationMethodCall('set_password', 'admin')
    first_name = ''
    last_name = ''

    email = factory.Sequence(lambda n: 'user%d@example.com' % n)
    telefono = ''

    is_superuser = True
    is_staff = True
    is_active = True
    date_joined = timezone.now()
    last_login = timezone.now()


class ProyectoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Proyecto

    nombre = 'Proyecto01'
    lider_proyecto = Usuario.objects.get(pk='1')
    descripcion = 'Proyecto de Prueba para los Test'
    fecha_inicio = timezone.now()
    fecha_fin = timezone.now()
    estado = 'PEN'
    observaciones = 'Esto es una prueba'


class FaseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Fase

    nombre = 'Fase01'
    descripcion = 'Esta es la fase01'
    estado = 'ACT'
    proyecto = Proyecto.objects.get(pk='1')
    nro_orden = '1'


class TipoItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TipoItem

    nombre = 'TipoItem01'
    fase = Fase.objects.get(pk=1)
    descripcion = 'TipoItem01'


#class ItemFactory(factory.DjangoModelFactory):
#    FACTORY_FOR = ItemBase
#
#    usuario = Usuario.objects.get(pk='1'),
#    usuario_modificacion = Usuario.objects.get(pk='1'),
#    nombre = 'Item01',
#    descripcion = 'Esto es un Item de prueba',
#    estado = 'ACT',
#    fecha_creacion = timezone.now(),
#    fecha_modificacion = timezone.now(),
#    tipoitem = TipoItem.objects.get(pk='1'),
#    complejidad = 10,
#    costo = 10,
#    tiempo = 10,
#    version = 1,
#    linea_base = '',


class TestAdministrarSolicitudes_creacion(TestCase):

    def setUp(self):
        """
        *Creamos las estructuras necesarias para las pruebas.*
        """
        UsuarioFactory.create()
        self.user = Usuario.objects.get(username='admin')
        ProyectoFactory.lider_proyecto = self.user
        ProyectoFactory.create()
        FaseFactory.proyecto = Proyecto.objects.get(nombre='Proyecto01')
        FaseFactory.create()
        TipoItemFactory.fase = Fase.objects.get(nombre='Fase01')
        TipoItemFactory.create()
        self.factory = RequestFactory()

    def test_createSolicitud_response(self):
        """
        *Test para la vista de creacion de Solicitudes en el sistema*
        """
        print '\nInicio - Prueba: Creacion de Solicitud'
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        proyecto = Proyecto.objects.get(nombre='Proyecto01')
        fase = Fase.objects.get(nombre='Fase01')
        fase.proyecto = proyecto
        fase.save()
        tipoItem = TipoItem.objects.get(nombre='TipoItem01')
        tipoItem.fase = fase
        tipoItem.save()

        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        project = Proyecto.objects.get(nombre='Proyecto01')
        fase = Fase.objects.get(nombre='Fase01')
        fase.proyecto = project
        fase.save()
        tipoItem = TipoItem.objects.get(nombre='TipoItem01')

        print 'Creación de Item'
        dato_item_exito = {
                'usuario': self.user,
                'usuario_modificacion': self.user,
                'nombre': 'Item01',
                'descripcion': 'Esto es un Item de prueba',
                'estado': 'VAL',
                'fecha_creacion': timezone.now(),
                'fecha_modificacion': timezone.now(),
                'tipoitem': tipoItem.id,
                'complejidad': 10,
                'costo': 10,
                'tiempo': 10,
                'version': 1,
                'linea_base': 1, }

        request = self.factory.post('/createitem/', dato_item_exito)
        request.user = self.user
        response = createItem(request, fase.id)
        self.assertEqual(response.status_code, 302, 'Error al crear el Item')
        item = ItemBase.objects.get(nombre='Item01')
        print item
        print 'Item creado exitosamente'

        print '\nCreación de Linea Base [Exitosa]'

        datos_LB = {
                    'observaciones': 'LineaBase01', }

        form = createLBForm(datos_LB)
        if form.is_valid():
            linea_base = form.save(commit=False)
            linea_base.fase = fase
            linea_base.fecha_creacion = '2014-05-24'
            linea_base.fecha_modificacion = '2014-05-24'
            linea_base.save()
            print 'Linea Base creada Exitosamente'
        else:
            print form.errors
            print 'Error al crear la Linea Base'

        LB = LineaBase.objects.get(observaciones='LineaBase01')

        print LB.observaciones

        print '\nCreación de Linea Base [Error Previsto]'

        datos_LB = {
                    'obervaciones': 'LineaBase01', }

        form = createLBForm(datos_LB)
        if form.is_valid():
            linea_base = form.save(commit=False)
            linea_base.fase = fase
            linea_base.fecha_creacion = '2014-05-24'
            linea_base.fecha_modificacion = '2014-05-24'
            linea_base.save()
            print 'Linea Base creada Exitosamente'
        else:
            print 'Error al crear la Linea Base. El campo "Observaciones" es obligatorio '
            print form.errors


        print '\nCreación de Solicitud de Cambio [Exitosa]'

        datos_SC = {
                    'motivo': 'SolicitudCambios01', }

        form = createSCForm(datos_SC)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.fase = fase
            solicitud.usuario = self.user
            solicitud.costo = 10
            solicitud.tiempo = 10
            solicitud.save()
            print 'Linea Base creada Exitosamente'
        else:
            print 'Error al crear la Solicitud de Cambios. El campo "Motivo" es obligatorio '
            print form.errors

        SC = SolicitudCambios.objects.get(motivo='SolicitudCambios01')
        print 'ID. de la Solicitud Creada: ' + str(SC.id)
        print '-Motivo: ' +SC.motivo
        print '-Tiempo: ' + str(SC.tiempo) + '\n-Costo:' + str(SC.costo)
        item.solicitudes.add(SC)
        item.save()
        print '-Items a Modificar : ' + item.nombre

        print '\nCreación de Solicitud de Cambio [Error Previsto]'

        datos_SC_error = {
                    'motivo ': 'SolicitudCambios01', }

        form = createSCForm(datos_SC_error)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.fase = fase
            solicitud.usuario = self.user
            solicitud.costo = 10
            solicitud.tiempo = 10
            solicitud.save()
            print 'Linea Base creada Exitosamente'
        else:
            print 'Error al crear la Solicitud de Cambios. El campo "Motivo" es obligatorio '
            print form.errors

        print '\nFin - Prueba: Creacion de Solicitud\n'

