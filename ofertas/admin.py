from django.contrib import admin
from .models import Categoria, Oferta


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'categoria', 'tipo', 'modalidad', 'estado', 'fecha_limite')
    list_filter = ('estado', 'tipo', 'modalidad', 'categoria')
    search_fields = ('titulo', 'empresa__razon_social', 'descripcion', 'requisitos')
    date_hierarchy = 'fecha_limite'
