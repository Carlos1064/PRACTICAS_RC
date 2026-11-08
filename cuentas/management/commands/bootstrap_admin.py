import os

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from cuentas.models import Usuario


class Command(BaseCommand):
    help = 'Crea una cuenta administradora inicial con variables de entorno.'

    def handle(self, *args, **options):
        correo = os.environ.get('BOOTSTRAP_ADMIN_EMAIL', '').strip().lower()
        nombre = os.environ.get('BOOTSTRAP_ADMIN_NAME', '').strip()
        password = os.environ.get('BOOTSTRAP_ADMIN_PASSWORD', '')
        valores = (correo, nombre, password)

        if not any(valores):
            tiene_admin_activo = Usuario.objects.filter(
                rol=Usuario.Rol.ADMINISTRADOR,
                is_active=True,
            ).exists()
            if os.environ.get('RENDER') and not tiene_admin_activo:
                raise CommandError(
                    'Define BOOTSTRAP_ADMIN_EMAIL, BOOTSTRAP_ADMIN_NAME y '
                    'BOOTSTRAP_ADMIN_PASSWORD en Render para crear el primer administrador.'
                )
            self.stdout.write('No se configuraron datos iniciales de administrador; no se realizaron cambios.')
            return

        if not all(valores):
            raise CommandError(
                'Configura juntos BOOTSTRAP_ADMIN_EMAIL, BOOTSTRAP_ADMIN_NAME y '
                'BOOTSTRAP_ADMIN_PASSWORD.'
            )

        existente = Usuario.objects.filter(correo__iexact=correo).first()
        if existente:
            if existente.rol != Usuario.Rol.ADMINISTRADOR:
                raise CommandError(
                    f'El correo {correo} ya existe con un rol distinto a administrador.'
                )
            self.stdout.write('La cuenta administradora ya existe; se conserva su contraseña.')
            return

        try:
            validate_password(password)
        except ValidationError as error:
            raise CommandError('La contraseña no cumple los requisitos: ' + ' '.join(error.messages)) from error
        Usuario.objects.create_superuser(
            correo=correo,
            nombre=nombre,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS('Cuenta administradora inicial creada.'))
