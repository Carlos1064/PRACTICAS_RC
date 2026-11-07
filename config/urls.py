from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

handler403 = 'config.views.error_403'
handler404 = 'config.views.error_404'
handler500 = 'config.views.error_500'
