#encoding:utf-8
from django.utils import timezone
from django.test import TestCase
from django.test.client import RequestFactory
from administrarProyectos.models import Proyecto
from autenticacion.models import Usuario
from administrarProyectos.views import changeProject, createProject
from administrarProyectos.forms import NewProjectForm, ChangeProjectForm
import factory

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


class TestAdministrarProjectos(TestCase):
    """
    *Test para Administración de usuarios, pruebas realizadas:*
        + *ChangeProject*: Test de vista y modificación de los atributos de un proyecto en el sistema.
        + *CreateProject*: Test de Vista y creación de un nuevo proyecto en el sistema.
    """
    un_admin = 'admin'
    pw_admin = 'admin'

    def setUp(self):
        """
        *Crea el usuario 'admin' con contraseña 'admin' para las pruebas.*
        """
        UsuarioFactory.create()
        self.factory = RequestFactory()

    def test_createProject_response(self):
        """
        *Test para la vista de creacion de proyectos en el sistema*
        """
        print '\nInicio - Prueba: createProject'
        self.user = Usuario.objects.get(username='admin')
        dato = {'nombre': 'Proyecto1', 'lider_proyecto': '2', 'descripcion': 'Test:CreacionProyecto'}
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        request = self.factory.post('createproject/', dato)
        request.user = self.user
        response = createProject(request)
        self.assertEqual(response.status_code, 302, 'Error al crear el Proyecto')
        print 'Proyecto creado exitosamente'
        print Proyecto.objects.all()
        print 'Fin - Prueba: createProject\n'

    def test_changeProject_response(self):
        """
        *Test para la vista de modificacion de proyectos en el sistema*
        """
        print '\nInicio - Prueba: changeProject'
        self.user = Usuario.objects.get(username='admin')
        dato1 = {'nombre': 'Proyecto', 'lider_proyecto': '1', 'estado': 'PEN', 'descripcion': 'Test:CreadoProyecto'}
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        form = NewProjectForm(dato1)
        if form.is_valid():
            form.save()
            print 'Proyecto: '+form['nombre'].value()+' creado exitosamente en la Base de Datos'
        else:
            print 'Error en los datos del formulario de creación'
        dato2 = {'nombre': 'ProyectoModificado', 'lider_proyecto': '1', 'estado': 'PEN', 'descripcion': 'Test:ModificadoProyecto'}
        request = self.factory.post('changeproject/', dato2)
        request.user = self.user
        response = changeProject(request, '1')
        self.assertEqual(response.status_code, 302, 'Error al modificar el Proyecto')
        print 'Proyecto Modificado Exitosamente'
        print Proyecto.objects.all()
        print 'Fin - Prueba: changeProject'