#encoding:utf-8
from django.utils import timezone
from django.test import TestCase
from django.test.client import RequestFactory
from administrarUsuarios.forms import CustomUserCreationForm
from autenticacion.models import Usuario
from administrarUsuarios.views import changeUser, createUser, changePass
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


class TestAdministrarUsuarios(TestCase):
    """
    Test para Administración de usuarios, pruebas realizadas:
        + CustomUserCreationForm: Formulario para la creación de usuarios en el sistema
        + ChangePass: Prueba de vista y modificación de la contraseña del usuario actual.
        + ChangeUser: Prueba de vista y modificación de los atributos del usuario actual.
        + CreateUser: Prueba de Vista y creación de un nuevo usuario en el sistema.

    """
    un_admin = 'admin'
    pw_admin = 'admin'
    pw_new_admin = '123456'

    def setUp(self):
        """
            Crea el usuario 'admin' con contraseña 'admin'
        """
        UsuarioFactory.create()
        self.factory = RequestFactory()

    def test_CustomUserCreationForm_response(self):
        """
        Test para el formulario de  creación de usuarios en el sistema
        """
        print 'Inicio - Prueba 1: CustomUserCreationForm'
        self.user = Usuario.objects.get(pk=1)
        print 'Usuario existente en la base de datos: ' + self.user.username
        dato = {'username': 'test', 'password1': '123456', 'password2': '123456'}
        form = CustomUserCreationForm(dato)
        if form.is_valid():
            form.save()
            print 'Usuario '+form['username'].value()+' creado exitosamente en la Base de Datos'
        else:
            print 'Error en los datos del formulario'

        self.user = Usuario.objects.get(pk=2)
        self.assertEqual(self.user.username, 'test', 'No coinciden los parámetros: Usuario no cargado exitosamente en la Base de datos')
        print 'Fin - Prueba 1: Exitosa'

    def test_changeUser_response(self):
        """
        Test para la vista de modificación de usuarios en el sistema
        """
        print 'Inicio - Prueba 2: changeUser'
        self.factory = RequestFactory()
        self.user = Usuario.objects.get(pk=4)
        dato = {'first_name': 'Administrador', 'last_name': 'Test3', 'email': 'test3@zarpm.com', 'telefono': '3435365'}
        request = self.factory.post('usuario/changeuser/', dato)
        request.user = self.user
        response = changeUser(request)
        self.assertEqual(response.status_code, 302, 'Error al modificar el usuario')
        self.user = Usuario.objects.get(pk=4)
        usuario = Usuario.objects.get(first_name='Administrador')
        self.assertEqual(self.user, usuario, 'Los datos no coinciden: Usuario no modificado correctamente')
        print 'Fin - Prueba 2: Exitosa'

    def test_createUser_response(self):
        """
        Test para la vista de creación de usuarios en el sistema
        """
        print 'Inicio - Prueba 3: createUser'
        self.user = Usuario.objects.all()
        print self.user
        print 'usuarios'
        self.user = Usuario.objects.get()
        dato = {'username': 'test2', 'password1': '123456', 'password2': '123456'}
        request = self.factory.post('/createUser/', dato)
        request.user = self.user
        response = createUser(request)
        self.assertEqual(response.status_code, 302, 'Error al crear el Usuario')
        self.user = Usuario.objects.get(username='test2')
        self.assertEqual(self.user.username, 'test2', 'No coinciden los parámetros: Usuario no cargado exitosamente en la Base de datos')
        print 'Usuario '+self.user.username+' creado exitosamente en la Base de Datos'
        print 'Fin - Prueba 3: Exitosa'

    def test_changePass_response(self):
        """
        Test del Logeo del usuario 'admin' y posterior modificación de la contraseña.
        """
        print 'Inicio - Prueba 4: changePass'
        login = self.client.login(username=self.un_admin, password=self.pw_admin)
        self.assertTrue(login)
        self.factory = RequestFactory()
        self.user = Usuario.objects.get()
        dato = {'old_password': self.pw_admin, 'new_password1': self.pw_new_admin, 'new_password2': self.pw_new_admin}
        request = self.factory.post('usuario/changePass/', dato)
        request.user = self.user
        response = changePass(request)
        self.assertEqual(response.status_code, 302, 'Error al modificar la contraseña del usuario ')
        login = self.client.login(username=self.un_admin, password=self.pw_new_admin)
        self.assertTrue(login, 'Error al cambiar contraseña')
        print 'Fin - Prueba 4: Exitosa'
