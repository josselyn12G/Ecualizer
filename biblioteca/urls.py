"""URLs de la app `biblioteca` (favoritos / social)."""

from django.urls import path

from .views import (
    ToggleLikeCancionView,
    ToggleSeguirArtistaView,
    ToggleGuardarAlbumView,
    MisCancionesLikedView,
    MisArtistasSeguidosView,
    MisAlbumesGuardadosView,
)


app_name = 'biblioteca'

urlpatterns = [
    # ── Toggles (POST → JSON) ──────────────────────────
    path('like/cancion/<int:pk>/',
         ToggleLikeCancionView.as_view(),
         name='toggle_like_cancion'),
    path('seguir/artista/<int:pk>/',
         ToggleSeguirArtistaView.as_view(),
         name='toggle_seguir_artista'),
    path('guardar/album/<int:pk>/',
         ToggleGuardarAlbumView.as_view(),
         name='toggle_guardar_album'),

    # ── Listas ───────────────────────────────────────
    path('mis-canciones/',
         MisCancionesLikedView.as_view(),
         name='mis_canciones_liked'),
    path('mis-artistas/',
         MisArtistasSeguidosView.as_view(),
         name='mis_artistas'),
    path('mis-albumes/',
         MisAlbumesGuardadosView.as_view(),
         name='mis_albumes'),
]
