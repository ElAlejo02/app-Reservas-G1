"""Guardar y consultar cotizaciones."""

from __future__ import annotations

from app.db import conectar

_COLUMNAS = (
    "c.id_cotizacion, c.codigo, c.estado, c.cliente_nombre, "
    "c.cliente_correo, c.destino_codigo, d.nombre AS destino, "
    "c.fecha_entrada, c.fecha_salida, c.noches, c.adultos, c.ninos, "
    "c.precio_hotel, c.precio_actividades, c.subtotal, "
    "c.descuento_porcentaje, c.descuento, c.iva_porcentaje, c.iva, "
    "c.tasas, c.total, "
    "c.fecha_creacion, h.nombre AS hotel, t.tipo_habitacion, t.temporada"
)
_DESDE = (
    "FROM cotizaciones c "
    "JOIN destinos d ON d.codigo = c.destino_codigo "
    "JOIN tarifas_hotel t ON t.id_tarifa = c.id_tarifa "
    "JOIN hoteles h ON h.id_hotel = t.id_hotel "
)
_DINERO = (
    "precio_hotel",
    "precio_actividades",
    "subtotal",
    "descuento",
    "iva",
    "tasas",
    "total",
)


def guardar(cotizacion: dict, lineas: list[dict]) -> str:
    """Guarda la cotización y sus actividades. Devuelve el código.

    Todo va en una sola transacción: o queda completa o no queda nada.
    """
    with conectar() as conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO cotizaciones (cliente_nombre, "
                    "cliente_correo, destino_codigo, fecha_entrada, "
                    "fecha_salida, noches, adultos, ninos, id_tarifa, "
                    "precio_hotel, precio_actividades, subtotal, "
                    "descuento_porcentaje, descuento, iva_porcentaje, iva, "
                    "tasas, total) "
                    "VALUES (%(cliente_nombre)s, %(cliente_correo)s, "
                    "%(destino_codigo)s, %(fecha_entrada)s, "
                    "%(fecha_salida)s, %(noches)s, %(adultos)s, %(ninos)s, "
                    "%(id_tarifa)s, %(precio_hotel)s, "
                    "%(precio_actividades)s, %(subtotal)s, "
                    "%(descuento_porcentaje)s, %(descuento)s, "
                    "%(iva_porcentaje)s, %(iva)s, "
                    "%(tasas)s, %(total)s)",
                    cotizacion,
                )
                nuevo_id = cursor.lastrowid
                # El código sale del id: 7 -> COT-000007.
                codigo = f"COT-{nuevo_id:06d}"
                cursor.execute(
                    "UPDATE cotizaciones SET codigo = %s "
                    "WHERE id_cotizacion = %s",
                    (codigo, nuevo_id),
                )
                cursor.executemany(
                    "INSERT INTO cotizacion_actividades (id_cotizacion, "
                    "id_actividad, adultos, ninos, precio) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    [
                        (
                            nuevo_id,
                            ln["id_actividad"],
                            ln["adultos"],
                            ln["ninos"],
                            ln["precio"],
                        )
                        for ln in lineas
                    ],
                )
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
    return codigo


def buscar(codigo: str) -> dict | None:
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(
            f"SELECT {_COLUMNAS} {_DESDE} WHERE c.codigo = %s", (codigo,)
        )
        fila = cursor.fetchone()
        if not fila:
            return None
        cursor.execute(
            "SELECT l.id_actividad, a.nombre, l.adultos, l.ninos, l.precio "
            "FROM cotizacion_actividades l "
            "JOIN actividades a ON a.id_actividad = l.id_actividad "
            "WHERE l.id_cotizacion = %s ORDER BY l.id_linea",
            (fila["id_cotizacion"],),
        )
        lineas = list(cursor.fetchall())
    for campo in _DINERO:
        fila[campo] = int(fila[campo])
    for linea in lineas:
        linea["precio"] = int(linea["precio"])
    fila["actividades"] = lineas
    return fila


def listar(estado: str | None = None, limite: int = 50) -> list[dict]:
    sql = (
        "SELECT codigo, estado, cliente_nombre, destino_codigo, "
        "fecha_entrada, total, fecha_creacion FROM cotizaciones "
    )
    parametros: tuple = ()
    if estado:
        sql += "WHERE estado = %s "
        parametros = (estado,)
    sql += "ORDER BY id_cotizacion DESC LIMIT %s"
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(sql, (*parametros, limite))
        filas = list(cursor.fetchall())
    for fila in filas:
        fila["total"] = int(fila["total"])
    return filas


def cambiar_estado(codigo: str, estado: str) -> None:
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE cotizaciones SET estado = %s WHERE codigo = %s",
                (estado, codigo),
            )
        conexion.commit()


def borrar(codigo: str) -> None:
    """Solo para las pruebas: las cotizaciones reales se ANULAN."""
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM cotizaciones WHERE codigo = %s", (codigo,)
            )
        conexion.commit()
