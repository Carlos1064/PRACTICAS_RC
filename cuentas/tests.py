from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from cuentas.models import Empresa, PerfilEstudiante


Usuario = get_user_model()


class RegistroAutenticacionTests(TestCase):
    def test_inicio_de_sesion_invalido_no_autentica(self):
        response = self.client.post(reverse('cuentas:ingresar'), {
            'username': 'inexistente@example.test', 'password': 'incorrecta',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'no son correctos')

    def test_registro_estudiante_crea_cuenta_y_perfil(self):
        response = self.client.post(reverse('cuentas:registro_estudiante'), {
            'nombre': 'Estudiante Nuevo', 'correo': 'nuevo@example.test',
            'programa': 'Ingeniería de Sistemas', 'semestre': '6', 'ciudad': 'Bogotá',
            'password1': 'ClaveFuerte#924', 'password2': 'ClaveFuerte#924',
        })
        usuario = Usuario.objects.get(correo='nuevo@example.test')
        self.assertRedirects(response, reverse('cuentas:ingresar'))
        self.assertEqual(usuario.rol, Usuario.Rol.ESTUDIANTE)
        self.assertTrue(usuario.check_password('ClaveFuerte#924'))
        self.assertEqual(PerfilEstudiante.objects.get(usuario=usuario).programa, 'Ingeniería de Sistemas')

    def test_registro_empresa_queda_pendiente(self):
        response = self.client.post(reverse('cuentas:registro_empresa'), {
            'nombre': 'Representante Nuevo', 'correo': 'empresa@example.test',
            'razon_social': 'Empresa Nueva S.A.S.', 'nit': '900555444-1',
            'sector': 'Tecnología', 'ciudad': 'Bogotá', 'descripcion': 'Empresa de prueba.',
            'password1': 'ClaveFuerte#924', 'password2': 'ClaveFuerte#924',
        })
        empresa = Empresa.objects.get(nit='900555444-1')
        self.assertRedirects(response, reverse('cuentas:ingresar'))
        self.assertEqual(empresa.estado, Empresa.Estado.PENDIENTE)

    def test_estudiante_no_accede_a_gestion_de_categorias(self):
        estudiante = Usuario.objects.create_user(
            correo='estudiante@example.test', password='ClaveFuerte#924',
            nombre='Estudiante', rol=Usuario.Rol.ESTUDIANTE,
        )
        self.client.force_login(estudiante)
        response = self.client.get(reverse('ofertas:categorias'))
        self.assertEqual(response.status_code, 403)

    def test_administrador_aprueba_empresa_pendiente(self):
        admin = Usuario.objects.create_user(
            correo='admin@example.test', password='ClaveFuerte#924',
            nombre='Administración', rol=Usuario.Rol.ADMINISTRADOR,
        )
        representante = Usuario.objects.create_user(
            correo='rep@example.test', password='ClaveFuerte#924',
            nombre='Representante', rol=Usuario.Rol.EMPRESA,
        )
        empresa = Empresa.objects.create(
            usuario=representante, razon_social='Pendiente S.A.S.', nit='900555444-2',
            sector='Tecnología', ciudad='Cali', descripcion='Solicitud pendiente.',
        )
        self.client.force_login(admin)
        response = self.client.post(reverse('cuentas_admin:empresa_decision', args=[empresa.pk]), {'decision': 'aprobar'})
        empresa.refresh_from_db()
        self.assertRedirects(response, reverse('cuentas_admin:empresas_pendientes'))
        self.assertEqual(empresa.estado, Empresa.Estado.APROBADA)


@override_settings(DEBUG=False, ROOT_URLCONF='config.test_urls')
class PaginasDeErrorTests(TestCase):
    def test_404_muestra_pagina_personalizada_sin_traceback(self):
        response = self.client.get('/ruta-que-no-existe/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'No encontramos esta página', status_code=404)
        self.assertNotContains(response, 'Traceback', status_code=404)

    def test_500_muestra_pagina_personalizada_sin_detalle_interno(self):
        cliente = Client(raise_request_exception=False)
        response = cliente.get('/_prueba/error-500/')
        self.assertEqual(response.status_code, 500)
        self.assertContains(response, 'Tuvimos un problema', status_code=500)
        self.assertNotContains(response, 'Este detalle interno', status_code=500)
        self.assertNotContains(response, 'Traceback', status_code=500)

    def test_403_muestra_pagina_personalizada(self):
        usuario = Usuario.objects.create_user(
            correo='estudiante403@example.test', password='ClaveFuerte#924',
            nombre='Estudiante', rol=Usuario.Rol.ESTUDIANTE,
        )
        self.client.force_login(usuario)
        response = self.client.get(reverse('ofertas:categorias'))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'No tienes permiso', status_code=403)
    def test_formulario_estudiante_vacio_muestra_errores_del_servidor(self):
        response = self.client.post(reverse('cuentas:registro_estudiante'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(Usuario.objects.filter(correo='').exists())

    def test_ingreso_vacio_muestra_errores_del_servidor(self):
        response = self.client.post(reverse('cuentas:ingresar'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
    def test_registro_empresa_vacio_muestra_errores_del_servidor(self):
        response = self.client.post(reverse('cuentas:registro_empresa'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_edicion_de_perfil_estudiante_vacia_muestra_errores(self):
        usuario = Usuario.objects.create_user(
            correo='perfil-estudiante@example.test', password='ClaveFuerte#924',
            nombre='Perfil Estudiante', rol=Usuario.Rol.ESTUDIANTE,
        )
        PerfilEstudiante.objects.create(usuario=usuario, programa='Sistemas', ciudad='Bogotá')
        self.client.force_login(usuario)
        response = self.client.post(reverse('cuentas:perfil_editar'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_edicion_de_perfil_empresa_vacia_muestra_errores(self):
        usuario = Usuario.objects.create_user(
            correo='perfil-empresa@example.test', password='ClaveFuerte#924',
            nombre='Representante', rol=Usuario.Rol.EMPRESA,
        )
        Empresa.objects.create(
            usuario=usuario, razon_social='Perfil S.A.S.', nit='900555444-3',
            sector='Tecnología', ciudad='Bogotá', descripcion='Descripción existente.',
        )
        self.client.force_login(usuario)
        response = self.client.post(reverse('cuentas:perfil_editar'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
