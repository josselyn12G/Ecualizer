from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_usuarios, name='index_usuarios'),
    path('login/', views.LoginView.as_view(), name='login'),

    # Persona
    path('personas/', views.PersonaListView.as_view(), name='persona_list'),
    path('personas/crear/', views.PersonaCreateView.as_view(), name='persona_create'),
    path('personas/editar/<int:pk>/', views.PersonaUpdateView.as_view(), name='persona_update'),
    path('personas/eliminar/<int:pk>/', views.PersonaDeleteView.as_view(), name='persona_delete'),

    # Usuario
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/crear/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),

    # Artista
    path('artistas/', views.ArtistaListView.as_view(), name='artista_list'),
    path('artistas/crear/', views.ArtistaCreateView.as_view(), name='artista_create'),
    path('artistas/editar/<int:pk>/', views.ArtistaUpdateView.as_view(), name='artista_update'),
    path('artistas/eliminar/<int:pk>/', views.ArtistaDeleteView.as_view(), name='artista_delete'),

    # Administrador
    path('administradores/', views.AdministradorListView.as_view(), name='administrador_list'),
    path('administradores/crear/', views.AdministradorCreateView.as_view(), name='administrador_create'),
    path('administradores/editar/<int:pk>/', views.AdministradorUpdateView.as_view(), name='administrador_update'),
    path('administradores/eliminar/<int:pk>/', views.AdministradorDeleteView.as_view(), name='administrador_delete'),
]