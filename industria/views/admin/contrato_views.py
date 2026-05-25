"""CRUD de Contratos con Discográficas (Administrador)."""

from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import DatabaseError

from usuarios.mixins import RequiereAdmin
from ...models import ContratoDiscografica
from ...forms import ContratoForm


class ContratoListView(RequiereAdmin, View):
    template_name = 'industria/admin/contrato_list.html'

    def get(self, request):
        estado = request.GET.get('estado') or ''
        qs = ContratoDiscografica.objects.select_related(
            'artista', 'discografica').order_by('-fecha_inicio')
        if estado:
            qs = qs.filter(estado_contrato=estado)
        return render(request, self.template_name, {
            'contratos': qs,
            'estado_sel': estado,
            'estados': ContratoDiscografica.ESTADO_CHOICES,
        })


class ContratoCreateView(RequiereAdmin, View):
    template_name = 'industria/admin/contrato_form.html'

    def get(self, request):
        return render(request, self.template_name,
                      {'form': ContratoForm(), 'modo': 'create'})

    def post(self, request):
        form = ContratoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Contrato creado correctamente.')
                return redirect('industria:contrato_list')
            except DatabaseError as e:
                messages.error(request, f'Error al guardar: {e}')
        return render(request, self.template_name, {'form': form, 'modo': 'create'})


class ContratoUpdateView(RequiereAdmin, View):
    template_name = 'industria/admin/contrato_form.html'

    def get(self, request, pk):
        obj = get_object_or_404(ContratoDiscografica, pk=pk)
        return render(request, self.template_name,
                      {'form': ContratoForm(instance=obj), 'obj': obj, 'modo': 'update'})

    def post(self, request, pk):
        obj = get_object_or_404(ContratoDiscografica, pk=pk)
        form = ContratoForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Contrato actualizado.')
                return redirect('industria:contrato_list')
            except DatabaseError as e:
                messages.error(request, f'Error al actualizar: {e}')
        return render(request, self.template_name,
                      {'form': form, 'obj': obj, 'modo': 'update'})


class ContratoDeleteView(RequiereAdmin, View):
    def post(self, request, pk):
        obj = get_object_or_404(ContratoDiscografica, pk=pk)
        try:
            obj.delete()
            messages.success(request, f'Contrato #{obj.id_contrato} eliminado.')
        except DatabaseError as e:
            messages.error(request, f'No se pudo eliminar: {e}')
        return redirect('industria:contrato_list')
