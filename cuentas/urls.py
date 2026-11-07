from django.urls import path
from . import views

app_name = 'cuentas'
urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('registro/estudiante/', views.registro_estudiante, name='registro_estudiante'),
    path('registro/empresa/', views.registro_empresa, name='registro_empresa'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('salir/', views.salir, name='salir'),
    path('perfil/', views.perfil, name='perfil'),
]
