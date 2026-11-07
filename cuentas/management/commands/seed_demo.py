from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from cuentas.models import Empresa, PerfilEstudiante, Usuario
from ofertas.models import Categoria, Oferta


class Command(BaseCommand):
    help = 'Crea o actualiza datos de demostración para el desarrollo local.'

    def handle(self, *args, **options):
        clave = 'PracticasDemo2026!'
        estudiante = self.usuario_demo(
            'estudiante@demo.local', 'Estudiante Demo', Usuario.Rol.ESTUDIANTE, clave,
        )
        PerfilEstudiante.objects.update_or_create(
            usuario=estudiante,
            defaults={
                'programa': 'Ingeniería de Sistemas',
                'semestre': 8,
                'ciudad': 'Bogotá',
                'habilidades': 'Python, Django, SQL, trabajo en equipo',
                'resumen': 'Estudiante interesado en desarrollo de software.',
            },
        )

        administrador = self.usuario_demo(
            'admin@demo.local', 'Administración Demo',
            Usuario.Rol.ADMINISTRADOR, clave,
            is_staff=True, is_superuser=True,
        )
        empresas = []
        for numero, nombre, ciudad in [
            (1, 'Nube Andina S.A.S.', 'Bogotá'),
            (2, 'Soluciones del Valle S.A.S.', 'Cali'),
        ]:
            usuario_empresa = self.usuario_demo(
                f'empresa{numero}@demo.local', f'Representante Empresa {numero}',
                Usuario.Rol.EMPRESA, clave,
            )
            empresa, _ = Empresa.objects.update_or_create(
                usuario=usuario_empresa,
                defaults={
                    'razon_social': nombre,
                    'nit': f'90012345{numero}-{numero}',
                    'sector': 'Tecnología',
                    'ciudad': ciudad,
                    'descripcion': f'Empresa de demostración del sector tecnológico en {ciudad}.',
                    'estado': Empresa.Estado.APROBADA,
                },
            )
            empresas.append(empresa)

        categorias_nombres = [
            'Desarrollo de software', 'Datos y analítica', 'Diseño y experiencia de usuario',
            'Infraestructura y nube', 'Gestión de proyectos',
        ]
        categorias = [
            Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': f'Oportunidades relacionadas con {nombre.lower()}.'},
            )[0]
            for nombre in categorias_nombres
        ]

        titulos = [
            'Desarrollador(a) Python', 'Analista de datos', 'Diseñador(a) UX/UI',
            'Asistente de infraestructura cloud', 'Auxiliar de proyectos tecnológicos',
            'Practicante de desarrollo web', 'Ingeniero(a) de automatización',
            'Analista QA', 'Desarrollador(a) frontend', 'Desarrollador(a) backend',
        ]
        hoy = timezone.localdate()
        for indice in range(30):
            empresa = empresas[indice % len(empresas)]
            titulo = f'{titulos[indice % len(titulos)]} {indice + 1:02d}'
            Oferta.objects.update_or_create(
                empresa=empresa,
                titulo=titulo,
                defaults={
                    'categoria': categorias[indice % len(categorias)],
                    'descripcion': (
                        f'Buscamos talento para apoyar proyectos de {categorias[indice % len(categorias)].nombre.lower()}. '
                        'La persona seleccionada colaborará con un equipo interdisciplinario.'
                    ),
                    'requisitos': 'Formación relacionada, comunicación efectiva e interés por aprender.',
                    'tipo': Oferta.Tipo.PRACTICA if indice % 3 else Oferta.Tipo.EMPLEO,
                    'modalidad': list(Oferta.Modalidad.values)[indice % len(Oferta.Modalidad.values)],
                    'vacantes': (indice % 4) + 1,
                    'fecha_limite': hoy + timedelta(days=15 + (indice % 45)),
                    'estado': Oferta.Estado.PUBLICADA,
                },
            )

        Oferta.objects.update_or_create(
            empresa=empresas[0],
            titulo='Practicante de soporte TI (pendiente)',
            defaults={
                'categoria': categorias[3],
                'descripcion': 'Oferta de demostración pendiente de revisión administrativa.',
                'requisitos': 'Conocimientos básicos de soporte técnico.',
                'tipo': Oferta.Tipo.PRACTICA,
                'modalidad': Oferta.Modalidad.PRESENCIAL,
                'vacantes': 1,
                'fecha_limite': hoy + timedelta(days=30),
                'estado': Oferta.Estado.PENDIENTE,
            },
        )

        self.stdout.write(self.style.SUCCESS(
            'Seed listo: 4 usuarios, 2 empresas, 5 categorías, '
            '30 ofertas publicadas y 1 oferta pendiente.'
        ))
        self.stdout.write('Cuentas demo: estudiante@demo.local, empresa1@demo.local, empresa2@demo.local y admin@demo.local')
        self.stdout.write('Contraseña local compartida: PracticasDemo2026!')
        self.stdout.write('No uses estas credenciales en producción.')

    @staticmethod
    def usuario_demo(correo, nombre, rol, clave, **flags):
        usuario, _ = Usuario.objects.get_or_create(
            correo=correo,
            defaults={'nombre': nombre, 'rol': rol, **flags},
        )
        usuario.nombre = nombre
        usuario.rol = rol
        usuario.is_active = True
        for campo in ('is_staff', 'is_superuser'):
            if campo in flags:
                setattr(usuario, campo, flags[campo])
        usuario.set_password(clave)
        usuario.save()
        return usuario
