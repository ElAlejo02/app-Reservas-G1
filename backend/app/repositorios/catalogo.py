"""Lectura de destinos, hoteles, tarifas y actividades."""

from __future__ import annotations

from datetime import date, timedelta

from app.db import conectar


def _leer(sql: str, parametros: tuple = ()) -> list[dict]:
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(sql, parametros)
        return list(cursor.fetchall())


def _enteros(fila: dict | None, *campos: str) -> dict | None:
    # MySQL devuelve los DECIMAL como Decimal; acá todo es en pesos enteros.
    if fila:
        for campo in campos:
            fila[campo] = int(fila[campo])
    return fila


def listar_destinos() -> list[dict]:
    filas = _leer(
        "SELECT codigo, nombre, exento_iva, tasa_por_persona "
        "FROM destinos ORDER BY nombre"
    )
    for fila in filas:
        fila["exento_iva"] = bool(fila["exento_iva"])
        _enteros(fila, "tasa_por_persona")
    return filas


def buscar_destino(codigo: str) -> dict | None:
    filas = [d for d in listar_destinos() if d["codigo"] == codigo]
    return filas[0] if filas else None


def listar_hoteles(destino: str | None = None) -> list[dict]:
    sql = (
        "SELECT id_hotel, nombre, destino_codigo, estrellas FROM hoteles "
        "WHERE activo"
    )
    if destino:
        return _leer(
            sql + " AND destino_codigo = %s ORDER BY nombre", (destino,)
        )
    return _leer(sql + " ORDER BY destino_codigo, nombre")


def listar_actividades(destino: str | None = None) -> list[dict]:
    sql = (
        "SELECT id_actividad, nombre, destino_codigo, descripcion, "
        "costo_adulto, costo_nino FROM actividades WHERE activo"
    )
    if destino:
        filas = _leer(
            sql + " AND destino_codigo = %s ORDER BY nombre", (destino,)
        )
    else:
        filas = _leer(sql + " ORDER BY destino_codigo, nombre")
    return [_enteros(f, "costo_adulto", "costo_nino") for f in filas]


def buscar_actividades(ids: list[int]) -> dict[int, dict]:
    """Devuelve {id: actividad} solo de las que existen y están activas."""
    if not ids:
        return {}
    marcas = ", ".join(["%s"] * len(ids))
    filas = _leer(
        "SELECT id_actividad, nombre, destino_codigo, costo_adulto, "
        f"costo_nino FROM actividades WHERE activo AND id_actividad IN "
        f"({marcas})",
        tuple(ids),
    )
    return {
        f["id_actividad"]: _enteros(f, "costo_adulto", "costo_nino")
        for f in filas
    }


_SQL_TARIFAS = (
    "SELECT t.id_tarifa, h.id_hotel, h.nombre AS hotel, h.estrellas, "
    "h.destino_codigo, t.tipo_habitacion, t.temporada, "
    "t.costo_adulto_noche, t.costo_nino_noche, t.capacidad_maxima "
    "FROM tarifas_hotel t JOIN hoteles h ON h.id_hotel = t.id_hotel "
    "WHERE h.activo "
)


def tarifas_disponibles(
    destino: str, entrada: date, salida: date, personas: int
) -> list[dict]:
    """Tarifas que cubren toda la estadía y donde caben todos.

    La última noche es la del día antes de la salida, por eso se resta un
    día. Si la estadía cruza dos temporadas no aparece (pendiente).
    """
    filas = _leer(
        _SQL_TARIFAS + "AND h.destino_codigo = %s AND t.fecha_desde <= %s "
        "AND t.fecha_hasta >= %s AND t.capacidad_maxima >= %s "
        "ORDER BY h.nombre, t.costo_adulto_noche",
        (destino, entrada, salida - timedelta(days=1), personas),
    )
    return [
        _enteros(f, "costo_adulto_noche", "costo_nino_noche") for f in filas
    ]
