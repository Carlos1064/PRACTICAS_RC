from django.urls import path
from . import views

app_name = 'ofertas'
urlpatterns = [
    path('', views.lista, name='lista'),
    path('empresa/ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('empresa/ofertas/nueva/', views.oferta_crear, name='crear'),
    path('empresa/ofertas/<int:pk>/editar/', views.oferta_editar, name='editar'),
    path('empresa/ofertas/<int:pk>/cerrar/', views.oferta_cerrar, name='cerrar'),
    path('admin-plataforma/categorias/', views.categorias, name='categorias'),
    path('admin-plataforma/categorias/nueva/', views.categoria_crear, name='categoria_crear'),
    path('admin-plataforma/categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('admin-plataforma/categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),
    path('admin-plataforma/ofertas/pendientes/', views.ofertas_pendientes, name='pendientes'),
    path('admin-plataforma/ofertas/<int:pk>/decision/', views.oferta_decision, name='decision'),
]
