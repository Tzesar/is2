#encoding:utf-8
from django.utils import timezone
from django.test import TestCase
from django.test.client import RequestFactory
import factory
from administrarItems.models import ItemBase

from administrarProyectos.models import Proyecto
from administrarTipoItem.models import TipoItem
from autenticacion.models import Usuario
from administrarItems.views import createItem, changeItem
from administrarFases.models import Fase
from administrarItems.forms import itemForm


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


class TestAdministrarItems_modificacion(TestCase):
    """
    *Test para Administración de usuarios, pruebas realizadas:*
        + **Creación de Item**: Test de vista y creación de los items dentro de un proyecto.
        + **Modificacion de Item**: Test de Vista y modificación de los items.
        + **Modificar Estados del item**: Test de vista y diferentes cambios de un ítem através de su desarrollo.
    """

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


    def test_changeItem_response(self):
        """
            *Test para la vista de modificacion de fases en el sistema.*
        """
        print '\nInicio - Prueba: changeItem'
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)

        project = Proyecto.objects.get(nombre='Proyecto01')
        fase = Fase.objects.get(nombre='Fase01')
        fase.proyecto = project
        fase.save()
        tipoItem = TipoItem.objects.get(nombre='TipoItem01')
        tipoItem.fase = fase
        tipoItem.save()

        dato_item_exito = {
                  'usuario': self.user,
                  'usuario_modificacion': self.user,
                  'nombre': 'Item01',
                  'descripcion': 'Esto es un Item de prueba',
                  'estado' : 'ACT',
                  'fecha_creacion': timezone.now(),
                  'fecha_modificacion': timezone.now(),
                  'tipoitem': tipoItem.id,
                  'complejidad': 10,
                  'costo': 10,
                  'tiempo': 10,
                  'version': 1,
                  'linea_base': '', }

        form = itemForm(dato_item_exito)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario = self.user
            item.usuario_modificacion = self.user
            item.save()
        else:
            print 'Error en los datos del formulario'

        item = ItemBase.objects.get(nombre='Item01')
        print 'Prueba de Exitosa'

        dato_item_mod = {
                 'usuario': self.user,
                  'usuario_modificacion': self.user,
                  'nombre': 'Item01_Modificado',
                  'descripcion': 'Esto es un Item de prueba',
                  'estado' : 'ACT',
                  'fecha_creacion': timezone.now(),
                  'fecha_modificacion': timezone.now(),
                  'tipoitem': tipoItem.id,
                  'complejidad': 10,
                  'costo': 10,
                  'tiempo': 10,
                  'version': 1,
                  'linea_base': '', }

        request = self.factory.post('/changeitem/', dato_item_mod)
        request.user = self.user
        response = changeItem(request, item.id)

        if response == None:
            print 'Error Previsto: La item especificado no existe\nPor favor verifique los datos ingresados'
        else:
            self.assertEqual(response.status_code, 302, 'Error al modificar el Item')

        print '\nItem modificado exitosamente'
        print ItemBase.objects.all()
        print 'Fin - Prueba: changeItem\n'
        print 'Inicio - Prueba: changeItem(ERROR PREVISTO)'
        id_item = 3
        response = changeItem(request, id_item)
        if response == None:
           print 'Error Previsto: El código de item ' + str(id_item)  + ' especificado no existe\nPor favor verifique los datos ingresados'
        print 'Fin - Prueba: changePhase(ERROR PREVISTO)\n'


class TestAdministrarItems_creacion(TestCase):
    """
    """

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

    def test_createItem_response(self):
        """
            *Test para la vista de creacion de proyectos en el sistema*
        """
        print '\nInicio - Prueba: Creacion de Item'
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        project = Proyecto.objects.get(nombre='Proyecto01')
        fase = Fase.objects.get(nombre='Fase01')
        fase.proyecto = project
        fase.save()
        tipoItem = TipoItem.objects.get(nombre='TipoItem01')

        dato_item_exito = {
                'usuario': self.user,
                'usuario_modificacion': self.user,
                'nombre': 'Item01',
                'descripcion': 'Esto es un Item de prueba',
                'estado' : 'ACT',
                'fecha_creacion': timezone.now(),
                'fecha_modificacion': timezone.now(),
                'tipoitem': tipoItem.id,
                'complejidad': 10,
                'costo': 10,
                'tiempo': 10,
                'version': 1,
                'linea_base': '', }

        print 'Prueba de Exitosa'
        request = self.factory.post('/createitem/', dato_item_exito)
        request.user = self.user
        response = createItem(request, fase.id)
        self.assertEqual(response.status_code, 302, 'Error al crear el Item')
        print ItemBase.objects.all()

        print '\nPrueba con Error Previsto'
        dato_item_falso = {
                'usuario': self.user,
                'usuario_modificacion': self.user,
                'nombre': 'Item01',
                'descripcion': 'Esto es un Item de prueba',
                'estado' : 'ACT',
                'fecha_creacion': timezone.now(),
                'fecha_modificacion': timezone.now(),
                'tipoitem': tipoItem,
                'complejidad': 10,
                'costo': 10,
                'tiempo': 10,
                'version': 1,
                'linea_base': '', }

        form = itemForm(dato_item_falso)
        try:
            form.save()
        except TypeError as e:
            print e
            print 'Error en el formulario, el campo tipo de item no recibe un dato válido'

        request = self.factory.post('/createitem/', dato_item_falso)
        request.user = self.user
        response = createItem(request, fase.id)
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200, 'Error en la creación de ítems, los datos ingresados en el formulario no son válidos')
            print 'Es posible establecer una conexión con la vista. \nPero no es posible crear el ítem, ya que existen campos inválidos en el formulario.'
        else:
            self.assertEqual(response.status_code, 302, 'Error en la creación de ítems, los datos ingresados en el formulario no son válidos')

        print 'Fin - Prueba: Creacion de Item\n'

