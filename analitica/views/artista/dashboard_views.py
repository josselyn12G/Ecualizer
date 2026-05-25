"""Vistas de analítica del artista (dashboard + analytics filtrable)."""

from __future__ import annotations

from calendar import monthrange
from datetime import date

from django.shortcuts import render
from django.views import View

from usuarios.mixins import RequiereArtista
from usuarios.models import Persona, Artista
from catalogo.models import Album

from ...services import artista_service
from ...forms import FiltroAnalyticsArtistaForm


# ──────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────
def _get_persona_y_artista(request):
    uid = request.session.get('usuario_id')
    persona = Persona.objects.filter(pk=uid).first() if uid else None
    perfil = None
    if persona:
        try:
            perfil = persona.artista
        except (Artista.DoesNotExist, AttributeError):
            perfil = None
    return persona, perfil


def _albumes_del_artista(id_artista):
    return list(
        Album.objects
        .filter(artista_id=id_artista)
        .exclude(estado_album='eliminado')
        .values('id_album', 'titulo_album')
        .order_by('titulo_album')
    )


def _primer_y_ultimo_dia(mes: int, anio: int) -> tuple[date, date]:
    return date(anio, mes, 1), date(anio, mes, monthrange(anio, mes)[1])


# ──────────────────────────────────────────────────────────
# Dashboard (datos por defecto del mes actual)
# ──────────────────────────────────────────────────────────
class DashboardArtistaView(RequiereArtista, View):
    """Dashboard del artista. Sin filtros — usa el mes/año actual."""
    template_name = 'analitica/artista/dashboard.html'

    def get(self, request):
        persona, perfil = _get_persona_y_artista(request)
        id_artista = request.session.get('usuario_id')
        hoy = date.today()

        oyentes        = artista_service.oyentes_mensuales_crecimiento(
                            id_artista, hoy.month, hoy.year)
        top10          = artista_service.top10_canciones(id_artista, 'mes')
        geografia      = artista_service.distribucion_geografica(id_artista, 'mes')
        repros_cancion = artista_service.reproducciones_por_cancion(
                            id_artista, None, 'mes')

        ini, fin = _primer_y_ultimo_dia(hoy.month, hoy.year)
        regalias = artista_service.regalias_artista(
                            id_artista, ini.isoformat(), fin.isoformat())

        # KPIs derivados
        total_reproducciones_mes = sum(
            (r.get('TotalReproducciones') or 0) for r in repros_cancion)
        total_regalias_mes = sum(
            float(r.get('MontoNetoArtista') or 0) for r in regalias)

        return render(request, self.template_name, {
            'persona': persona,
            'perfil':  perfil,
            'oyentes':        oyentes,
            'top10':          top10,
            'geografia':      geografia,
            'repros_cancion': repros_cancion,
            'regalias':       regalias,
            'kpis': {
                'oyentes_mes':       oyentes.get('OyentesUnicosMes', 0) if oyentes else 0,
                'oyentes_anterior':  oyentes.get('OyentesUnicosMesAnterior', 0) if oyentes else 0,
                'crecimiento_pct':   oyentes.get('PorcentajeCrecimiento', 0) if oyentes else 0,
                'periodo_label':     oyentes.get('PeriodoConsultado', '') if oyentes else '',
                'reproducciones_mes': total_reproducciones_mes,
                'regalias_mes':       round(total_regalias_mes, 2),
            },
        })


# ──────────────────────────────────────────────────────────
# Analytics (mismos datos pero filtrables)
# ──────────────────────────────────────────────────────────
class AnalyticsArtistaView(RequiereArtista, View):
    """Analytics con filtros para todos los SPs del artista."""
    template_name = 'analitica/artista/analytics.html'

    def get(self, request):
        persona, perfil = _get_persona_y_artista(request)
        id_artista = request.session.get('usuario_id')
        hoy = date.today()

        # Defaults razonables
        defaults = {
            'periodo':                'mes',
            'periodo_top':            'mes',
            'mes':                    hoy.month,
            'anio':                   hoy.year,
            'desde':                  date(hoy.year, hoy.month, 1),
            'hasta':                  hoy,
            'valor_por_reproduccion': 0.004,
        }
        form = FiltroAnalyticsArtistaForm(request.GET or defaults)
        form.is_valid()
        d = form.cleaned_data

        periodo     = d.get('periodo')     or defaults['periodo']
        periodo_top = d.get('periodo_top') or defaults['periodo_top']
        album       = d.get('album') or None
        mes         = d.get('mes')   or defaults['mes']
        anio        = d.get('anio')  or defaults['anio']
        desde       = d.get('desde') or defaults['desde']
        hasta       = d.get('hasta') or defaults['hasta']
        valor       = float(d.get('valor_por_reproduccion') or defaults['valor_por_reproduccion'])

        albumes = _albumes_del_artista(id_artista)

        oyentes        = artista_service.oyentes_mensuales_crecimiento(id_artista, mes, anio)
        top10          = artista_service.top10_canciones(id_artista, periodo_top)
        geografia      = artista_service.distribucion_geografica(id_artista, periodo)
        repros_cancion = artista_service.reproducciones_por_cancion(
                            id_artista, album, periodo)
        regalias       = artista_service.regalias_artista(
                            id_artista, desde.isoformat(), hasta.isoformat(), valor)

        total_repros = sum(r.get('TotalReproducciones') or 0 for r in repros_cancion)
        total_regalias = sum(float(r.get('MontoNetoArtista') or 0) for r in regalias)

        return render(request, self.template_name, {
            'persona': persona,
            'perfil':  perfil,
            'form':    form,
            'albumes': albumes,
            'oyentes':        oyentes,
            'top10':          top10,
            'geografia':      geografia,
            'repros_cancion': repros_cancion,
            'regalias':       regalias,
            'filtros_aplicados': {
                'periodo': periodo, 'periodo_top': periodo_top,
                'mes': mes, 'anio': anio,
                'desde': desde, 'hasta': hasta,
                'valor': valor, 'album': album,
            },
            'kpis': {
                'oyentes_mes':       oyentes.get('OyentesUnicosMes', 0) if oyentes else 0,
                'oyentes_anterior':  oyentes.get('OyentesUnicosMesAnterior', 0) if oyentes else 0,
                'crecimiento_pct':   oyentes.get('PorcentajeCrecimiento', 0) if oyentes else 0,
                'periodo_label':     oyentes.get('PeriodoConsultado', '') if oyentes else '',
                'reproducciones_total': total_repros,
                'regalias_total':       round(total_regalias, 2),
            },
        })
