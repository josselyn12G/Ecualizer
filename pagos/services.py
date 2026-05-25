from django.db import connection


def sp_historial_suscripciones_pagos(usuario_id):
    with connection.cursor() as cur:
        cur.execute(
            "EXEC Pagos.sp_HistorialSuscripcionesPagos @idUsuario=%s;",
            [usuario_id]
        )
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def sp_vencer_suscripciones_expiradas():
    with connection.cursor() as cur:
        cur.execute("EXEC Pagos.SP_VencerSuscripcionesExpiradas;")
        row = cur.fetchone()
        return row[0] if row else 0


def sp_generar_recordatorios_renovacion():
    with connection.cursor() as cur:
        cur.execute("EXEC Pagos.SP_GenerarRecordatoriosRenovacion;")
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]