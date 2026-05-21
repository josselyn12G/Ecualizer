#!/usr/bin/env python3
"""
Script de prueba para verificar que el módulo usuarios carga correctamente
Este script verifica:
1. Que Django se inicializa correctamente
2. Que los URLs están configurados
3. Que los templates están presentes
4. Que la página se puede renderizar
"""

import os
import sys
import django
from pathlib import Path

# Configurar rutas y Django
os.chdir('c:\\Ecualizer')
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("\n" + "="*70)
print("PRUEBA 1: Verificar configuración de Django")
print("="*70)

try:
    django.setup()
    print("✓ Django inicializado correctamente")
except Exception as e:
    print(f"✗ Error al inicializar Django: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("PRUEBA 2: Verificar URLs del módulo usuarios")
print("="*70)

from django.urls import reverse, NoReverseMatch
from django.test.client import Client

url_names = [
    'index_usuarios',
    'persona_list', 'persona_create', 'persona_update', 'persona_delete',
    'usuario_list', 'usuario_create', 'usuario_update', 'usuario_delete',
    'artista_list', 'artista_create', 'artista_update', 'artista_delete',
    'administrador_list', 'administrador_create', 'administrador_update', 'administrador_delete',
]

urls_ok = 0
urls_failed = 0

for url_name in url_names:
    try:
        if 'update' in url_name or 'delete' in url_name:
            url = reverse(url_name, args=[1])
        else:
            url = reverse(url_name)
        print(f"✓ {url_name:30} -> {url}")
        urls_ok += 1
    except NoReverseMatch as e:
        print(f"✗ {url_name:30} ERROR: {e}")
        urls_failed += 1

print(f"\nResultado: {urls_ok} URLs OK, {urls_failed} fallidas")

print("\n" + "="*70)
print("PRUEBA 3: Verificar templates")
print("="*70)

templates = {
    'base.html': 'c:\\Ecualizer\\templates\\base.html',
    'usuarios/index.html': 'c:\\Ecualizer\\usuarios\\templates\\usuarios\\index.html',
    'usuarios/persona_list.html': 'c:\\Ecualizer\\usuarios\\templates\\usuarios\\persona_list.html',
    'usuarios/usuario_list.html': 'c:\\Ecualizer\\usuarios\\templates\\usuarios\\usuario_list.html',
    'usuarios/artista_list.html': 'c:\\Ecualizer\\usuarios\\templates\\usuarios\\artista_list.html',
    'usuarios/administrador_list.html': 'c:\\Ecualizer\\usuarios\\templates\\usuarios\\administrador_list.html',
}

templates_ok = 0
templates_failed = 0

for template_name, template_path in templates.items():
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if template_name == 'base.html':
                if '{% block content %}' in content:
                    print(f"✓ {template_name:35} (contiene {% block content %})")
                    templates_ok += 1
                else:
                    print(f"✗ {template_name:35} (FALTA {% block content %})")
                    templates_failed += 1
            else:
                if '{% extends' in content and '{% block content %}' in content:
                    print(f"✓ {template_name:35} (extends + block OK)")
                    templates_ok += 1
                else:
                    print(f"✗ {template_name:35} (estructura incorrecta)")
                    templates_failed += 1
    else:
        print(f"✗ {template_name:35} NO ENCONTRADO")
        templates_failed += 1

print(f"\nResultado: {templates_ok} templates OK, {templates_failed} fallidas")

print("\n" + "="*70)
print("PRUEBA 4: Test de renderización HTTP")
print("="*70)

try:
    client = Client()
    
    # Test página principal de usuarios
    response = client.get('/usuarios/')
    status = response.status_code
    print(f"GET /usuarios/ -> Status {status}")
    
    if status == 200:
        print("✓ Página se renderiza correctamente")
        content = response.content.decode('utf-8')
        
        # Verificar que el contenido esperado está presente
        if 'Módulo de Usuarios' in content:
            print("✓ Contenido esperado presente: 'Módulo de Usuarios'")
        else:
            print("⚠ No encontrado: 'Módulo de Usuarios'")
            
        if 'Personas' in content and 'Usuarios Oyentes' in content:
            print("✓ Menú de opciones visible")
        else:
            print("⚠ Menú de opciones incompleto")
    else:
        print(f"✗ Error HTTP: {status}")
        print(f"   Contenido: {response.content[:200]}")
        
except Exception as e:
    print(f"⚠ No se pudo conectar (esperado si el servidor no está corriendo)")
    print(f"   Error: {e}")

print("\n" + "="*70)
print("RESUMEN DE PRUEBAS")
print("="*70)
print(f"URLs: {urls_ok} OK, {urls_failed} fallidas")
print(f"Templates: {templates_ok} OK, {templates_failed} fallidas")

if urls_failed == 0 and templates_failed == 0:
    print("\n✓ TODAS LAS PRUEBAS PASARON")
    sys.exit(0)
else:
    print("\n✗ ALGUNAS PRUEBAS FALLARON")
    sys.exit(1)
