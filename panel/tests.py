from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.models import Empresa, PerfilEstudiante, Usuario
from ofertas.models import Categoria, Oferta
from postulaciones.models import Postulacion


class ReporteCSVTests(TestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user(
            correo='admin@example.test', password='ClaveFuerte#924',
            nombre='Administración', rol=Usuario.Rol.ADMINISTRADOR,
        )
        estudiante = Usuario.objects.create_user(
            correo='estudiante@example.test', password='ClaveFuerte#924',
            nombre='Estudiante CSV', rol=Usuario.Rol.ESTUDIANTE,
        )
        PerfilEstudiante.objects.create(usuario=estudiante, programa='Ingeniería', ciudad='Bogotá')
        empresa_usuario = Usuario.objects.create_user(
            correo='empresa@example.test', password='ClaveFuerte#924',
            nombre='Representante', rol=Usuario.Rol.EMPRESA,
        )
        empresa = Empresa.objects.create(
            usuario=empresa_usuario, razon_social='Empresa CSV S.A.S.', nit='900300300-1',
            sector='Tecnología', ciudad='Bogotá', descripcion='Empresa de reporte.',
            estado=Empresa.Estado.APROBADA,
        )
        categoria = Categoria.objects.create(nombre='Ciencia de datos')
        oferta = Oferta.objects.create(
            empresa=empresa, categoria=categoria, titulo='Analista CSV',
            descripcion='Oferta de reporte.', requisitos='Python.', tipo=Oferta.Tipo.EMPLEO,
            modalidad=Oferta.Modalidad.REMOTA, vacantes=1,
            fecha_limite=timezone.localdate() + timedelta(days=30), estado=Oferta.Estado.PUBLICADA,
        )
        Postulacion.objects.create(oferta=oferta, estudiante=estudiante, estado=Postulacion.Estado.CONTRATADO)
        self.categoria = categoria

    def test_exporta_csv_utf8_para_excel_con_datos_de_bd(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('panel:reporte_csv'))
        contenido = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
        self.assertTrue(contenido.startswith('\ufeff'))
        self.assertIn('Estudiante CSV', contenido)
        self.assertIn('Analista CSV', contenido)
        self.assertIn('Contratado', contenido)

    def test_reporte_filtra_por_categoria_y_periodo(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('panel:reporte'), {
            'categoria': self.categoria.pk,
            'desde': (timezone.localdate() - timedelta(days=1)).isoformat(),
            'hasta': (timezone.localdate() + timedelta(days=1)).isoformat(),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
