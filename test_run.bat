@echo off
cd /d c:\Ecualizer
echo ===== PRUEBA 1: Verificar configuración Django =====
python manage.py check
echo.
echo ===== PRUEBA 2: Migraciones =====
python manage.py migrate --run-syncdb
echo.
echo ===== PRUEBA 3: Hacer colecta de statics =====
python manage.py collectstatic --noinput
echo.
echo Listo para ejecutar el servidor. Presiona Enter para continuar...
pause
echo.
echo ===== INICIANDO SERVIDOR DJANGO =====
python manage.py runserver
