from django.db import models


class Postulacion(models.Model):
    class Estado(models.TextChoices):
        ENVIADA = 'enviada', 'Enviada'
        EN_REVISION = 'en_revision', 'En revisión'
        PRESELECCIONADO = 'preseleccionado', 'Preseleccionado'
        RECHAZADO = 'rechazado', 'Rechazado'
        CONTRATADO = 'contratado', 'Contratado'
        RETIRADA = 'retirada', 'Retirada'

    TRANSICIONES = {
        Estado.ENVIADA: (Estado.EN_REVISION, Estado.PRESELECCIONADO, Estado.RECHAZADO),
        Estado.EN_REVISION: (Estado.PRESELECCIONADO, Estado.RECHAZADO, Estado.CONTRATADO),
        Estado.PRESELECCIONADO: (Estado.EN_REVISION, Estado.RECHAZADO, Estado.CONTRATADO),
        Estado.RECHAZADO: (),
        Estado.CONTRATADO: (),
        Estado.RETIRADA: (),
    }

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
    estado = models.CharField('estado', max_length=20, choices=Estado.choices, default=Estado.ENVIADA)
    creado_en = models.DateTimeField('fecha de postulación', auto_now_add=True)

    class Meta:
        verbose_name = 'postulación'
        verbose_name_plural = 'postulaciones'
        ordering = ['-creado_en']
        constraints = [
            models.UniqueConstraint(fields=['oferta', 'estudiante'], name='postulacion_unica_por_estudiante_oferta'),
        ]
        indexes = [models.Index(fields=['oferta', 'estado'], name='postulacion_oferta_estado_idx')]

    @property
    def transiciones_disponibles(self):
        return self.TRANSICIONES.get(self.estado, ())

    @property
    def transiciones_con_etiquetas(self):
        disponibles = self.transiciones_disponibles
        return tuple((valor, etiqueta) for valor, etiqueta in self.Estado.choices if valor in disponibles)

    def __str__(self):
        return f'{self.estudiante.nombre} — {self.oferta.titulo}'
