from django.http import HttpResponse
from django.urls import path
from django.views import View

from config.urls import urlpatterns as rutas_principales


def provocar_error(request):
    raise RuntimeError('Este detalle interno no debe mostrarse al visitante.')


urlpatterns = [
    *rutas_principales,
    path('_prueba/error-500/', provocar_error),
]

handler403 = 'config.views.error_403'
handler404 = 'config.views.error_404'
handler500 = 'config.views.error_500'
