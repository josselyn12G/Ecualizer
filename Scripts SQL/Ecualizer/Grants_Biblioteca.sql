/* ============================================================
   Grants consolidados del esquema BIBLIOTECA
   ------------------------------------------------------------
   Otorga los permisos que la aplicación Ecualizer necesita para
   operar la Biblioteca del oyente: playlists, "me gusta",
   artistas seguidos y álbumes guardados.

   La app se conecta con un único login (user_Administrador), por
   lo que TODAS las operaciones pasan por ese usuario. Este script
   también incluye a los roles, por si en otra instalación la app
   usa logins por rol.

   Es IDEMPOTENTE (GRANT no falla si ya existe) y DEFENSIVO:
     · sólo otorga a los principals que realmente existen,
     · sólo otorga EXECUTE sobre los SP que existen.

   Ejecútalo (como dbo/sa) DESPUÉS de (re)crear los procedimientos,
   porque al recrear un SP con CREATE/DROP se pierden sus permisos.
   ============================================================ */

USE Ecualizer;
GO

SET NOCOUNT ON;

------------------------------------------------------------
-- Principals candidatos (se filtran a los que existan)
------------------------------------------------------------
DECLARE @principals TABLE (nombre SYSNAME);
INSERT INTO @principals (nombre) VALUES
    ('user_Administrador'),
    ('RolAdministrador'),
    ('user_Oyente'),
    ('RolOyente'),
    ('user_Sistema'),
    ('RolSistema');

------------------------------------------------------------
-- Tablas de Biblioteca sobre las que la app hace DML directo
------------------------------------------------------------
DECLARE @tablas TABLE (nombre SYSNAME);
INSERT INTO @tablas (nombre) VALUES
    ('Playlist'),
    ('UsuarioPlaylist'),
    ('CancionPlaylist'),
    ('UsuarioAlbum'),
    ('UsuarioCancionLike'),
    ('UsuarioSigueArtista');

DECLARE @p SYSNAME, @t SYSNAME, @sql NVARCHAR(MAX);

DECLARE cur_p CURSOR LOCAL FAST_FORWARD FOR
    SELECT nombre FROM @principals
    WHERE nombre IN (SELECT name FROM sys.database_principals);

OPEN cur_p;
FETCH NEXT FROM cur_p INTO @p;
WHILE @@FETCH_STATUS = 0
BEGIN
    ------------------------------------------------------------
    -- 1) EXECUTE sobre los SP de Biblioteca que existan
    ------------------------------------------------------------
    IF OBJECT_ID('Biblioteca.SP_CrearPlaylistUsuario') IS NOT NULL
    BEGIN
        SET @sql = 'GRANT EXECUTE ON Biblioteca.SP_CrearPlaylistUsuario TO ' + QUOTENAME(@p) + ';';
        EXEC sys.sp_executesql @sql;
    END

    IF OBJECT_ID('Biblioteca.sp_ListarPlaylistsUsuario') IS NOT NULL
    BEGIN
        SET @sql = 'GRANT EXECUTE ON Biblioteca.sp_ListarPlaylistsUsuario TO ' + QUOTENAME(@p) + ';';
        EXEC sys.sp_executesql @sql;
    END

    IF OBJECT_ID('Biblioteca.sp_ListarGenerosFavoritos') IS NOT NULL
    BEGIN
        SET @sql = 'GRANT EXECUTE ON Biblioteca.sp_ListarGenerosFavoritos TO ' + QUOTENAME(@p) + ';';
        EXEC sys.sp_executesql @sql;
    END

    ------------------------------------------------------------
    -- 2) SELECT/INSERT/UPDATE/DELETE sobre las tablas de Biblioteca
    --    (la app consulta y modifica estas tablas directamente)
    ------------------------------------------------------------
    DECLARE cur_t CURSOR LOCAL FAST_FORWARD FOR SELECT nombre FROM @tablas;
    OPEN cur_t;
    FETCH NEXT FROM cur_t INTO @t;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        IF OBJECT_ID('Biblioteca.' + @t) IS NOT NULL
        BEGIN
            SET @sql = 'GRANT SELECT, INSERT, UPDATE, DELETE ON Biblioteca.'
                       + QUOTENAME(@t) + ' TO ' + QUOTENAME(@p) + ';';
            EXEC sys.sp_executesql @sql;
        END
        FETCH NEXT FROM cur_t INTO @t;
    END
    CLOSE cur_t;
    DEALLOCATE cur_t;

    PRINT 'Permisos de Biblioteca otorgados a: ' + @p;
    FETCH NEXT FROM cur_p INTO @p;
END
CLOSE cur_p;
DEALLOCATE cur_p;
GO

PRINT 'Grants de Biblioteca aplicados correctamente.';
GO
