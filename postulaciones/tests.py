from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cuentas.models import Empresa, PerfilEstudiante, Usuario
from ofertas.models import Categoria, Oferta
from .models import Postulacion


class FlujosDePostulacionTests(TestCase):
    def setUp(self):
        self.estudiante = Usuario.objects.create_user(
            correo='estudiante@example.test', password='ClaveFuerte#924',
            nombre='Estudiante Uno', rol=Usuario.Rol.ESTUDIANTE,
        )
        PerfilEstudiante.objects.create(
            usuario=self.estudiante, programa='Ingeniería de Sistemas',
            semestre=8, ciudad='Bogotá', habilidades='Python',
        )
        self.usuario_empresa = Usuario.objects.create_user(
            correo='empresa@example.test', password='ClaveFuerte#924',
            nombre='Representante', rol=Usuario.Rol.EMPRESA,
        )
        self.empresa = Empresa.objects.create(
            usuario=self.usuario_empresa, razon_social='Empresa Uno S.A.S.', nit='900200200-1',
            sector='Tecnología', ciudad='Bogotá', descripcion='Empresa de prueba.',
            estado=Empresa.Estado.APROBADA,
        )
        self.usuario_ajeno = Usuario.objects.create_user(
            correo='otra-empresa@example.test', password='ClaveFuerte#924',
            nombre='Otra representante', rol=Usuario.Rol.EMPRESA,
        )
        self.empresa_ajena = Empresa.objects.create(
            usuario=self.usuario_ajeno, razon_social='Empresa Dos S.A.S.', nit='900200200-2',
            sector='Tecnología', ciudad='Cali', descripcion='Otra empresa de prueba.',
            estado=Empresa.Estado.APROBADA,
        )
        self.categoria = Categoria.objects.create(nombre='Analítica')
        self.oferta = self.crear_oferta('Analista de datos')

    def crear_oferta(self, titulo, *, dias=30, estado=Oferta.Estado.PUBLICADA, empresa=None):
        return Oferta.objects.create(
            empresa=empresa or self.empresa, categoria=self.categoria, titulo=titulo,
            descripcion='Oportunidad de demostración.', requisitos='Manejo de datos.',
            tipo=Oferta.Tipo.EMPLEO, modalidad=Oferta.Modalidad.REMOTA,
            vacantes=1, fecha_limite=timezone.localdate() + timedelta(days=dias), estado=estado,
        )

    def test_estudiante_se_postula_y_el_registro_persiste(self):
        self.client.force_login(self.estudiante)
        response = self.client.post(reverse('postulaciones:crear', args=[self.oferta.pk]), {'mensaje': 'Me interesa.'})
        self.assertRedirects(response, reverse('postulaciones:mis_postulaciones'))
        self.assertTrue(Postulacion.objects.filter(oferta=self.oferta, estudiante=self.estudiante).exists())

    def test_no_se_permite_una_postulacion_duplicada(self):
        self.client.force_login(self.estudiante)
        url = reverse('postulaciones:crear', args=[self.oferta.pk])
        self.client.post(url, {'mensaje': 'Primera postulación.'})
        response = self.client.post(url, {'mensaje': 'Intento duplicado.'})
        self.assertEqual(Postulacion.objects.filter(oferta=self.oferta, estudiante=self.estudiante).count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_no_se_aceptan_ofertas_cerradas_ni_vencidas(self):
        self.client.force_login(self.estudiante)
        cerrada = self.crear_oferta('Oferta cerrada', estado=Oferta.Estado.CERRADA)
        vencida = self.crear_oferta('Oferta vencida', dias=-1)
        for oferta in (cerrada, vencida):
            response = self.client.post(reverse('postulaciones:crear', args=[oferta.pk]), {'mensaje': ''})
            self.assertEqual(response.status_code, 302)
            self.assertFalse(Postulacion.objects.filter(oferta=oferta, estudiante=self.estudiante).exists())

    def test_estudiante_revisa_y_retira_su_postulacion(self):
        postulacion = Postulacion.objects.create(oferta=self.oferta, estudiante=self.estudiante)
        self.client.force_login(self.estudiante)
        response = self.client.post(reverse('postulaciones:retirar', args=[postulacion.pk]))
        postulacion.refresh_from_db()
        self.assertRedirects(response, reverse('postulaciones:mis_postulaciones'))
        self.assertEqual(postulacion.estado, Postulacion.Estado.RETIRADA)

    def test_empresa_ajena_recibe_403_en_lista_y_perfil(self):
        postulacion = Postulacion.objects.create(oferta=self.oferta, estudiante=self.estudiante)
        self.client.force_login(self.usuario_ajeno)
        response_lista = self.client.get(reverse('postulaciones:postulantes', args=[self.oferta.pk]))
        response_perfil = self.client.get(reverse('postulaciones:detalle_candidato', args=[postulacion.pk]))
        self.assertEqual(response_lista.status_code, 403)
        self.assertEqual(response_perfil.status_code, 403)

    def test_empresa_propietaria_cambia_estado_con_transicion_valida(self):
        postulacion = Postulacion.objects.create(oferta=self.oferta, estudiante=self.estudiante)
        self.client.force_login(self.usuario_empresa)
        response = self.client.post(
            reverse('postulaciones:cambiar_estado', args=[postulacion.pk]),
            {'estado': Postulacion.Estado.EN_REVISION},
        )
        postulacion.refresh_from_db()
        self.assertRedirects(response, reverse('postulaciones:postulantes', args=[self.oferta.pk]))
        self.assertEqual(postulacion.estado, Postulacion.Estado.EN_REVISION)

    def test_transicion_no_permitida_no_cambia_el_estado(self):
        postulacion = Postulacion.objects.create(oferta=self.oferta, estudiante=self.estudiante)
        self.client.force_login(self.usuario_empresa)
        self.client.post(
            reverse('postulaciones:cambiar_estado', args=[postulacion.pk]),
            {'estado': Postulacion.Estado.CONTRATADO},
        )
        postulacion.refresh_from_db()
        self.assertEqual(postulacion.estado, Postulacion.Estado.ENVIADA)

    def test_empresa_no_aprobada_no_acepta_postulaciones(self):
        self.empresa.estado = Empresa.Estado.PENDIENTE
        self.empresa.save(update_fields=['estado'])
        self.client.force_login(self.estudiante)
        self.client.post(reverse('postulaciones:crear', args=[self.oferta.pk]), {'mensaje': ''})
        self.assertFalse(Postulacion.objects.filter(oferta=self.oferta, estudiante=self.estudiante).exists())

    def test_empresa_propietaria_puede_ver_perfil_del_postulante(self):
        postulacion = Postulacion.objects.create(oferta=self.oferta, estudiante=self.estudiante)
        self.client.force_login(self.usuario_empresa)
        response = self.client.get(reverse('postulaciones:detalle_candidato', args=[postulacion.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ingeniería de Sistemas')

    def test_cambio_de_estado_vacio_se_rechaza(self):
        postulacion = Postulacion.objects.create(oferta=self.oferta, estudiante=self.estudiante)
        self.client.force_login(self.usuario_empresa)
        response = self.client.post(reverse('postulaciones:cambiar_estado', args=[postulacion.pk]), {})
        self.assertRedirects(response, reverse('postulaciones:postulantes', args=[self.oferta.pk]))
        postulacion.refresh_from_db()
        self.assertEqual(postulacion.estado, Postulacion.Estado.ENVIADA)
