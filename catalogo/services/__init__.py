"""
Servicios de catálogo — wrappers que invocan Stored Procedures de SQL Server.

Cada función abre un cursor con `connection.cursor()` y ejecuta `EXEC` sobre
el SP correspondiente del esquema [Catalogo].

Convención: las funciones devuelven el resultado del SP o lanzan la excepción
propagada por SQL Server (THROW) para que la vista la maneje.
"""

from .album_service import (
    sp_crear_album,
    sp_editar_album,
    sp_listar_albumes,
    sp_desactivar_album,
)
from .cancion_service import (
    sp_crear_cancion,
    sp_editar_cancion,
    sp_listar_canciones,
    sp_filtrar_canciones_genero,
    sp_desactivar_cancion,
    sp_reportar_cancion,
)
from .existing_sps import (
    sp_reporte_reproducciones_por_cancion,
    sp_top10_canciones_artista,
    sp_ranking_global_canciones,
    sp_registrar_reproduccion,
)

__all__ = [
    # SPs nuevos (creados en [Catalogo] por esta app)
    'sp_crear_album', 'sp_editar_album', 'sp_listar_albumes', 'sp_desactivar_album',
    'sp_crear_cancion', 'sp_editar_cancion', 'sp_listar_canciones',
    'sp_filtrar_canciones_genero', 'sp_desactivar_cancion', 'sp_reportar_cancion',
    # SPs existentes (reutilizados en las vistas)
    'sp_reporte_reproducciones_por_cancion',
    'sp_top10_canciones_artista',
    'sp_ranking_global_canciones',
    'sp_registrar_reproduccion',
]
