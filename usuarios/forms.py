from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.backends import ModelBackend
from .models import Persona, Usuario, Artista, Administrador


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Persona.objects.get(correo=username)
        except Persona.DoesNotExist:
            return None
        
        if user.contrasena == password and self.user_can_authenticate(user):
            return user
        return None
    
    def user_can_authenticate(self, user):
        return user.estado == 'activo'


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'cedula_usuario',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'correo',
            'contrasena',
            'estado',
        ]
        widgets = {
            'contrasena': forms.PasswordInput(),
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario',
            'alias',
            'pais_usuario',
            'fecha_nacimiento',
            'genero',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = [
            'id_usuario',
            'nombre_artistico',
            'biografia',
        ]


class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = [
            'id_usuario',
            'rol_admin',
            'departamento',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario o Correo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@ecualizer.com',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )
    
    def get_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        try:
            persona = Persona.objects.get(correo=username)
            if persona.contrasena == password and persona.estado == 'activo':
                return persona
        except Persona.DoesNotExist:
            pass
        
        raise forms.ValidationError('Correo o contraseña incorrectos.')
    
    def clean(self):
        cleaned_data = super().clean()
        try:
            self.get_user()
        except forms.ValidationError as e:
            raise e
        return cleaned_data