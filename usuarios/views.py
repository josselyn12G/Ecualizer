from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from .models import Persona, Usuario, Artista, Administrador
from .forms import PersonaForm, UsuarioForm, ArtistaForm, AdministradorForm, LoginForm


def index_usuarios(request):
    return render(request, 'usuarios/index.html')


class LoginView(View):
    form_class = LoginForm
    template_name = 'usuarios/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index_usuarios')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                request.session['user_id'] = user.id_usuario
                request.session['user_name'] = user.primer_nombre
                return redirect('index_usuarios')
        return render(request, self.template_name, {'form': form})


# =========================
# CRUD PERSONA
# =========================

class PersonaListView(ListView):
    model = Persona
    template_name = 'usuarios/persona_list.html'
    context_object_name = 'personas'


class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'usuarios/persona_form.html'
    success_url = reverse_lazy('persona_list')


class PersonaUpdateView(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'usuarios/persona_form.html'
    success_url = reverse_lazy('persona_list')


class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('persona_list')


# =========================
# CRUD USUARIO
# =========================

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'


class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('usuario_list')


# =========================
# CRUD ARTISTA
# =========================

class ArtistaListView(ListView):
    model = Artista
    template_name = 'usuarios/artista_list.html'
    context_object_name = 'artistas'


class ArtistaCreateView(CreateView):
    model = Artista
    form_class = ArtistaForm
    template_name = 'usuarios/artista_form.html'
    success_url = reverse_lazy('artista_list')


class ArtistaUpdateView(UpdateView):
    model = Artista
    form_class = ArtistaForm
    template_name = 'usuarios/artista_form.html'
    success_url = reverse_lazy('artista_list')


class ArtistaDeleteView(DeleteView):
    model = Artista
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('artista_list')


# =========================
# CRUD ADMINISTRADOR
# =========================

class AdministradorListView(ListView):
    model = Administrador
    template_name = 'usuarios/administrador_list.html'
    context_object_name = 'administradores'


class AdministradorCreateView(CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'usuarios/administrador_form.html'
    success_url = reverse_lazy('administrador_list')


class AdministradorUpdateView(UpdateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'usuarios/administrador_form.html'
    success_url = reverse_lazy('administrador_list')


class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'usuarios/confirm_delete.html'
    success_url = reverse_lazy('administrador_list')