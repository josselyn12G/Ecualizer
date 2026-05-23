from django.shortcuts import render, redirect
from django.views import View

from ..models import Persona, Usuario, Artista
from ..mixins import RequiereLogin


def _get_persona(request):
    uid = request.session.get('usuario_id')
    if not uid:
        return None
    try:
        return Persona.objects.get(pk=uid)
    except Persona.DoesNotExist:
        return None


class DashboardOyenteView(RequiereLogin, View):
    def get(self, request):
        if request.session.get('tipo_usuario') != 'oyente':
            from .auth_views import _redirect_por_tipo
            return _redirect_por_tipo(request.session.get('tipo_usuario', ''))

        persona = _get_persona(request)
        try:
            perfil = persona.usuario
        except (Usuario.DoesNotExist, AttributeError):
            perfil = None

        return render(request, 'usuarios/oyente/dashboard.html', {
            'persona': persona,
            'perfil': perfil,
            'stats': {
                'canciones_favoritas': 0,
                'playlists': 0,
                'artistas_seguidos': 0,
                'horas_escuchadas': 0,
            },
            'historial': [],
        })


class DashboardArtistaView(RequiereLogin, View):
    def get(self, request):
        if request.session.get('tipo_usuario') != 'artista':
            from .auth_views import _redirect_por_tipo
            return _redirect_por_tipo(request.session.get('tipo_usuario', ''))

        persona = _get_persona(request)
        try:
            perfil = persona.artista
        except (Artista.DoesNotExist, AttributeError):
            perfil = None

        return render(request, 'usuarios/artista/dashboard.html', {
            'persona': persona,
            'perfil': perfil,
            'stats': {
                'albumes': 0,
                'canciones': 0,
                'reproducciones': 0,
                'seguidores': 0,
            },
            'canciones_recientes': [],
        })
