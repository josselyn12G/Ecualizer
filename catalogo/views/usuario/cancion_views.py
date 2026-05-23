"""
Vistas de Cancion para el USUARIO (oyente).

SPs usados:
  - Catalogo.SP_ListarCanciones            → UsuarioCancionListView
  - Catalogo.SP_FiltrarCancionesGenero     → UsuarioCancionFilterView
  - Analitica.SP_RegistrarReproduccion     → UsuarioCancionDetailView (al reproducir)
"""

from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.db import DatabaseError

from usuarios.mixins import RequiereOyente
from ...models import Cancion, GeneroMusical
from ...services import (
    sp_listar_canciones,
    sp_filtrar_canciones_genero,
    sp_registrar_reproduccion,
)


# ──────────────────────────────────────────────────────────
# LIST · todas las canciones activas
# ──────────────────────────────────────────────────────────
class UsuarioCancionListView(RequiereOyente, View):
    template_name = 'catalogo/usuario/usuario_cancion.html'

    def get(self, request):
        busqueda = request.GET.get('q') or None

        # SP: SP_ListarCanciones (estado='activa' fijo)
        canciones = sp_listar_canciones(
            artista_id=None,
            album_id=None,
            estado='activa',
            busqueda=busqueda,
        )

        return render(request, self.template_name, {
            'canciones': canciones,
            'generos': GeneroMusical.objects.all(),
            'busqueda': busqueda or '',
            'genero_actual': '',
            'modo': 'list',
        })


# ──────────────────────────────────────────────────────────
# FILTER · por género musical
# ──────────────────────────────────────────────────────────
class UsuarioCancionFilterView(RequiereOyente, View):
    template_name = 'catalogo/usuario/usuario_cancion.html'

    def get(self, request, genero_id):
        # SP: SP_FiltrarCancionesGenero
        canciones = sp_filtrar_canciones_genero(genero_id=genero_id)
        genero = get_object_or_404(GeneroMusical, pk=genero_id)
        return render(request, self.template_name, {
            'canciones': canciones,
            'generos': GeneroMusical.objects.all(),
            'busqueda': '',
            'genero_actual': genero_id,
            'genero_nombre': genero.nombre_genero,
            'modo': 'filter',
        })


# ──────────────────────────────────────────────────────────
# DETAIL · ficha + (al hacer "play") registra reproducción
# ──────────────────────────────────────────────────────────
class UsuarioCancionDetailView(RequiereOyente, View):
    template_name = 'catalogo/usuario/usuario_cancion.html'

    def get(self, request, pk):
        cancion = get_object_or_404(
            Cancion.objects.select_related('album', 'album__artista'),
            pk=pk,
            estado_cancion='activa',
        )
        return render(request, self.template_name, {
            'cancion': cancion,
            'generos': GeneroMusical.objects.all(),
            'modo': 'detail',
        })

    def post(self, request, pk):
        """
        POST = el oyente presiona "play".
        Ejecuta SP_RegistrarReproduccion (regla de negocio).
        """
        cancion = get_object_or_404(Cancion, pk=pk, estado_cancion='activa')
        usuario_id = request.session['usuario_id']

        # Campos opcionales que el front envía (o defaults razonables)
        pais = request.POST.get('pais', 'Ecuador')
        try:
            duracion = int(request.POST.get('duracion_escuchada', cancion.duracion))
        except ValueError:
            return HttpResponseBadRequest('duracion_escuchada inválido')
        fue_saltada = request.POST.get('fue_saltada', 'N')

        try:
            resultado = sp_registrar_reproduccion(
                usuario_id=usuario_id,
                cancion_id=cancion.pk,
                pais=pais,
                duracion_escuchada=duracion,
                fue_saltada=fue_saltada,
            )
        except DatabaseError as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

        return JsonResponse({'ok': True, 'data': resultado})
