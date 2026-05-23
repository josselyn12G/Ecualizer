from django.shortcuts import redirect
from django.contrib import messages


class RequiereLogin:
    """Redirige a login si no hay sesion activa."""
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesion para acceder.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class RequiereAdmin:
    """Redirige a login si el usuario no es administrador."""
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesion para acceder.')
            return redirect('login')
        if request.session.get('tipo_usuario') != 'administrador':
            messages.error(request, 'No tienes permisos para acceder al panel de administracion.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
