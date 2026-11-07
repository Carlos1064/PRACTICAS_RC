from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(DjangoUserAdmin):
    ordering = ('correo',)
    list_display = ('correo', 'nombre', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('correo', 'nombre')
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información personal', {'fields': ('nombre', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'creado_en')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('correo', 'nombre', 'rol', 'password1', 'password2')}),
    )
    readonly_fields = ('creado_en', 'last_login')
