from django.db import models
from django.db.models import Q


class Categoria(models.Model):
    nombre = models.CharField('nombre', max_length=100, unique=True)
    descripcion = models.TextField('descripción', blank=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Oferta(models.Model):
    class Tipo(models.TextChoices):
        PRACTICA = 'practica', 'Práctica'
        EMPLEO = 'empleo', 'Empleo'

    class Modalidad(models.TextChoices):
        PRESENCIAL = 'presencial', 'Presencial'
        REMOTA = 'remota', 'Remota'
        HIBRIDA = 'hibrida', 'Híbrida'

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PUBLICADA = 'publicada', 'Publicada'
        RECHAZADA = 'rechazada', 'Rechazada'
        CERRADA = 'cerrada', 'Cerrada'

    empresa = models.ForeignKey('cuentas.Empresa', on_delete=models.PROTECT, related_name='ofertas', verbose_name='empresa')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='ofertas', verbose_name='categoría')
    titulo = models.CharField('título', max_length=180)
    descripcion = models.TextField('descripción')
    requisitos = models.TextField('requisitos')
    tipo = models.CharField('tipo de oportunidad', max_length=12, choices=Tipo.choices)
    modalidad = models.CharField('modalidad', max_length=12, choices=Modalidad.choices)
    vacantes = models.PositiveSmallIntegerField('vacantes')
    fecha_limite = models.DateField('fecha límite')
    estado = models.CharField('estado', max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    creado_en = models.DateTimeField('creada el', auto_now_add=True)

    class Meta:
        verbose_name = 'oferta'
        verbose_name_plural = 'ofertas'
        ordering = ['-creado_en', 'titulo']
        constraints = [models.CheckConstraint(condition=Q(vacantes__gt=0), name='oferta_vacantes_positivas')]
        indexes = [
            models.Index(fields=['estado', 'fecha_limite'], name='oferta_estado_fecha_idx'),
            models.Index(fields=['tipo', 'modalidad'], name='oferta_tipo_modalidad_idx'),
        ]

    def __str__(self):
        return self.titulo
