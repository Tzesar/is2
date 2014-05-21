#encoding:utf-8
from django.utils import timezone
from django.test import TestCase
from django.test.client import RequestFactory
import factory

from administrarProyectos.models import Proyecto
from autenticacion.models import Usuario
from administrarFases.views import createPhase, changePhase, deletePhase
from administrarFases.models import Fase


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

    nombre = 'Proyecto de Prueba'
    lider_proyecto = Usuario.objects.get(pk='1')
    descripcion = 'Proyecto de Prueba para los Test'
    fecha_inicio = timezone.now()
    fecha_fin = timezone.now()
    estado = 'PEN'
    observaciones = 'Esto es una prueba'


class TestAdministrarFases(TestCase):
    """
    *Test para Administración de usuarios, pruebas realizadas:*
        + *ChangePhase*: Test de vista y modificación de los atributos de una fase en el sistema.
        + *CreatePhase*: Test de Vista y creación de una nueva fase en el sistema.
        + *DeletePhase*: Test de vista y eliminación de una fase en el sistema
    """

    def setUp(self):
        """
        *Crea el usuario 'admin' con contraseña 'admin' para las pruebas.*
        """
        UsuarioFactory.create()
        self.user = Usuario.objects.get(username='admin')
        ProyectoFactory.lider_proyecto = self.user
        ProyectoFactory.create()
        self.factory = RequestFactory()

    def test_createPhase_response(self):
        """
        *Test para la vista de creacion de proyectos en el sistema*
        """
        print '\nInicio - Prueba: createPhase'
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        project = Proyecto.objects.get(nombre='Proyecto de Prueba')
        dato_fase = {'nombre': 'Fase_Prueba', 'descripcion': 'Fase Test'}
        request = self.factory.post('/createphase/', dato_fase)
        request.user =self.user
        response = createPhase(request, project.id)
        self.assertEqual(response.status_code, 302, 'Error al crear la Fase')
        print 'Fase creada exitosamente'
        print Fase.objects.all()
        print 'Fin - Prueba: createPhase\n'

    def test_changePhase_response(self):
        """
        *Test para la vista de modificacion de fases en el sistema.*
        """
        print '\nInicio - Prueba: changePhase'
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        project = Proyecto.objects.get(nombre='Proyecto de Prueba')
        dato_fase = {'nombre': 'Fase_Prueba', 'descripcion': 'Fase Test'}
        request = self.factory.post('/createphase/', dato_fase)
        request.user = self.user
        response = createPhase(request, project.id )
        self.assertEqual(response.status_code, 302, 'Error al crear la Fase')
        print Fase.objects.all()

        phase = Fase.objects.get(nombre='Fase_Prueba')
        dato_fase_mod = {'nombre': 'Fase_Prueba_modificado', 'estado': 'PEN', 'descripcion': 'Fase Test'}
        request = self.factory.post('/changephase/', dato_fase_mod)
        request.user = self.user
        response = changePhase(request, phase.id)

        if response == None:
            print 'Error Previsto: La fase especificada no existe\nPor favor verifique los datos ingresados'
        else:
            self.assertEqual(response.status_code, 302, 'Error al modificar la Fase')

        print 'Fase modificada exitosamente'
        print Fase.objects.all()
        print 'Fin - Prueba: changePhase\n'

        print 'Inicio - Prueba: changePhase(ERROR PREVISTO)'
        response = changePhase(request, 3)

        if response == None:
            print 'Error Previsto: La fase especificada no existe\nPor favor verifique los datos ingresados'

        print 'Fin - Prueba: changePhase(ERROR PREVISTO)\n'



    def test_deletePhase_response(self):
        """
        *Test para la vista de eliminacion de una fase en el sistema.*
        """
        print '\nInicio - Prueba: deletePhase'
        project = Proyecto.objects.get(nombre='Proyecto de Prueba')
        dato_fase = {'nombre': 'Fase_Prueba', 'descripcion': 'Fase Test'}
        request = self.factory.post('/createphase/', dato_fase)
        request.user = self.user
        response = createPhase(request, project.id )
        self.assertEqual(response.status_code, 302, 'Error al crear la Fase')
        print Fase.objects.all()

        phase = Fase.objects.get(nombre='Fase_Prueba')
        dato_fase_mod = {'nombre': 'Fase_Prueba_modificado', 'estado': 'PEN', 'descripcion': 'Fase Test'}
        request = self.factory.post('/deletephase/', dato_fase_mod)
        request.user = self.user
        response = deletePhase(request, phase.id)
        self.assertEqual(response.status_code, 302, 'Error Previsto: Error al eiminar la Fase')
        print 'Fase Eliminada exitosamente'
        print Fase.objects.all()
        print 'Fin - Prueba: deletePhase\n'
