from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlencode, url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import EmpresaPerfilForm, IngresoForm, PerfilEstudianteForm, RegistroEmpresaForm, RegistroEstudianteForm
from .models import Empresa, PerfilEstudiante
from .permissions import administrador_requerido, roles_requeridos


def inicio(request):
    return render(request, 'inicio.html')


def registro(request):
    return render(request, 'cuentas/registro.html')


def registro_estudiante(request):
    form = RegistroEstudianteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tu cuenta quedó creada. Ya puedes ingresar.')
        return redirect('cuentas:ingresar')
    return render(request, 'cuentas/registro_estudiante.html', {'form': form})


def registro_empresa(request):
    form = RegistroEmpresaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'La cuenta quedó registrada. La empresa está pendiente de aprobación.')
        return redirect('cuentas:ingresar')
    return render(request, 'cuentas/registro_empresa.html', {'form': form})


def ingresar(request):
    destino = request.POST.get('next') or request.GET.get('next', '')
    if request.user.is_authenticated:
        return _destino_por_rol(request.user.rol)
    form = IngresoForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.get_user()
        login(request, usuario)
        messages.success(request, f'Bienvenido/a, {usuario.nombre}.')
        if url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            return redirect(destino)
        return _destino_por_rol(usuario.rol)
    return render(request, 'cuentas/ingresar.html', {'form': form, 'next': destino})


def _destino_por_rol(rol):
    if rol == 'administrador':
        return redirect('panel:dashboard')
    if rol == 'empresa':
        return redirect('ofertas:mis_ofertas')
    return redirect('cuentas:perfil')


@require_POST
def salir(request):
    logout(request)
    messages.info(request, 'Has cerrado la sesión.')
    return redirect('inicio')


@login_required
def perfil(request):
    estudiante = PerfilEstudiante.objects.filter(usuario=request.user).first() if request.user.rol == 'estudiante' else None
    empresa = Empresa.objects.filter(usuario=request.user).first() if request.user.rol == 'empresa' else None
    return render(request, 'cuentas/perfil.html', {'perfil_estudiante': estudiante, 'empresa': empresa})


@roles_requeridos('estudiante', 'empresa')
def perfil_editar(request):
    if request.user.rol == 'estudiante':
        instancia = get_object_or_404(PerfilEstudiante, usuario=request.user)
        formulario = PerfilEstudianteForm(request.POST or None, instance=instancia, usuario=request.user)
    else:
        instancia = get_object_or_404(Empresa, usuario=request.user)
        formulario = EmpresaPerfilForm(request.POST or None, instance=instancia, usuario=request.user)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        messages.success(request, 'El perfil se actualizó correctamente.')
        return redirect('cuentas:perfil')
    return render(request, 'cuentas/perfil_editar.html', {'form': formulario})


@administrador_requerido
def empresas_pendientes(request):
    consulta = request.GET.get('q', '').strip()
    queryset = Empresa.objects.filter(estado=Empresa.Estado.PENDIENTE).select_related('usuario')
    if consulta:
        queryset = queryset.filter(Q(razon_social__icontains=consulta) | Q(nit__icontains=consulta) | Q(usuario__correo__icontains=consulta))
    page_obj = Paginator(queryset, 10).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    return render(request, 'cuentas/admin/empresas_pendientes.html', {
        'page_obj': page_obj, 'empresas': page_obj.object_list,
        'consulta': consulta, 'querystring': urlencode(parametros),
    })


@administrador_requerido
@require_POST
def empresa_decision(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    decision = request.POST.get('decision')
    if empresa.estado != Empresa.Estado.PENDIENTE:
        messages.error(request, 'Esta empresa ya no está pendiente de revisión.')
    elif decision == 'aprobar':
        empresa.estado = Empresa.Estado.APROBADA
        empresa.save(update_fields=['estado'])
        messages.success(request, f'{empresa.razon_social} quedó aprobada.')
    elif decision == 'rechazar':
        empresa.estado = Empresa.Estado.RECHAZADA
        empresa.save(update_fields=['estado'])
        messages.success(request, f'{empresa.razon_social} fue rechazada.')
    else:
        messages.error(request, 'La decisión enviada no es válida.')
    return redirect('cuentas_admin:empresas_pendientes')
