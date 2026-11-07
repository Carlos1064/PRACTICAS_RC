from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import IngresoForm, RegistroEmpresaForm, RegistroEstudianteForm
from .models import Empresa, PerfilEstudiante


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
    perfil_estudiante = None
    empresa = None
    if request.user.rol == 'estudiante':
        perfil_estudiante = PerfilEstudiante.objects.filter(usuario=request.user).first()
    elif request.user.rol == 'empresa':
        empresa = Empresa.objects.filter(usuario=request.user).first()
    return render(request, 'cuentas/perfil.html', {
        'perfil_estudiante': perfil_estudiante,
        'empresa': empresa,
    })
