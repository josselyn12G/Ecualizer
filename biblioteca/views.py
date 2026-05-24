"""
Vistas de favoritos / social para el OYENTE.

- POST endpoints de toggle (devuelven JSON con el nuevo estado).
- Vistas de lista: "Canciones que me gustan", "Mis Artistas", "Mis Álbumes".
"""

import logging
import traceback

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import DatabaseError

from usuarios.mixins import RequiereOyente
from catalogo.services import (
    deezer_get_artist_image,
    deezer_get_track_image,
    deezer_get_album_image,
    deezer_enrich_canciones,
    deezer_enrich_albumes,
)

from . import services

logger = logging.getLogger('ecualizer.biblioteca')


# ──────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────
def _uid(request):
    return request.session.get('usuario_id')


def _ajax_ok(active: bool, **extra) -> JsonResponse:
    return JsonResponse({'ok': True, 'active': active, **extra})


def _ajax_err(msg: str) -> JsonResponse:
    return JsonResponse({'ok': False, 'error': msg}, status=400)


# ══════════════════════════════════════════════════════════
# TOGGLES (POST → JSON)
# ══════════════════════════════════════════════════════════
class ToggleLikeCancionView(RequiereOyente, View):
    def post(self, request, pk):
        usuario_id = _uid(request)
        try:
            active = services.toggle_like_cancion(usuario_id, int(pk))
            logger.info('LIKE cancion=%s usuario=%s → %s', pk, usuario_id, active)
            return _ajax_ok(active, kind='like_cancion', target_id=int(pk))
        except DatabaseError as e:
            logger.error('Error toggle_like_cancion: %s', e)
            logger.error(traceback.format_exc())
            return _ajax_err(str(e))

    def get(self, request, pk):
        return HttpResponseBadRequest('Use POST')


class ToggleSeguirArtistaView(RequiereOyente, View):
    def post(self, request, pk):
        usuario_id = _uid(request)
        try:
            active = services.toggle_seguir_artista(usuario_id, int(pk))
            logger.info('FOLLOW artista=%s usuario=%s → %s', pk, usuario_id, active)
            return _ajax_ok(active, kind='seguir_artista', target_id=int(pk))
        except DatabaseError as e:
            logger.error('Error toggle_seguir_artista: %s', e)
            logger.error(traceback.format_exc())
            return _ajax_err(str(e))

    def get(self, request, pk):
        return HttpResponseBadRequest('Use POST')


class ToggleGuardarAlbumView(RequiereOyente, View):
    def post(self, request, pk):
        usuario_id = _uid(request)
        try:
            active = services.toggle_guardar_album(usuario_id, int(pk))
            logger.info('SAVE album=%s usuario=%s → %s', pk, usuario_id, active)
            return _ajax_ok(active, kind='guardar_album', target_id=int(pk))
        except DatabaseError as e:
            logger.error('Error toggle_guardar_album: %s', e)
            logger.error(traceback.format_exc())
            return _ajax_err(str(e))

    def get(self, request, pk):
        return HttpResponseBadRequest('Use POST')


# ══════════════════════════════════════════════════════════
# LISTAS — Canciones que me gustan / Mis Artistas / Mis Álbumes
# ══════════════════════════════════════════════════════════
class MisCancionesLikedView(RequiereOyente, View):
    template_name = 'biblioteca/mis_canciones_liked.html'

    def get(self, request):
        usuario_id = _uid(request)
        try:
            canciones = services.get_canciones_liked(usuario_id)
        except DatabaseError as e:
            logger.error('Error cargando canciones liked: %s', e)
            canciones = []

        for c in canciones:
            c['coverUrl'] = deezer_get_track_image(
                c.get('nombreCancion') or '',
                c.get('nombreArtistico') or '',
                c.get('tituloAlbum') or '',
            )

        return render(request, self.template_name, {
            'canciones': canciones,
            'total': len(canciones),
        })


class MisArtistasSeguidosView(RequiereOyente, View):
    template_name = 'biblioteca/mis_artistas.html'

    def get(self, request):
        usuario_id = _uid(request)
        try:
            artistas = services.get_artistas_seguidos(usuario_id)
        except DatabaseError as e:
            logger.error('Error cargando artistas seguidos: %s', e)
            artistas = []

        for a in artistas:
            a['foto'] = deezer_get_artist_image(a.get('nombreArtistico') or '')

        return render(request, self.template_name, {
            'artistas': artistas,
            'total': len(artistas),
        })


class MisAlbumesGuardadosView(RequiereOyente, View):
    template_name = 'biblioteca/mis_albumes.html'

    def get(self, request):
        usuario_id = _uid(request)
        try:
            albumes = services.get_albumes_guardados(usuario_id)
        except DatabaseError as e:
            logger.error('Error cargando albumes guardados: %s', e)
            albumes = []

        deezer_enrich_albumes(albumes)
        # (deezer_enrich_albumes pone .coverUrl)

        return render(request, self.template_name, {
            'albumes': albumes,
            'total': len(albumes),
        })
