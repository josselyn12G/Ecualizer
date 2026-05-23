from django.shortcuts import render, redirect
from django.views import View

# Formularios de autenticación
from ..forms import LoginForm, AdminLoginForm

# Modelos de usuario
from ..models import Persona, Usuario, Artista, Administrador


# ----------------------------------------------------
# Detecta qué tipo de cuenta tiene la persona
# ----------------------------------------------------
def _detectar_tipo(persona):

    # Revisar si es usuario/oyente
    try:
        persona.usuario
        return 'oyente'
    except Usuario.DoesNotExist:
        pass

    # Revisar si es artista
    try:
        persona.artista
        return 'artista'
    except Artista.DoesNotExist:
        pass

    # Revisar si es administrador
    try:
        persona.administrador
        return 'administrador'
    except Administrador.DoesNotExist:
        pass

    # Si no coincide con ningún tipo
    return 'desconocido'


# ----------------------------------------------------
# Redirección automática según tipo de usuario
# ----------------------------------------------------
def _redirect_por_tipo(tipo):

    mapa = {
        'oyente': 'dashboard_oyente',
        'artista': 'dashboard_artista',
        'administrador': 'admin_dashboard',
    }

    return redirect(mapa.get(tipo, 'login'))


# ----------------------------------------------------
# Punto inicial usuarios/
# ----------------------------------------------------
def index_usuarios(request):

    tipo = request.session.get('tipo_usuario')

    # Si ya existe sesión activa → enviar dashboard
    if tipo:
        return _redirect_por_tipo(tipo)

    # Caso contrario → login
    return redirect('login')


# ====================================================
# LOGIN GENERAL (Oyentes + Artistas)
# ====================================================
class LoginView(View):

    template_name = 'usuarios/login.html'

    # -----------------------------------------
    # GET → cargar página login
    # -----------------------------------------
    def get(self, request):

        print("GET LOGIN EJECUTADO")

        # Si ya inició sesión → dashboard
        if request.session.get('usuario_id'):

            print("SESION YA EXISTENTE")

            return _redirect_por_tipo(
                request.session.get('tipo_usuario', '')
            )

        # Mostrar formulario vacío
        return render(
            request,
            self.template_name,
            {'form': LoginForm()}
        )

    # -----------------------------------------
    # POST → procesar login
    # -----------------------------------------
    def post(self, request):

        print("POST LOGIN RECIBIDO")

        # Crear formulario con datos enviados
        form = LoginForm(data=request.POST)

        print("FORMULARIO CREADO")

        # Validar formulario
        if form.is_valid():

            print("FORMULARIO VALIDO")

            # Obtener persona autenticada
            persona = form.get_persona()

            print("PERSONA:", persona)

            # Detectar tipo de usuario
            tipo = _detectar_tipo(persona)

            print("TIPO DETECTADO:", tipo)

            # Guardar sesión
            request.session['usuario_id'] = persona.id_usuario
            request.session['usuario_nombre'] = persona.primer_nombre
            request.session['tipo_usuario'] = tipo

            print("SESION GUARDADA")

            # Redireccionar dashboard
            return _redirect_por_tipo(tipo)

        # Si formulario inválido
        print("FORM INVALIDO")
        print(form.errors)
        print(form.non_field_errors())

        return render(
            request,
            self.template_name,
            {'form': form}
        )


# ====================================================
# LOGOUT
# ====================================================
class LogoutView(View):

    def get(self, request):

        print("CERRANDO SESION")

        # Eliminar toda la sesión
        request.session.flush()

        return redirect('login')


# ====================================================
# Selección tipo registro
# ====================================================
class SeleccionarTipoView(View):

    def get(self, request):

        print("PAGINA SELECCION TIPO")

        return render(
            request,
            'usuarios/seleccionar_tipo.html'
        )


# ====================================================
# LOGIN SOLO ADMINISTRADORES
# ====================================================
class AdminLoginView(View):

    template_name = 'usuarios/admin/login.html'

    # -----------------------------------------
    # GET admin login
    # -----------------------------------------
    def get(self, request):

        print("GET ADMIN LOGIN")

        # Si ya está logueado como admin
        if request.session.get('tipo_usuario') == 'administrador':

            print("ADMIN YA AUTENTICADO")

            return redirect('admin_dashboard')

        return render(
            request,
            self.template_name,
            {'form': AdminLoginForm()}
        )

    # -----------------------------------------
    # POST admin login
    # -----------------------------------------
    def post(self, request):

        print("POST ADMIN LOGIN")

        form = AdminLoginForm(data=request.POST)

        if form.is_valid():

            print("ADMIN FORM VALIDO")

            persona = form.get_persona()

            print("ADMIN:", persona)

            # Crear sesión admin
            request.session['usuario_id'] = persona.id_usuario
            request.session['usuario_nombre'] = persona.primer_nombre
            request.session['tipo_usuario'] = 'administrador'

            print("ADMIN LOGIN OK")

            return redirect('admin_dashboard')

        print("ADMIN FORM INVALIDO")
        print(form.errors)

        return render(
            request,
            self.template_name,
            {'form': form}
        )