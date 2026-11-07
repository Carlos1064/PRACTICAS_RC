from django.urls import path
from . import views

app_name = 'postulaciones'
urlpatterns = [
    path('ofertas/<int:oferta_pk>/postular/', views.crear, name='crear'),
    path('cuentas/postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),
    path('cuentas/postulaciones/<int:pk>/retirar/', views.retirar, name='retirar'),
    path('empresa/ofertas/<int:oferta_pk>/postulantes/', views.postulantes, name='postulantes'),
    path('empresa/postulaciones/<int:pk>/', views.detalle_candidato, name='detalle_candidato'),
    path('empresa/postulaciones/<int:pk>/estado/', views.cambiar_estado, name='cambiar_estado'),
]
