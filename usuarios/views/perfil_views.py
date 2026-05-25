from django.shortcuts import render
from django.views import View
from django.db import DatabaseError

from ..models import Persona, Usuario
from ..mixins import RequiereLogin
from analitica.services.oyente_service import (
    sp_top_canciones_usuario,
    sp_tiempo_total_escucha,
    sp_generos_favoritos_usuario,
    sp_recomendaciones_semanales,
)
from biblioteca.services import get_canciones_liked


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
        uid = persona.id_usuario

        try:
            perfil = persona.usuario
        except (Usuario.DoesNotExist, AttributeError):
            perfil = None

        try:
            top_canciones = sp_top_canciones_usuario(uid, 'mes')
        except DatabaseError:
            top_canciones = []

        try:
            tiempo = sp_tiempo_total_escucha(uid, 'mes')
            horas = tiempo[0]['TotalHoras'] if tiempo else 0
        except DatabaseError:
            horas = 0

        try:
            generos = sp_generos_favoritos_usuario(uid, 'mes')
        except DatabaseError:
            generos = []

        try:
            recomendaciones = sp_recomendaciones_semanales(uid)
        except DatabaseError:
            recomendaciones = []

        try:
            likes = get_canciones_liked(uid)
            n_likes = len(likes)
        except DatabaseError:
            n_likes = 0

        historial = []
        for c in top_canciones[:8]:
            historial.append({
                'nombre':   c.get('nombreCancion', ''),
                'artista':  c.get('nombreArtistico', '') or c.get('Artista', ''),
                'album':    c.get('tituloAlbum', '') or c.get('Album', ''),
                'duracion': c.get('UltimaVezEscuchada', ''),
            })

        return render(request, 'usuarios/oyente/dashboard.html', {
            'persona':         persona,
            'perfil':          perfil,
            'top_canciones':   top_canciones,
            'recomendaciones': recomendaciones,
            'generos':         generos,
            'historial':       historial,
            'stats': {
                'canciones_favoritas': n_likes,
                'playlists':           0,
                'artistas_seguidos':   0,
                'horas_escuchadas':    horas,
            },
        })


class DashboardArtistaView(RequiereLogin, View):
    """Dashboard del artista — delega a la vista analítica del módulo analitica."""

    def get(self, request):
        if request.session.get('tipo_usuario') != 'artista':
            from .auth_views import _redirect_por_tipo
            return _redirect_por_tipo(request.session.get('tipo_usuario', ''))

        from analitica.views.artista import DashboardArtistaView as _DashAnalitica
        return _DashAnalitica.as_view()(request)