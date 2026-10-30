"""Guardar y consultar usuarios."""

from __future__ import annotations

import pymysql

from app.db import conectar

_COLUMNAS = "id_usuario, nombre, correo, rol, activo, fecha_creacion"
ERROR_DUPLICADO = 1062


class CorreoRepetidoError(Exception):
    pass


def _uno(sql: str, parametros: tuple) -> dict | None:
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(sql, parametros)
        fila = cursor.fetchone()
    if fila:
        fila["activo"] = bool(fila["activo"])
    return fila


def crear(nombre: str, correo: str, clave_hash: str, rol: str) -> int:
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, correo, clave_hash, rol) "
                    "VALUES (%s, %s, %s, %s)",
                    (nombre, correo, clave_hash, rol),
                )
            except pymysql.err.IntegrityError as error:
                if error.args[0] == ERROR_DUPLICADO:
                    raise CorreoRepetidoError(correo) from error
                raise
            nuevo_id = cursor.lastrowid
        conexion.commit()
    return nuevo_id


def buscar_por_id(id_usuario: int) -> dict | None:
    return _uno(
        f"SELECT {_COLUMNAS} FROM usuarios WHERE id_usuario = %s",
        (id_usuario,),
    )


def buscar_para_login(correo: str) -> dict | None:
    """Es la única consulta que trae la huella de la clave."""
    return _uno(
        f"SELECT {_COLUMNAS}, clave_hash FROM usuarios WHERE correo = %s",
        (correo,),
    )


def listar() -> list[dict]:
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(f"SELECT {_COLUMNAS} FROM usuarios ORDER BY nombre")
        filas = list(cursor.fetchall())
    for fila in filas:
        fila["activo"] = bool(fila["activo"])
    return filas


def actualizar(id_usuario: int, cambios: dict) -> bool:
    """Cambia rol y/o activo. Devuelve False si el usuario no existe."""
    permitidos = {k: v for k, v in cambios.items() if k in ("rol", "activo")}
    if not permitidos:
        return buscar_por_id(id_usuario) is not None
    # Los nombres de columna salen de la lista fija de arriba, nunca del
    # usuario; los valores sí van con %s.
    asignaciones = ", ".join(f"{campo} = %s" for campo in permitidos)
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            filas = cursor.execute(
                f"UPDATE usuarios SET {asignaciones} WHERE id_usuario = %s",
                (*permitidos.values(), id_usuario),
            )
        conexion.commit()
    return filas > 0


def borrar(correo: str) -> None:
    """Solo para las pruebas."""
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE cotizaciones c JOIN usuarios u "
                "ON u.id_usuario = c.id_usuario SET c.id_usuario = NULL "
                "WHERE u.correo = %s",
                (correo,),
            )
            cursor.execute("DELETE FROM usuarios WHERE correo = %s", (correo,))
        conexion.commit()
