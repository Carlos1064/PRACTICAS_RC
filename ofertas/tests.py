from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.models import Empresa, Usuario
from ofertas.forms import OfertaForm
from ofertas.models import Categoria, Oferta


class FlujosDeOfertaTests(TestCase):
    def setUp(self):
        self.usuario_empresa = Usuario.objects.create_user(
            correo='empresa@example.test', password='ClaveFuerte#924',
            nombre='Representante', rol=Usuario.Rol.EMPRESA,
        )
        self.empresa = Empresa.objects.create(
            usuario=self.usuario_empresa, razon_social='Empresa Uno S.A.S.', nit='900100100-1',
            sector='Tecnología', ciudad='Bogotá', descripcion='Empresa de prueba.',
            estado=Empresa.Estado.APROBADA,
        )
        self.categoria = Categoria.objects.create(nombre='Desarrollo')
        self.admin = Usuario.objects.create_user(
            correo='admin@example.test', password='ClaveFuerte#924',
            nombre='Administración', rol=Usuario.Rol.ADMINISTRADOR,
        )

    def crear_oferta(self, titulo, *, dias=30, empresa=None):
        return Oferta.objects.create(
            empresa=empresa or self.empresa, categoria=self.categoria, titulo=titulo,
            descripcion='Descripción de la oportunidad.', requisitos='Experiencia relacionada.',
            tipo=Oferta.Tipo.PRACTICA, modalidad=Oferta.Modalidad.HIBRIDA,
            vacantes=1, fecha_limite=timezone.localdate() + timedelta(days=dias),
            estado=Oferta.Estado.PUBLICADA,
        )

    def test_fecha_limite_pasada_es_rechazada_por_formulario(self):
        formulario = OfertaForm(data={
            'categoria': self.categoria.pk, 'titulo': 'Oferta vencida',
            'descripcion': 'Descripción suficiente.', 'requisitos': 'Requisitos suficientes.',
            'tipo': Oferta.Tipo.PRACTICA, 'modalidad': Oferta.Modalidad.REMOTA,
            'vacantes': 1, 'fecha_limite': (timezone.localdate() - timedelta(days=1)).isoformat(),
        })
        self.assertFalse(formulario.is_valid())
        self.assertIn('fecha_limite', formulario.errors)

    def test_empresa_aprobada_crea_oferta_pendiente(self):
        self.client.force_login(self.usuario_empresa)
        response = self.client.post(reverse('ofertas:crear'), {
            'categoria': self.categoria.pk, 'titulo': 'Nueva oportunidad',
            'descripcion': 'Descripción de la oportunidad.', 'requisitos': 'Requisitos mínimos.',
            'tipo': Oferta.Tipo.PRACTICA, 'modalidad': Oferta.Modalidad.HIBRIDA,
            'vacantes': 2, 'fecha_limite': (timezone.localdate() + timedelta(days=20)).isoformat(),
        })
        oferta = Oferta.objects.get(titulo='Nueva oportunidad')
        self.assertRedirects(response, reverse('ofertas:mis_ofertas'))
        self.assertEqual(oferta.estado, Oferta.Estado.PENDIENTE)
        self.assertEqual(oferta.empresa, self.empresa)

    def test_oferta_pendiente_se_publica_solo_por_aprobacion_admin(self):
        oferta = self.crear_oferta('Pendiente para aprobación')
        oferta.estado = Oferta.Estado.PENDIENTE
        oferta.save(update_fields=['estado'])
        self.client.force_login(self.admin)
        response = self.client.post(reverse('ofertas:decision', args=[oferta.pk]), {'decision': 'aprobar'})
        oferta.refresh_from_db()
        self.assertRedirects(response, reverse('ofertas:pendientes'))
        self.assertEqual(oferta.estado, Oferta.Estado.PUBLICADA)

    def test_ajax_filtra_y_devuelve_solo_el_parcial(self):
        visible = self.crear_oferta('Práctica visible para filtro')
        response = self.client.get(
            reverse('ofertas:lista'), {'q': 'visible'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        contenido = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn(visible.titulo, contenido)
        self.assertNotIn('<html', contenido)

    def test_paginacion_limita_el_numero_de_ofertas(self):
        for indice in range(11):
            self.crear_oferta(f'Oferta paginada {indice}')
        response = self.client.get(reverse('ofertas:lista'))
        self.assertEqual(response.context['page_obj'].paginator.count, 11)
        self.assertEqual(len(response.context['ofertas']), 9)

    def test_empresa_pendiente_no_puede_crear_ofertas(self):
        self.empresa.estado = Empresa.Estado.PENDIENTE
        self.empresa.save(update_fields=['estado'])
        self.client.force_login(self.usuario_empresa)
        response = self.client.post(reverse('ofertas:crear'), {})
        self.assertRedirects(response, reverse('ofertas:mis_ofertas'))
        self.assertFalse(Oferta.objects.filter(empresa=self.empresa, estado=Oferta.Estado.PENDIENTE).exists())

    def test_empresa_ajena_recibe_403_al_editar_o_cerrar(self):
        otra_cuenta = Usuario.objects.create_user(
            correo='otra@example.test', password='ClaveFuerte#924',
            nombre='Otra empresa', rol=Usuario.Rol.EMPRESA,
        )
        otra_empresa = Empresa.objects.create(
            usuario=otra_cuenta, razon_social='Otra S.A.S.', nit='900100100-2',
            sector='Tecnología', ciudad='Cali', descripcion='Otra empresa.',
            estado=Empresa.Estado.APROBADA,
        )
        oferta = self.crear_oferta('Oferta de la primera empresa', empresa=self.empresa)
        self.client.force_login(otra_cuenta)
        edicion = self.client.get(reverse('ofertas:editar', args=[oferta.pk]))
        cierre = self.client.post(reverse('ofertas:cerrar', args=[oferta.pk]))
        self.assertEqual(edicion.status_code, 403)
        self.assertEqual(cierre.status_code, 403)

    def test_formulario_de_oferta_vacio_muestra_errores_del_servidor(self):
        self.client.force_login(self.usuario_empresa)
        response = self.client.post(reverse('ofertas:crear'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_edicion_de_oferta_vacia_muestra_errores_del_servidor(self):
        oferta = self.crear_oferta('Oferta para editar')
        self.client.force_login(self.usuario_empresa)
        response = self.client.post(reverse('ofertas:editar', args=[oferta.pk]), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_categoria_vacia_muestra_errores_del_servidor(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('ofertas:categoria_crear'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
