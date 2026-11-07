from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from cuentas.permissions import administrador_requerido
from cuentas.models import Empresa
from ofertas.models import Categoria, Oferta
from postulaciones.models import Postulacion


@login_required
@administrador_requerido
def dashboard(request):
    return render(request, 'panel/dashboard.html', {
        'empresas_activas': Empresa.objects.filter(estado=Empresa.Estado.APROBADA).count(),
        'ofertas_publicadas': Oferta.objects.filter(estado=Oferta.Estado.PUBLICADA).count(),
        'postulaciones': Postulacion.objects.count(),
        'categorias': Categoria.objects.count(),
    })
