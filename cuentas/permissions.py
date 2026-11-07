from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def roles_requeridos(*roles):
    def decorador(vista):
        @login_required
        @wraps(vista)
        def protegida(request, *args, **kwargs):
            if request.user.rol not in roles:
                raise PermissionDenied
            return vista(request, *args, **kwargs)
        return protegida
    return decorador


def estudiante_requerido(vista):
    return roles_requeridos('estudiante')(vista)


def empresa_requerida(vista):
    return roles_requeridos('empresa')(vista)


def administrador_requerido(vista):
    return roles_requeridos('administrador')(vista)
