from django.db import models


class Empresa(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        APROBADA = 'aprobada', 'Aprobada'
        RECHAZADA = 'rechazada', 'Rechazada'

    usuario = models.OneToOneField(
        'cuentas.Usuario',
        on_delete=models.CASCADE,
        related_name='empresa',
        limit_choices_to={'rol': 'empresa'},
        verbose_name='usuario representante',
    )
    razon_social = models.CharField('razón social', max_length=180)
    nit = models.CharField('NIT', max_length=30, unique=True)
    sector = models.CharField('sector', max_length=100)
    ciudad = models.CharField('ciudad', max_length=100)
    descripcion = models.TextField('descripción')
    estado = models.CharField(
        'estado de aprobación', max_length=12,
        choices=Estado.choices, default=Estado.PENDIENTE,
    )
    creado_en = models.DateTimeField('creada el', auto_now_add=True)

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        ordering = ['razon_social']

    def __str__(self):
        return self.razon_social
