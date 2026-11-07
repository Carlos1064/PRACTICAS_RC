from django.db import models


class Postulacion(models.Model):
    class Estado(models.TextChoices):
        ENVIADA = 'enviada', 'Enviada'
        EN_REVISION = 'en_revision', 'En revisión'
        PRESELECCIONADO = 'preseleccionado', 'Preseleccionado'
        RECHAZADO = 'rechazado', 'Rechazado'
        CONTRATADO = 'contratado', 'Contratado'
        RETIRADA = 'retirada', 'Retirada'

    oferta = models.ForeignKey(
        'ofertas.Oferta', on_delete=models.CASCADE,
        related_name='postulaciones', verbose_name='oferta',
    )
    estudiante = models.ForeignKey(
        'cuentas.Usuario', on_delete=models.CASCADE,
        related_name='postulaciones', limit_choices_to={'rol': 'estudiante'},
        verbose_name='estudiante',
    )
    mensaje = models.TextField('mensaje', blank=True)
    estado = models.CharField(
        'estado', max_length=20, choices=Estado.choices,
        default=Estado.ENVIADA,
    )
    creado_en = models.DateTimeField('fecha de postulación', auto_now_add=True)

    class Meta:
        verbose_name = 'postulación'
        verbose_name_plural = 'postulaciones'
        ordering = ['-creado_en']
        constraints = [
            models.UniqueConstraint(fields=['oferta', 'estudiante'], name='postulacion_unica_por_estudiante_oferta'),
        ]
        indexes = [models.Index(fields=['oferta', 'estado'], name='postulacion_oferta_estado_idx')]

    def __str__(self):
        return f'{self.estudiante.nombre} — {self.oferta.titulo}'
