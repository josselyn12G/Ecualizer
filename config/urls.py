"""URL configuration for ecualizer_config project."""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    """Página inicial pública."""
    return render(request, 'home.html')


urlpatterns = [
    # ── Páginas públicas ───────────────────────────────────
    path('', home, name='home'),

    # ── Apps de Ecualizer ──────────────────────────────────
    path('usuarios/',   include('usuarios.urls')),
    path('catalogo/',   include('catalogo.urls')),
    path('biblioteca/', include('biblioteca.urls')),

    # IMPORTANTE: estos paths van ANTES de `admin/` porque Django resuelve
    # los patterns en orden y `path('admin/', admin.site.urls)` matchea
    # cualquier URL que empiece con `admin/` (incluyendo admin/analitica/…).
    # Si los pusiéramos después nunca llegarían a resolverse.
    path('admin/analitica/', include('analitica.urls')),
    path('admin/industria/', include('industria.urls')),

    # ── Django admin built-in (último para no interceptar las anteriores) ─
    path('admin/', admin.site.urls),
]
