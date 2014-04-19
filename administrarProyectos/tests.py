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
    is_staff = False
    is_active = True
    date_joined = timezone.now()
    last_login = timezone.now()


class TestAdministrarProjectos(TestCase):
    """
    Test para Administración de usuarios, pruebas realizadas:
        + ChangeProject: Test de vista y modificación de los atributos de un proyecto en el sistema.
        + CreateProject: Test de Vista y creación de un nuevo proyecto en el sistema.
    """

    def setUp(self):
        """
        Crea el usuario 'admin' con contraseña 'admin' para las pruebas.
        """
        UsuarioFactory.create()
        self.factory = RequestFactory()

    def test_NewProjectForm_response(self):
        """
        Test para la vista de creación de proyectos en el sistema

        """
        print 'Inicio - Prueba 1: NewProjectForm'
        self.user = Usuario.objects.get(pk=1)
        print 'Usuario existente en la base de datos: ' + self.user.username
        dato = {'nombre': 'Proyecto1', 'lider_proyecto': '1', 'descripcion': 'Test:CreacionProyecto'}
        form = NewProjectForm(dato)
        if form.is_valid():
            form.save()
            print 'Proyecto '+form['nombre'].value()+' creado exitosamente en la Base de Datos'
        else:
            print 'Error en los datos del formulario de creación'

        project = Proyecto.objects.get(pk=1)
        self.assertEqual(project.nombre, 'Proyecto1', 'No coinciden los parámetros: Usuario no cargado exitosamente en la Base de datos')

        dato2 = {'nombre': 'Proyecto', 'lider_proyecto': '1', 'estado': 'PEN', 'descripcion': 'Test:ModificadoProyecto'}
        formulario = ChangeProjectForm(dato2, instance=project)
        if formulario.is_valid():
            formulario.save()
            print 'Proyecto '+formulario['nombre'].value()+' modificado exitosamente en la Base de Datos'
        else:
            print 'Error en los datos del formulario de modificación'

        project = Proyecto.objects.get(pk=1)
        print project.descripcion
        self.assertEqual(project.nombre, 'Proyecto', 'No coinciden los parámetros: Usuario no cargado exitosamente en la Base de datos')
        print 'Fin - Prueba 1: Exitosa'

    def test_createProject_response(self):
        print 'Inicio - Prueba 2: createProject'
        self.factory = RequestFactory()
        self.user = Usuario.objects.get()
        dato = {'nombre': 'Proyecto1', 'lider_proyecto': '1', 'descripcion': 'Test:CreacionProyecto'}
        request = self.factory.post('/proyecto/createproject', dato)
        request.user = self.user
        response = createProject(request)
        self.assertEqual(response.status_code, 200, 'Error al crear el Proyecto')
        print 'Fin - Prueba 2: Exitosa'
