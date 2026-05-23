"""
URLs de la app `catalogo`.

Estructura:
  catalogo/
    ├── artista/album/...
    ├── artista/cancion/...
    ├── usuario/album/...
    ├── usuario/cancion/...
    ├── admin/album/...
    └── admin/cancion/...
"""

from django.urls import path

from .views.artista.album_views import (
    ArtistaAlbumListView, ArtistaAlbumCreateView,
    ArtistaAlbumUpdateView, ArtistaAlbumDeactivateView,
)
from .views.artista.cancion_views import (
    ArtistaCancionListView, ArtistaCancionCreateView,
    ArtistaCancionUpdateView, ArtistaCancionDeactivateView,
)
from .views.usuario.album_views import (
    UsuarioAlbumListView, UsuarioAlbumDetailView, UsuarioAlbumSearchView,
)
from .views.usuario.cancion_views import (
    UsuarioCancionListView, UsuarioCancionDetailView, UsuarioCancionFilterView,
)
from .views.administrador.album_views import (
    AdminAlbumListView, AdminAlbumUpdateView, AdminAlbumReportView,
)
from .views.administrador.cancion_views import (
    AdminCancionListView, AdminCancionUpdateView,
    AdminCancionDeactivateView, AdminCancionReportView,
)


app_name = 'catalogo'

urlpatterns = [
    # ═════════════════════════════════════════════════════
    # ARTISTA · Album
    # ═════════════════════════════════════════════════════
    path('artista/albumes/',
         ArtistaAlbumListView.as_view(),
         name='artista_album_list'),
    path('artista/albumes/nuevo/',
         ArtistaAlbumCreateView.as_view(),
         name='artista_album_create'),
    path('artista/albumes/<int:pk>/editar/',
         ArtistaAlbumUpdateView.as_view(),
         name='artista_album_update'),
    path('artista/albumes/<int:pk>/desactivar/',
         ArtistaAlbumDeactivateView.as_view(),
         name='artista_album_deactivate'),

    # ═════════════════════════════════════════════════════
    # ARTISTA · Cancion
    # ═════════════════════════════════════════════════════
    path('artista/canciones/',
         ArtistaCancionListView.as_view(),
         name='artista_cancion_list'),
    path('artista/canciones/nueva/',
         ArtistaCancionCreateView.as_view(),
         name='artista_cancion_create'),
    path('artista/canciones/<int:pk>/editar/',
         ArtistaCancionUpdateView.as_view(),
         name='artista_cancion_update'),
    path('artista/canciones/<int:pk>/desactivar/',
         ArtistaCancionDeactivateView.as_view(),
         name='artista_cancion_deactivate'),

    # ═════════════════════════════════════════════════════
    # USUARIO (oyente) · Album
    # ═════════════════════════════════════════════════════
    path('albumes/',
         UsuarioAlbumListView.as_view(),
         name='usuario_album_list'),
    path('albumes/buscar/',
         UsuarioAlbumSearchView.as_view(),
         name='usuario_album_search'),
    path('albumes/<int:pk>/',
         UsuarioAlbumDetailView.as_view(),
         name='usuario_album_detail'),

    # ═════════════════════════════════════════════════════
    # USUARIO (oyente) · Cancion
    # ═════════════════════════════════════════════════════
    path('canciones/',
         UsuarioCancionListView.as_view(),
         name='usuario_cancion_list'),
    path('canciones/<int:pk>/',
         UsuarioCancionDetailView.as_view(),
         name='usuario_cancion_detail'),
    path('canciones/genero/<int:genero_id>/',
         UsuarioCancionFilterView.as_view(),
         name='usuario_cancion_filter'),

    # ═════════════════════════════════════════════════════
    # ADMIN · Album
    # ═════════════════════════════════════════════════════
    path('admin/albumes/',
         AdminAlbumListView.as_view(),
         name='admin_album_list'),
    path('admin/albumes/<int:pk>/editar/',
         AdminAlbumUpdateView.as_view(),
         name='admin_album_update'),
    path('admin/albumes/<int:pk>/reportar/',
         AdminAlbumReportView.as_view(),
         name='admin_album_report'),

    # ═════════════════════════════════════════════════════
    # ADMIN · Cancion
    # ═════════════════════════════════════════════════════
    path('admin/canciones/',
         AdminCancionListView.as_view(),
         name='admin_cancion_list'),
    path('admin/canciones/<int:pk>/editar/',
         AdminCancionUpdateView.as_view(),
         name='admin_cancion_update'),
    path('admin/canciones/<int:pk>/desactivar/',
         AdminCancionDeactivateView.as_view(),
         name='admin_cancion_deactivate'),
    path('admin/canciones/<int:pk>/reportar/',
         AdminCancionReportView.as_view(),
         name='admin_cancion_report'),
]
