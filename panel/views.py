import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.http import urlencode

from cuentas.models import Empresa
from cuentas.permissions import administrador_requerido
from ofertas.models import Categoria, Oferta
from postulaciones.models import Postulacion
from .forms import ReporteFiltrosForm


@login_required
@administrador_requerido
def dashboard(request):
    ofertas_categoria = list(
        Categoria.objects.annotate(total=Count('ofertas', filter=Q(ofertas__estado=Oferta.Estado.PUBLICADA)))
        .filter(total__gt=0).order_by('nombre').values('nombre', 'total')
    )
    estados_postulacion = list(
        Postulacion.objects.values('estado').annotate(total=Count('id')).order_by('estado')
    )
    etiquetas_estado = dict(Postulacion.Estado.choices)
    distribucion_estado = [{'estado': etiquetas_estado[item['estado']], 'total': item['total']} for item in estados_postulacion]
    return render(request, 'panel/dashboard.html', {
        'empresas_activas': Empresa.objects.filter(estado=Empresa.Estado.APROBADA).count(),
        'ofertas_publicadas': Oferta.objects.filter(estado=Oferta.Estado.PUBLICADA).count(),
        'postulaciones': Postulacion.objects.count(),
        'vinculaciones': Postulacion.objects.filter(estado=Postulacion.Estado.CONTRATADO).count(),
        'ofertas_categoria_json': json.dumps(ofertas_categoria, ensure_ascii=False),
        'estados_json': json.dumps(distribucion_estado, ensure_ascii=False),
        'ofertas_categoria': ofertas_categoria,
        'distribucion_estado': distribucion_estado,
    })


@administrador_requerido
def reporte(request):
    formulario = ReporteFiltrosForm(request.GET)
    queryset = Postulacion.objects.select_related(
        'estudiante', 'estudiante__perfil_estudiante', 'oferta',
        'oferta__empresa', 'oferta__categoria',
    )
    parametros = {}
    if formulario.is_valid():
        desde = formulario.cleaned_data.get('desde')
        hasta = formulario.cleaned_data.get('hasta')
        categoria = formulario.cleaned_data.get('categoria')
        if desde:
            queryset = queryset.filter(creado_en__date__gte=desde)
            parametros['desde'] = desde.isoformat()
        if hasta:
            queryset = queryset.filter(creado_en__date__lte=hasta)
            parametros['hasta'] = hasta.isoformat()
        if categoria:
            queryset = queryset.filter(oferta__categoria=categoria)
            parametros['categoria'] = str(categoria.pk)
    consulta = request.GET.get('q', '').strip()
    if consulta:
        queryset = queryset.filter(
            Q(estudiante__nombre__icontains=consulta) |
            Q(estudiante__correo__icontains=consulta) |
            Q(oferta__titulo__icontains=consulta) |
            Q(oferta__empresa__razon_social__icontains=consulta)
        )
        parametros['q'] = consulta

    if (request.GET.get('format') == 'csv' or request.path.endswith('.csv')) and formulario.is_valid():
        return exportar_csv(queryset)

    parametros_url = urlencode(parametros)
    page_obj = Paginator(queryset, 20).get_page(request.GET.get('page'))
    return render(request, 'panel/reporte.html', {
        'form': formulario,
        'page_obj': page_obj,
        'postulaciones': page_obj.object_list,
        'consulta': consulta,
        'querystring': parametros_url,
        'parametros_exportar': parametros_url,
    })


def exportar_csv(queryset):
    respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
    respuesta['Content-Disposition'] = 'attachment; filename="reporte_postulaciones.csv"'
    respuesta.write('\ufeff')
    escritor = csv.writer(respuesta, delimiter=';')
    escritor.writerow(['Fecha', 'Estudiante', 'Correo', 'Programa', 'Empresa', 'Categoría', 'Oferta', 'Estado'])
    for postulacion in queryset.iterator():
        perfil = getattr(postulacion.estudiante, 'perfil_estudiante', None)
        escritor.writerow([
            timezone.localtime(postulacion.creado_en).strftime('%Y-%m-%d %H:%M'),
            postulacion.estudiante.nombre,
            postulacion.estudiante.correo,
            perfil.programa if perfil else '',
            postulacion.oferta.empresa.razon_social,
            postulacion.oferta.categoria.nombre,
            postulacion.oferta.titulo,
            postulacion.get_estado_display(),
        ])
    return respuesta
