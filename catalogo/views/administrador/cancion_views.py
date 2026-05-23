"""
Vistas de Cancion para el ADMINISTRADOR.

SPs usados:
  - Catalogo.SP_ListarCanciones              → AdminCancionListView
  - Analitica.sp_RankingGlobalCanciones      → AdminCancionListView (top 20 global)
  - Catalogo.SP_EditarCancion                → AdminCancionUpdateView
  - Catalogo.SP_DesactivarCancion            → AdminCancionUpdateView (acción rápida)
  - Catalogo.SP_ReportarCancion              → AdminCancionReportView
"""

from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import DatabaseError

from usuarios.mixins import RequiereAdmin
from ...models import Cancion, Album, GeneroMusical
from ...forms import CancionAdminUpdateForm, CancionReportForm
from ...services import (
    sp_listar_canciones,
    sp_editar_cancion,
    sp_desactivar_cancion,
    sp_reportar_cancion,
    sp_ranking_global_canciones,
)


# ──────────────────────────────────────────────────────────
# LIST · todas las canciones + ranking global
# ──────────────────────────────────────────────────────────
class AdminCancionListView(RequiereAdmin, View):
    template_name = 'catalogo/administrador/admin_cancion.html'

    def get(self, request):
        busqueda = request.GET.get('q') or None
        estado = request.GET.get('estado') or None

        # SP: SP_ListarCanciones
        canciones = sp_listar_canciones(
            artista_id=None, album_id=None,
            estado=estado, busqueda=busqueda,
        )

        # SP existente: sp_RankingGlobalCanciones
        try:
            ranking = sp_ranking_global_canciones(periodo='mes')
        except DatabaseError:
            ranking = []

        return render(request, self.template_name, {
            'canciones': canciones,
            'ranking_global': ranking,
            'busqueda': busqueda or '',
            'estado_actual': estado or '',
            'estados': Cancion.ESTADO_CHOICES,
            'modo': 'list',
        })


# ──────────────────────────────────────────────────────────
# UPDATE (admin)
# ──────────────────────────────────────────────────────────
class AdminCancionUpdateView(RequiereAdmin, View):
    template_name = 'catalogo/administrador/admin_cancion.html'

    def get(self, request, pk):
        cancion = get_object_or_404(Cancion, pk=pk)
        form = CancionAdminUpdateForm(instance=cancion)
        return render(request, self.template_name, {
            'form': form, 'cancion': cancion, 'modo': 'update',
        })

    def post(self, request, pk):
        cancion = get_object_or_404(Cancion, pk=pk)
        form = CancionAdminUpdateForm(request.POST, instance=cancion)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form, 'cancion': cancion, 'modo': 'update',
            })
        data = form.cleaned_data
        try:
            # SP: SP_EditarCancion (artista_id=None → admin)
            sp_editar_cancion(
                id_cancion=cancion.pk,
                nombre=data['nombre_cancion'],
                duracion=data['duracion'],
                fecha_lanzamiento=data['fecha_lanzamiento'],
                calidad_kbps=data['calidad_kbps'],
                letra=data.get('letra_cancion') or '',
                numero_pista=data['numero_pista'],
                estado=data['estado_cancion'],
                generos_ids=[g.pk for g in data.get('generos', [])],
                artista_id=None,
            )
            messages.success(request, 'Canción actualizada.')
        except DatabaseError as e:
            messages.error(request, f'Error: {e}')
            return render(request, self.template_name, {
                'form': form, 'cancion': cancion, 'modo': 'update',
            })
        return redirect('catalogo:admin_cancion_list')


# ──────────────────────────────────────────────────────────
# DEACTIVATE rápido
# ──────────────────────────────────────────────────────────
class AdminCancionDeactivateView(RequiereAdmin, View):
    def post(self, request, pk):
        cancion = get_object_or_404(Cancion, pk=pk)
        admin_id = request.session['usuario_id']
        try:
            sp_desactivar_cancion(id_cancion=cancion.pk, ejecutor_id=admin_id)
            messages.success(request, f'Canción "{cancion.nombre_cancion}" desactivada.')
        except DatabaseError as e:
            messages.error(request, f'Error: {e}')
        return redirect('catalogo:admin_cancion_list')


# ──────────────────────────────────────────────────────────
# REPORT · admin envía comentario al artista
# ──────────────────────────────────────────────────────────
class AdminCancionReportView(RequiereAdmin, View):
    template_name = 'catalogo/administrador/admin_cancion.html'

    def get(self, request, pk):
        cancion = get_object_or_404(Cancion, pk=pk)
        form = CancionReportForm()
        return render(request, self.template_name, {
            'form': form, 'cancion': cancion, 'modo': 'report',
        })

    def post(self, request, pk):
        cancion = get_object_or_404(Cancion, pk=pk)
        form = CancionReportForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form, 'cancion': cancion, 'modo': 'report',
            })
        admin_id = request.session['usuario_id']
        try:
            # SP: SP_ReportarCancion (registra reporte + bloquea canción)
            sp_reportar_cancion(
                id_cancion=cancion.pk,
                admin_id=admin_id,
                motivo=form.cleaned_data['motivo'],
                comentario=form.cleaned_data['comentario'],
            )
            messages.success(request, 'Reporte enviado al artista.')
        except DatabaseError as e:
            messages.error(request, f'Error: {e}')
            return render(request, self.template_name, {
                'form': form, 'cancion': cancion, 'modo': 'report',
            })
        return redirect('catalogo:admin_cancion_list')
