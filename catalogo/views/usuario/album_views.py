"""
Vistas de Album para el USUARIO (oyente).

El oyente solo lee — nunca modifica.

SPs usados:
  - Catalogo.SP_ListarAlbumes  → UsuarioAlbumListView · solo activos
"""

from django.views.generic import View, DetailView
from django.shortcuts import render, get_object_or_404

from usuarios.mixins import RequiereOyente
from ...models import Album
from ...services import sp_listar_albumes


# ──────────────────────────────────────────────────────────
# LIST · álbumes activos (catálogo público para el oyente)
# ──────────────────────────────────────────────────────────
class UsuarioAlbumListView(RequiereOyente, View):
    template_name = 'catalogo/usuario/usuario_album.html'

    def get(self, request):
        busqueda = request.GET.get('q') or None
        # SP: SP_ListarAlbumes (estado='activo' fijo para usuarios)
        albumes = sp_listar_albumes(
            artista_id=None,
            estado='activo',
            busqueda=busqueda,
        )
        return render(request, self.template_name, {
            'albumes': albumes,
            'busqueda': busqueda or '',
            'modo': 'list',
        })


# ──────────────────────────────────────────────────────────
# DETAIL · ficha del álbum (incluye canciones activas)
# ──────────────────────────────────────────────────────────
class UsuarioAlbumDetailView(RequiereOyente, View):
    template_name = 'catalogo/usuario/usuario_album.html'

    def get(self, request, pk):
        album = get_object_or_404(
            Album.objects.select_related('artista', 'tipo_album'),
            pk=pk,
            estado_album='activo',
        )
        canciones = album.canciones.filter(estado_cancion='activa').order_by('numero_pista')
        return render(request, self.template_name, {
            'album': album,
            'canciones': canciones,
            'modo': 'detail',
        })


# ──────────────────────────────────────────────────────────
# SEARCH · búsqueda libre
# ──────────────────────────────────────────────────────────
class UsuarioAlbumSearchView(RequiereOyente, View):
    template_name = 'catalogo/usuario/usuario_album.html'

    def get(self, request):
        q = request.GET.get('q', '').strip()
        resultados = sp_listar_albumes(
            artista_id=None,
            estado='activo',
            busqueda=q if q else None,
        )
        return render(request, self.template_name, {
            'albumes': resultados,
            'busqueda': q,
            'modo': 'search',
            'es_busqueda': True,
        })
