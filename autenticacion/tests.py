from django.test import TestCase


class TestAutenticacionViewsMyLogin(TestCase):
    """
        Prueba para la vista autenticacion.views.myLogin.
    """
    def test_login(self):
        """
            La pagina '/login/' se devuelve correctamente.
        """
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context)
