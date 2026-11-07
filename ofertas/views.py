from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import urlencode
from django.views.decorators.http import require_POST

from cuentas.models import Empresa
from cuentas.permissions import administrador_requerido, empresa_requerida
from .forms import CategoriaForm, OfertaForm
from .models import Categoria, Oferta
from postulaciones.models import Postulacion


@administrador_requerido
def categorias(request):
    consulta = request.GET.get('q', '').strip()
    queryset = Categoria.objects.all()
    if consulta:
        queryset = queryset.filter(Q(nombre__icontains=consulta) | Q(descripcion__icontains=consulta))
    page_obj = Paginator(queryset, 8).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    return render(request, 'ofertas/admin/categorias_lista.html', {
        'page_obj': page_obj, 'categorias': page_obj.object_list,
        'consulta': consulta, 'querystring': urlencode(parametros),
    })


@administrador_requerido
def categoria_crear(request):
    formulario = CategoriaForm(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        messages.success(request, 'La categoría se creó correctamente.')
        return redirect('ofertas:categorias')
    return render(request, 'ofertas/admin/categoria_formulario.html', {'form': formulario, 'accion': 'Crear'})


@administrador_requerido
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    formulario = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        messages.success(request, 'La categoría se actualizó correctamente.')
        return redirect('ofertas:categorias')
    return render(request, 'ofertas/admin/categoria_formulario.html', {'form': formulario, 'accion': 'Editar'})


@administrador_requerido
@require_POST
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    try:
        categoria.delete()
    except ProtectedError:
        messages.error(request, 'No se puede eliminar esta categoría porque tiene ofertas asociadas.')
    else:
        messages.success(request, 'La categoría se eliminó correctamente.')
    return redirect('ofertas:categorias')


def lista(request):
    hoy = timezone.localdate()
    queryset = Oferta.objects.filter(
        estado=Oferta.Estado.PUBLICADA,
        fecha_limite__gte=hoy,
        empresa__estado=Empresa.Estado.APROBADA,
    ).select_related('empresa', 'categoria')

    consulta = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    modalidad = request.GET.get('modalidad', '').strip()
    ciudad = request.GET.get('ciudad', '').strip()

    if consulta:
        queryset = queryset.filter(
            Q(titulo__icontains=consulta) | Q(descripcion__icontains=consulta) |
            Q(requisitos__icontains=consulta) | Q(empresa__razon_social__icontains=consulta) |
            Q(categoria__nombre__icontains=consulta)
        )
    if tipo in Oferta.Tipo.values:
        queryset = queryset.filter(tipo=tipo)
    if categoria_id.isdigit():
        queryset = queryset.filter(categoria_id=int(categoria_id))
    if modalidad in Oferta.Modalidad.values:
        queryset = queryset.filter(modalidad=modalidad)
    if ciudad:
        queryset = queryset.filter(empresa__ciudad__iexact=ciudad)

    page_obj = Paginator(queryset, 9).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    contexto = {
        'page_obj': page_obj,
        'ofertas': page_obj.object_list,
        'consulta': consulta,
        'tipo_filtro': tipo,
        'categoria_filtro': categoria_id,
        'modalidad_filtro': modalidad,
        'ciudad_filtro': ciudad,
        'categorias': Categoria.objects.order_by('nombre'),
        'tipos_oferta': Oferta.Tipo.choices,
        'modalidades': Oferta.Modalidad.choices,
        'ciudades': Empresa.objects.filter(estado=Empresa.Estado.APROBADA, ofertas__estado=Oferta.Estado.PUBLICADA, ofertas__fecha_limite__gte=hoy).values_list('ciudad', flat=True).distinct().order_by('ciudad'),
        'querystring': urlencode(parametros),
        'total_resultados': page_obj.paginator.count,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'ofertas/_resultados.html', contexto)
    return render(request, 'ofertas/lista.html', contexto)


def detalle(request, pk):
    oferta = get_object_or_404(
        Oferta.objects.select_related('empresa', 'categoria'),
        pk=pk, estado=Oferta.Estado.PUBLICADA,
    )
    postulacion = Postulacion.objects.filter(oferta=oferta, estudiante=request.user).first() if request.user.is_authenticated and request.user.rol == 'estudiante' else None
    return render(request, 'ofertas/detalle.html', {'oferta': oferta, 'vigente': oferta.fecha_limite >= timezone.localdate(), 'postulacion': postulacion})


@empresa_requerida
def mis_ofertas(request):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    if empresa.estado != Empresa.Estado.APROBADA:
        messages.warning(request, 'Empresa pendiente de aprobación')
    consulta = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    ofertas = Oferta.objects.filter(empresa=empresa).select_related('categoria')
    if consulta:
        ofertas = ofertas.filter(Q(titulo__icontains=consulta) | Q(categoria__nombre__icontains=consulta))
    if estado in Oferta.Estado.values:
        ofertas = ofertas.filter(estado=estado)
    page_obj = Paginator(ofertas, 8).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    return render(request, 'ofertas/empresa/lista.html', {
        'empresa': empresa, 'page_obj': page_obj, 'ofertas': page_obj.object_list,
        'consulta': consulta, 'estado_filtro': estado, 'querystring': urlencode(parametros),
        'estados_oferta': Oferta.Estado.choices,
    })


@empresa_requerida
def oferta_crear(request):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    if empresa.estado != Empresa.Estado.APROBADA:
        messages.error(request, 'Empresa pendiente de aprobación')
        return redirect('ofertas:mis_ofertas')
    formulario = OfertaForm(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        oferta = formulario.save(commit=False)
        oferta.empresa = empresa
        oferta.estado = Oferta.Estado.PENDIENTE
        oferta.save()
        messages.success(request, 'La oferta se creó y quedó pendiente de aprobación.')
        return redirect('ofertas:mis_ofertas')
    return render(request, 'ofertas/empresa/oferta_formulario.html', {'form': formulario, 'accion': 'Crear'})


@empresa_requerida
def oferta_editar(request, pk):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    if empresa.estado != Empresa.Estado.APROBADA:
        messages.error(request, 'Empresa pendiente de aprobación')
        return redirect('ofertas:mis_ofertas')
    oferta = get_object_or_404(Oferta, pk=pk, empresa=empresa)
    if oferta.estado == Oferta.Estado.CERRADA:
        messages.error(request, 'No puedes editar una oferta cerrada.')
        return redirect('ofertas:mis_ofertas')
    formulario = OfertaForm(request.POST or None, instance=oferta)
    if request.method == 'POST' and formulario.is_valid():
        oferta = formulario.save(commit=False)
        oferta.estado = Oferta.Estado.PENDIENTE
        oferta.save()
        messages.success(request, 'La oferta se actualizó y quedó pendiente de aprobación.')
        return redirect('ofertas:mis_ofertas')
    return render(request, 'ofertas/empresa/oferta_formulario.html', {'form': formulario, 'accion': 'Editar', 'oferta': oferta})


@empresa_requerida
@require_POST
def oferta_cerrar(request, pk):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    oferta = get_object_or_404(Oferta, pk=pk, empresa=empresa)
    if oferta.estado != Oferta.Estado.CERRADA:
        oferta.estado = Oferta.Estado.CERRADA
        oferta.save(update_fields=['estado'])
        messages.success(request, 'La oferta se cerró correctamente.')
    else:
        messages.info(request, 'La oferta ya estaba cerrada.')
    return redirect('ofertas:mis_ofertas')


@administrador_requerido
def ofertas_pendientes(request):
    consulta = request.GET.get('q', '').strip()
    queryset = Oferta.objects.filter(estado=Oferta.Estado.PENDIENTE).select_related('empresa', 'categoria')
    if consulta:
        queryset = queryset.filter(Q(titulo__icontains=consulta) | Q(empresa__razon_social__icontains=consulta))
    page_obj = Paginator(queryset, 10).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    return render(request, 'ofertas/admin/ofertas_pendientes.html', {
        'page_obj': page_obj, 'ofertas': page_obj.object_list,
        'consulta': consulta, 'querystring': urlencode(parametros),
    })


@administrador_requerido
@require_POST
def oferta_decision(request, pk):
    oferta = get_object_or_404(Oferta.objects.select_related('empresa'), pk=pk)
    decision = request.POST.get('decision')
    if oferta.estado != Oferta.Estado.PENDIENTE:
        messages.error(request, 'Esta oferta ya no está pendiente de revisión.')
    elif decision == 'aprobar' and oferta.empresa.estado != Empresa.Estado.APROBADA:
        messages.error(request, 'Aprueba primero la empresa antes de publicar sus ofertas.')
    elif decision == 'aprobar':
        oferta.estado = Oferta.Estado.PUBLICADA
        oferta.save(update_fields=['estado'])
        messages.success(request, 'La oferta quedó aprobada y publicada.')
    elif decision == 'rechazar':
        oferta.estado = Oferta.Estado.RECHAZADA
        oferta.save(update_fields=['estado'])
        messages.success(request, 'La oferta fue rechazada.')
    else:
        messages.error(request, 'La decisión enviada no es válida.')
    return redirect('ofertas:pendientes')
