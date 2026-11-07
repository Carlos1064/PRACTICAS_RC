from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import Empresa, PerfilEstudiante, Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('correo', 'nombre', 'rol')


@admin.register(Usuario)
class UsuarioAdmin(DjangoUserAdmin):
    add_form = UsuarioCreationForm
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


@admin.register(PerfilEstudiante)
class PerfilEstudianteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'programa', 'semestre', 'ciudad')
    search_fields = ('usuario__nombre', 'usuario__correo', 'programa', 'ciudad')
    list_filter = ('programa', 'ciudad')


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nit', 'sector', 'ciudad', 'estado')
    search_fields = ('razon_social', 'nit', 'usuario__correo')
    list_filter = ('estado', 'sector', 'ciudad')
    readonly_fields = ('creado_en',)
