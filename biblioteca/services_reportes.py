from django.db import connection


def sp_crear_playlist(usuario_id, nombre, descripcion, visibilidad, tipo):
    with connection.cursor() as cur:
        cur.execute(
            "EXEC Biblioteca.SP_CrearPlaylistUsuario "
            "@Usuario_idUsuario=%s, @nombrePlaylist=%s, "
            "@descripcion=%s, @tipoVisibilidad=%s, @tipoPlaylist=%s;",
            [usuario_id, nombre, descripcion, visibilidad, tipo]
        )
        row = cur.fetchone()
        return row[0] if row else None


def sp_listar_playlists(usuario_id, visibilidad=None):
    with connection.cursor() as cur:
        cur.execute(
            "EXEC Biblioteca.sp_ListarPlaylistsUsuario "
            "@idUsuario=%s, @visibilidad=%s;",
            [usuario_id, visibilidad]
        )
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def sp_generos_favoritos(usuario_id):
    with connection.cursor() as cur:
        cur.execute(
            "EXEC Biblioteca.sp_ListarGenerosFavoritos @idUsuario=%s;",
            [usuario_id]
        )
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]