"""CRUD de pasajeros en MySQL. Es el único archivo con SQL."""

from __future__ import annotations

import pymysql

from pasajeros.conexion import obtener_conexion
from pasajeros.modelo import Pasajero

# Los %s los llena PyMySQL de forma segura (evita inyección SQL).
# Nunca armar el SQL pegando lo que escribe el usuario.
COLUMNAS = (
    "id_pasajero, nombre, apellido, tipo_documento, numero_documento, "
    "fecha_nacimiento, pais, celular, correo"
)
SQL_INSERTAR = (
    "INSERT INTO pasajeros (nombre, apellido, tipo_documento, "
    "numero_documento, fecha_nacimiento, pais, celular, correo) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
)
SQL_BUSCAR = f"SELECT {COLUMNAS} FROM pasajeros WHERE numero_documento = %s"
SQL_LISTAR = f"SELECT {COLUMNAS} FROM pasajeros ORDER BY apellido, nombre"
SQL_ACTUALIZAR = (
    "UPDATE pasajeros SET nombre = %s, apellido = %s, "
    "tipo_documento = %s, fecha_nacimiento = %s, pais = %s, "
    "celular = %s, correo = %s WHERE numero_documento = %s"
)
SQL_ELIMINAR = "DELETE FROM pasajeros WHERE numero_documento = %s"

ERROR_DUPLICADO = 1062  # código de MySQL cuando se repite un UNIQUE


def _fila_a_pasajero(fila: dict) -> Pasajero:
    # Funciona porque las columnas se llaman igual que los atributos.
    return Pasajero(**fila)


def crear(pasajero: Pasajero) -> int:
    """Guarda un pasajero nuevo y devuelve su id."""
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            try:
                cursor.execute(
                    SQL_INSERTAR,
                    (
                        pasajero.nombre,
                        pasajero.apellido,
                        pasajero.tipo_documento,
                        pasajero.numero_documento,
                        pasajero.fecha_nacimiento,
                        pasajero.pais,
                        pasajero.celular,
                        pasajero.correo,
                    ),
                )
            except pymysql.err.IntegrityError as error:
                if error.args[0] == ERROR_DUPLICADO:
                    raise ValueError(
                        "Ya existe un pasajero con el documento "
                        f"{pasajero.numero_documento}."
                    ) from error
                raise
            nuevo_id = cursor.lastrowid
        conexion.commit()
    return nuevo_id


def buscar_por_documento(numero_documento: str) -> Pasajero | None:
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(SQL_BUSCAR, (numero_documento,))
            fila = cursor.fetchone()
    return _fila_a_pasajero(fila) if fila else None


def listar() -> list[Pasajero]:
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(SQL_LISTAR)
            filas = cursor.fetchall()
    return [_fila_a_pasajero(fila) for fila in filas]


def actualizar(pasajero: Pasajero) -> bool:
    """Busca por documento (que no se cambia). False si no existe."""
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            filas_afectadas = cursor.execute(
                SQL_ACTUALIZAR,
                (
                    pasajero.nombre,
                    pasajero.apellido,
                    pasajero.tipo_documento,
                    pasajero.fecha_nacimiento,
                    pasajero.pais,
                    pasajero.celular,
                    pasajero.correo,
                    pasajero.numero_documento,
                ),
            )
        conexion.commit()
    return filas_afectadas > 0


def eliminar(numero_documento: str) -> bool:
    """False si el documento no existe."""
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            filas_afectadas = cursor.execute(SQL_ELIMINAR, (numero_documento,))
        conexion.commit()
    return filas_afectadas > 0
