from django.urls import path
from . import views

app_name = 'ofertas'
urlpatterns = [
    path('', views.lista, name='lista'),
    path('empresa/ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('admin-plataforma/categorias/', views.categorias, name='categorias'),
    path('admin-plataforma/categorias/nueva/', views.categoria_crear, name='categoria_crear'),
    path('admin-plataforma/categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('admin-plataforma/categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),
]
