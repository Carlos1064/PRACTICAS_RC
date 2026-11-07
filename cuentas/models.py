from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio.')
        correo = self.normalize_email(correo).strip().lower()
        usuario = self.model(correo=correo, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('rol', Usuario.Rol.ADMINISTRADOR)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('rol') != Usuario.Rol.ADMINISTRADOR:
            raise ValueError('El superusuario debe tener el rol administrador.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        ESTUDIANTE = 'estudiante', 'Estudiante'
        EMPRESA = 'empresa', 'Empresa'
        ADMINISTRADOR = 'administrador', 'Administrador'

    nombre = models.CharField('nombre completo', max_length=150)
    correo = models.EmailField('correo electrónico', unique=True)
    rol = models.CharField('rol', max_length=20, choices=Rol.choices)
    is_active = models.BooleanField('activo', default=True)
    is_staff = models.BooleanField('acceso al sitio administrativo', default=False)
    creado_en = models.DateTimeField('creado el', auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['nombre', 'correo']

    def __str__(self):
        return f'{self.nombre} <{self.correo}>'


class PerfilEstudiante(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_estudiante',
        limit_choices_to={'rol': Usuario.Rol.ESTUDIANTE},
        verbose_name='usuario',
    )
    programa = models.CharField('programa académico', max_length=150)
    semestre = models.PositiveSmallIntegerField('semestre', null=True, blank=True)
    ciudad = models.CharField('ciudad', max_length=100)
    habilidades = models.TextField('habilidades', blank=True)
    resumen = models.TextField('perfil profesional', blank=True)
    cv_url = models.URLField('enlace a la hoja de vida', blank=True)

    class Meta:
        verbose_name = 'perfil de estudiante'
        verbose_name_plural = 'perfiles de estudiantes'
        ordering = ['usuario__nombre']

    def __str__(self):
        return f'Perfil de {self.usuario.nombre}'


from .models_empresa import Empresa  # noqa: E402,F401
