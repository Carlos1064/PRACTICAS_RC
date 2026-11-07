from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import urlencode
from django.views.decorators.http import require_POST

from cuentas.models import Empresa, PerfilEstudiante, Usuario
from cuentas.permissions import empresa_requerida, estudiante_requerido
from ofertas.models import Oferta
from .forms import CambioEstadoForm, MensajePostulacionForm
from .models import Postulacion


@estudiante_requerido
@require_POST
def crear(request, oferta_pk):
    oferta = get_object_or_404(Oferta.objects.select_related('empresa'), pk=oferta_pk)
    if (oferta.estado != Oferta.Estado.PUBLICADA or
            oferta.empresa.estado != Empresa.Estado.APROBADA or
            oferta.fecha_limite < timezone.localdate()):
        messages.error(request, 'Oferta cerrada')
        if oferta.estado == Oferta.Estado.PUBLICADA:
            return redirect('ofertas:detalle', pk=oferta.pk)
        return redirect('ofertas:lista')

    formulario = MensajePostulacionForm(request.POST)
    if not formulario.is_valid():
        messages.error(request, 'Revisa el mensaje y vuelve a intentarlo.')
        return redirect('ofertas:detalle', pk=oferta.pk)

    try:
        with transaction.atomic():
            postulacion = formulario.save(commit=False)
            postulacion.oferta = oferta
            postulacion.estudiante = request.user
            postulacion.estado = Postulacion.Estado.ENVIADA
            postulacion.save()
    except IntegrityError:
        messages.warning(request, 'Ya enviaste una postulación para esta oferta.')
        return redirect('ofertas:detalle', pk=oferta.pk)

    messages.success(request, 'Tu postulación se envió correctamente.')
    return redirect('postulaciones:mis_postulaciones')


@estudiante_requerido
def mis_postulaciones(request):
    consulta = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    queryset = Postulacion.objects.filter(estudiante=request.user).select_related('oferta', 'oferta__empresa', 'oferta__categoria')
    if consulta:
        queryset = queryset.filter(Q(oferta__titulo__icontains=consulta) | Q(oferta__empresa__razon_social__icontains=consulta))
    if estado in Postulacion.Estado.values:
        queryset = queryset.filter(estado=estado)
    page_obj = Paginator(queryset, 10).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    return render(request, 'postulaciones/mis_lista.html', {
        'page_obj': page_obj, 'postulaciones': page_obj.object_list,
        'consulta': consulta, 'estado_filtro': estado,
        'estados': Postulacion.Estado.choices, 'querystring': urlencode(parametros),
    })


@estudiante_requerido
@require_POST
def retirar(request, pk):
    postulacion = get_object_or_404(Postulacion, pk=pk, estudiante=request.user)
    if postulacion.estado not in Postulacion.TRANSICIONES:
        messages.error(request, 'No fue posible retirar esta postulación.')
    elif postulacion.estado in (Postulacion.Estado.RECHAZADO, Postulacion.Estado.CONTRATADO, Postulacion.Estado.RETIRADA):
        messages.error(request, 'Esta postulación ya no se puede retirar.')
    else:
        postulacion.estado = Postulacion.Estado.RETIRADA
        postulacion.save(update_fields=['estado'])
        messages.success(request, 'Retiraste la postulación.')
    return redirect('postulaciones:mis_postulaciones')


@empresa_requerida
def postulantes(request, oferta_pk):
    oferta = get_object_or_404(Oferta.objects.select_related('empresa'), pk=oferta_pk)
    if oferta.empresa.usuario_id != request.user.id:
        raise PermissionDenied
    consulta = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    queryset = Postulacion.objects.filter(oferta=oferta).select_related('estudiante', 'estudiante__perfil_estudiante')
    if consulta:
        queryset = queryset.filter(
            Q(estudiante__nombre__icontains=consulta) |
            Q(estudiante__correo__icontains=consulta) |
            Q(estudiante__perfil_estudiante__programa__icontains=consulta)
        )
    if estado in Postulacion.Estado.values:
        queryset = queryset.filter(estado=estado)
    page_obj = Paginator(queryset, 10).get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    return render(request, 'postulaciones/empresa/lista.html', {
        'oferta': oferta, 'page_obj': page_obj, 'postulaciones': page_obj.object_list,
        'consulta': consulta, 'estado_filtro': estado,
        'estados': Postulacion.Estado.choices, 'querystring': urlencode(parametros),
    })


@empresa_requerida
def detalle_candidato(request, pk):
    postulacion = get_object_or_404(
        Postulacion.objects.select_related('estudiante', 'oferta', 'oferta__empresa', 'estudiante__perfil_estudiante'), pk=pk,
    )
    if postulacion.oferta.empresa.usuario_id != request.user.id:
        raise PermissionDenied
    return render(request, 'postulaciones/empresa/detalle_candidato.html', {'postulacion': postulacion})


@empresa_requerida
@require_POST
def cambiar_estado(request, pk):
    postulacion = get_object_or_404(Postulacion.objects.select_related('oferta', 'oferta__empresa'), pk=pk)
    if postulacion.oferta.empresa.usuario_id != request.user.id:
        raise PermissionDenied
    formulario = CambioEstadoForm(request.POST, postulacion=postulacion)
    if formulario.is_valid():
        postulacion.estado = formulario.cleaned_data['estado']
        postulacion.save(update_fields=['estado'])
        messages.success(request, 'El estado de la postulación se actualizó.')
    else:
        messages.error(request, 'La transición solicitada no está permitida.')
    return redirect('postulaciones:postulantes', oferta_pk=postulacion.oferta_id)
