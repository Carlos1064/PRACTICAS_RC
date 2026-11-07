from django.urls import path
from . import views

app_name = 'panel'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reportes/postulaciones.csv', views.reporte, name='reporte_csv'),
    path('reportes/postulaciones/', views.reporte, name='reporte'),
]
