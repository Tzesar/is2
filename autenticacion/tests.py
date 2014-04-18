from django.test import TestCase
from django.utils import timezone
import factory
from autenticacion.models import Usuario


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


class TestAutenticacionViewsMyLogin(TestCase):
    """
        Prueba para la vista autenticacion.views.myLogin.
    """

    un_admin = 'xadmin'
    pw_admin = 'admin'

    un_unknown_user = 'cualquiera'
    pw_unknown_user = 'cualquiera'

    def setUp(self):
        """
            Crea el usuario 'admin' con contrasena 'admin'
        """
        UsuarioFactory.create()

    def test_login_response(self):
        """
            Prueba de la respuesta de la vista '/login/'
        """

        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_root_response(self):
        """
            Prueba de la respuesta de la vista '' root
        """

        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_login_admin(self):
        """
            Prueba del Logeo del usuario 'admin'
        """

        login = self.client.login(username=self.un_admin, password=self.pw_admin)
        self.assertTrue(login)

    def test_login_unknown_user(self):
        """
            Prueba del Logeo de un usuario no registrado
        """

        login = self.client.login(username=self.un_unknown_user, password=self.pw_unknown_user)
        self.assertFalse(login)