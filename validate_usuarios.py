#!/usr/bin/env python
"""
Script de validación del módulo usuarios
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, 'c:\\Ecualizer')

django.setup()

from django.urls import reverse, get_resolver
from django.test.client import Client

print("=" * 60)
print("VALIDACIÓN DEL MÓDULO USUARIOS")
print("=" * 60)

# 1. Validar URLs
print("\n✓ VALIDANDO URLS...")
try:
    resolver = get_resolver()
    
    # Verificar que las URLs estén registradas
    urls_to_check = [
        'index_usuarios',
        'persona_list', 'persona_create',
        'usuario_list', 'usuario_create',
        'artista_list', 'artista_create',
        'administrador_list', 'administrador_create',
    ]
    
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"  ✓ {url_name:20} -> {url}")
        except Exception as e:
            print(f"  ✗ {url_name:20} ERROR: {e}")
except Exception as e:
    print(f"  ✗ Error al verificar URLs: {e}")

# 2. Validar Templates
print("\n✓ VALIDANDO TEMPLATES...")
template_files = [
    'usuarios/index.html',
    'usuarios/persona_list.html',
    'usuarios/usuario_list.html',
    'usuarios/artista_list.html',
    'usuarios/administrador_list.html',
]

for template in template_files:
    path = f"c:\\Ecualizer\\usuarios\\templates\\{template}"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '{% block content %}' in content or '{% extends' in content:
                print(f"  ✓ {template}")
            else:
                print(f"  ⚠ {template} (sin estructura correcta)")
    else:
        print(f"  ✗ {template} NO ENCONTRADO")

# 3. Validar base.html
print("\n✓ VALIDANDO BASE.HTML...")
base_path = "c:\\Ecualizer\\templates\\base.html"
if os.path.exists(base_path):
    with open(base_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if '{% block content %}' in content:
            print(f"  ✓ base.html contiene {% block content %}")
        else:
            print(f"  ✗ base.html NO contiene {% block content %}")
else:
    print(f"  ✗ base.html NO ENCONTRADO")

# 4. Test HTTP (si el servidor está corriendo)
print("\n✓ INTENTANDO CONEXIÓN HTTP...")
try:
    client = Client()
    response = client.get('/usuarios/')
    print(f"  ✓ GET /usuarios/ -> Status {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ Página renderizada correctamente")
        if 'Módulo de Usuarios' in response.content.decode('utf-8'):
            print(f"  ✓ Contenido esperado presente")
        else:
            print(f"  ⚠ Contenido esperado NO encontrado")
except Exception as e:
    print(f"  ℹ No se pudo conectar (esperado si el servidor no está corriendo): {e}")

print("\n" + "=" * 60)
print("VALIDACIÓN COMPLETADA")
print("=" * 60)
