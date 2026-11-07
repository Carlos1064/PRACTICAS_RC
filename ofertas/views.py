from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlencode
from django.views.decorators.http import require_POST

from cuentas.permissions import administrador_requerido, empresa_requerida
from .forms import CategoriaForm
from .models import Categoria, Oferta


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
        'page_obj': page_obj,
        'categorias': page_obj.object_list,
        'consulta': consulta,
        'querystring': urlencode(parametros),
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
    ofertas = Oferta.objects.filter(estado=Oferta.Estado.PUBLICADA)
    page_obj = Paginator(ofertas, 9).get_page(request.GET.get('page'))
    return render(request, 'ofertas/lista.html', {'page_obj': page_obj, 'ofertas': page_obj.object_list, 'querystring': ''})


@empresa_requerida
def mis_ofertas(request):
    ofertas = Oferta.objects.filter(empresa__usuario=request.user)
    page_obj = Paginator(ofertas, 8).get_page(request.GET.get('page'))
    return render(request, 'ofertas/empresa/lista.html', {'page_obj': page_obj, 'ofertas': page_obj.object_list, 'querystring': ''})
