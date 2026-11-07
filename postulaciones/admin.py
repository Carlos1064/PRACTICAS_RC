from django.contrib import admin
from .models import Postulacion


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('oferta', 'estudiante', 'estado', 'creado_en')
    list_filter = ('estado', 'creado_en')
    search_fields = ('oferta__titulo', 'estudiante__nombre', 'estudiante__correo')
    readonly_fields = ('creado_en',)
