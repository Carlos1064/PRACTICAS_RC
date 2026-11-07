from django.contrib import admin
from django.urls import include, path
from cuentas.views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
    path('cuentas/', include('cuentas.urls')),
    path('', include('ofertas.urls')),
    path('admin-plataforma/', include('panel.urls')),
    path('admin/', admin.site.urls),
]

handler403 = 'config.views.error_403'
handler404 = 'config.views.error_404'
handler500 = 'config.views.error_500'
