from django.shortcuts import render, redirect
from django.views import View

from ..forms import LoginForm, AdminLoginForm
from ..models import Persona, Usuario, Artista, Administrador


def _detectar_tipo(persona):
    try:
        persona.usuario
        return 'oyente'
    except Usuario.DoesNotExist:
        pass
    try:
        persona.artista
        return 'artista'
    except Artista.DoesNotExist:
        pass
    try:
        persona.administrador
        return 'administrador'
    except Administrador.DoesNotExist:
        pass
    return 'desconocido'


def _redirect_por_tipo(tipo):
    mapa = {
        'oyente': 'dashboard_oyente',
        'artista': 'dashboard_artista',
        'administrador': 'admin_dashboard',
    }
    return redirect(mapa.get(tipo, 'login'))


def index_usuarios(request):
    tipo = request.session.get('tipo_usuario')
    if tipo:
        return _redirect_por_tipo(tipo)
    return redirect('login')


class LoginView(View):
    template_name = 'usuarios/login.html'

    def get(self, request):
        if request.session.get('usuario_id'):
            return _redirect_por_tipo(request.session.get('tipo_usuario', ''))
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            persona = form.get_persona()
            tipo = _detectar_tipo(persona)
            request.session['usuario_id'] = persona.id_usuario
            request.session['usuario_nombre'] = persona.primer_nombre
            request.session['tipo_usuario'] = tipo
            return _redirect_por_tipo(tipo)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('login')


class SeleccionarTipoView(View):
    def get(self, request):
        return render(request, 'usuarios/seleccionar_tipo.html')


class AdminLoginView(View):
    """Login exclusivo para administradores — URL separada del login general."""
    template_name = 'usuarios/admin/login.html'

    def get(self, request):
        if request.session.get('tipo_usuario') == 'administrador':
            return redirect('admin_dashboard')
        return render(request, self.template_name, {'form': AdminLoginForm()})

    def post(self, request):
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            persona = form.get_persona()
            request.session['usuario_id'] = persona.id_usuario
            request.session['usuario_nombre'] = persona.primer_nombre
            request.session['tipo_usuario'] = 'administrador'
            return redirect('admin_dashboard')
        return render(request, self.template_name, {'form': form})
