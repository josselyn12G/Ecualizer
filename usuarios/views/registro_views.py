from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.contrib import messages

from ..forms import RegistroPersonaForm, RegistroUsuarioForm, RegistroArtistaForm, RegistroAdministradorForm


class RegistroOyenteView(View):
    template_name = 'usuarios/registro/oyente_registro.html'

    def get(self, request):
        return render(request, self.template_name, {
            'persona_form': RegistroPersonaForm(),
            'usuario_form': RegistroUsuarioForm(),
            'paso_inicial': 1,
        })

    def post(self, request):
        persona_form = RegistroPersonaForm(request.POST)
        usuario_form = RegistroUsuarioForm(request.POST)

        if persona_form.is_valid() and usuario_form.is_valid():
            try:
                with transaction.atomic():
                    persona = persona_form.save()
                    usuario = usuario_form.save(commit=False)
                    usuario.id_usuario = persona
                    usuario.save()
                request.session['usuario_id'] = persona.id_usuario
                request.session['usuario_nombre'] = persona.primer_nombre
                request.session['tipo_usuario'] = 'oyente'
                messages.success(request, f'Bienvenido a Ecualizer, {persona.primer_nombre}!')
                return redirect('dashboard_oyente')
            except Exception as e:
                persona_form.add_error(None, f'Error al guardar: {e}')

        paso = 2 if (usuario_form.errors and not persona_form.errors) else 1
        return render(request, self.template_name, {
            'persona_form': persona_form,
            'usuario_form': usuario_form,
            'paso_inicial': paso,
        })


class RegistroArtistaView(View):
    template_name = 'usuarios/registro/artista_registro.html'

    def get(self, request):
        return render(request, self.template_name, {
            'persona_form': RegistroPersonaForm(),
            'artista_form': RegistroArtistaForm(),
            'paso_inicial': 1,
        })

    def post(self, request):
        persona_form = RegistroPersonaForm(request.POST)
        artista_form = RegistroArtistaForm(request.POST)

        if persona_form.is_valid() and artista_form.is_valid():
            try:
                with transaction.atomic():
                    persona = persona_form.save()
                    artista = artista_form.save(commit=False)
                    artista.id_usuario = persona
                    artista.save()
                request.session['usuario_id'] = persona.id_usuario
                request.session['usuario_nombre'] = persona.primer_nombre
                request.session['tipo_usuario'] = 'artista'
                messages.success(request, f'Bienvenido a Ecualizer, {persona.primer_nombre}!')
                return redirect('dashboard_artista')
            except Exception as e:
                persona_form.add_error(None, f'Error al guardar: {e}')

        paso = 2 if (artista_form.errors and not persona_form.errors) else 1
        return render(request, self.template_name, {
            'persona_form': persona_form,
            'artista_form': artista_form,
            'paso_inicial': paso,
        })


class RegistroAdminView(View):
    template_name = 'usuarios/registro/admin_registro.html'

    def get(self, request):
        return render(request, self.template_name, {
            'persona_form': RegistroPersonaForm(),
            'admin_form': RegistroAdministradorForm(),
            'paso_inicial': 1,
        })

    def post(self, request):
        persona_form = RegistroPersonaForm(request.POST)
        admin_form = RegistroAdministradorForm(request.POST)

        if persona_form.is_valid() and admin_form.is_valid():
            try:
                with transaction.atomic():
                    persona = persona_form.save()
                    admin = admin_form.save(commit=False)
                    admin.id_usuario = persona
                    admin.save()
                request.session['usuario_id'] = persona.id_usuario
                request.session['usuario_nombre'] = persona.primer_nombre
                request.session['tipo_usuario'] = 'administrador'
                messages.success(request, f'Bienvenido al panel, {persona.primer_nombre}!')
                return redirect('admin_dashboard')
            except Exception as e:
                persona_form.add_error(None, f'Error al guardar: {e}')

        paso = 2 if (admin_form.errors and not persona_form.errors) else 1
        return render(request, self.template_name, {
            'persona_form': persona_form,
            'admin_form': admin_form,
            'paso_inicial': paso,
        })
