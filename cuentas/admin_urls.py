from django.urls import path
from . import views

app_name = 'cuentas_admin'
urlpatterns = [
    path('empresas/pendientes/', views.empresas_pendientes, name='empresas_pendientes'),
    path('empresas/<int:pk>/decision/', views.empresa_decision, name='empresa_decision'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/<int:pk>/actualizar/', views.usuario_actualizar, name='usuario_actualizar'),
]
