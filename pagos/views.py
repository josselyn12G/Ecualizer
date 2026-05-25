from django.views import View
from django.shortcuts import render
from django.db import DatabaseError

from usuarios.mixins import RequiereOyente
from .services import sp_historial_suscripciones_pagos


class HistorialSuscripcionesView(RequiereOyente, View):
    template_name = 'pagos/historial_suscripciones.html'

    def get(self, request):
        uid = request.session.get('usuario_id')
        try:
            historial = sp_historial_suscripciones_pagos(uid)
        except DatabaseError:
            historial = []

        return render(request, self.template_name, {
            'historial': historial,
            'total': len(historial),
        })