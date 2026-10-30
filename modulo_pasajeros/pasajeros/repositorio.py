"""Repositorio: operaciones CRUD de pasajeros contra MySQL.

CRUD son las cuatro operaciones básicas sobre datos:

* **C**reate  -> ``crear``      -> ``INSERT``
* **R**ead    -> ``buscar_por_documento`` y ``listar`` -> ``SELECT``
* **U**pdate  -> ``actualizar`` -> ``UPDATE``
* **D**elete  -> ``eliminar``   -> ``DELETE``

Este archivo es el ÚNICO que escribe SQL. La interfaz no sabe nada de
MySQL: solo llama a estas funciones. Si mañana cambiamos MySQL por
PostgreSQL, solo se toca este archivo. A esa separación se le llama
"patrón repositorio".
"""

from __future__ import annotations

import pymysql

from pasajeros.conexion import obtener_conexion
from pasajeros.modelo import Pasajero

# --- Consultas SQL ---------------------------------------------------------
# Las consultas se guardan en constantes para leerlas fácil y no
# repetirlas. Los %s son "marcadores de posición": PyMySQL los reemplaza
# por los valores de forma SEGURA, escapando comillas y caracteres
# raros. Es lo mismo que los "?" del PreparedStatement de Java.
#
# NUNCA se arma el SQL pegando textos, por ejemplo:
#     f"SELECT * FROM pasajeros WHERE numero_documento = '{doc}'"
# porque alguien podría escribir  ' OR '1'='1  en el formulario y ver o
# borrar toda la tabla. Ese ataque se llama "inyección SQL".

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

# Código que devuelve MySQL cuando se viola una restricción UNIQUE
# (en nuestro caso, un número de documento repetido).
ERROR_DUPLICADO = 1062


# --- Funciones de apoyo (privadas) ------------------------------------------
# El guion bajo al inicio del nombre (_fila_a_pasajero) es una
# convención de PEP 8 que significa "uso interno de este módulo, no la
# llames desde afuera". Es lo más parecido a "private" de Java.
def _fila_a_pasajero(fila: dict) -> Pasajero:
    """Convierte una fila de MySQL (diccionario) en un ``Pasajero``."""
    # **fila "desempaca" el diccionario: cada llave se vuelve un
    # argumento con nombre. Equivale a escribir
    # Pasajero(id_pasajero=fila["id_pasajero"], nombre=fila["nombre"],
    # ...). Funciona porque las columnas del SELECT se llaman igual
    # que los atributos de la clase.
    return Pasajero(**fila)


# --- CRUD ----------------------------------------------------------------
def crear(pasajero: Pasajero) -> int:
    """Guarda un pasajero nuevo (INSERT).

    Args:
        pasajero: Pasajero ya validado y sin ``id_pasajero``.

    Returns:
        El ``id_pasajero`` que MySQL le asignó.

    Raises:
        ValueError: si ya existe un pasajero con ese documento.
    """
    # "with" abre la conexión y la CIERRA sola al salir del bloque,
    # incluso si hay un error. Evita conexiones "colgadas".
    with obtener_conexion() as conexion:
        # El cursor es el objeto que envía SQL y recibe resultados.
        with conexion.cursor() as cursor:
            try:
                # execute(sql, tupla): cada %s se llena en orden con
                # los valores de la tupla.
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
                # error.args[0] trae el código numérico de MySQL.
                if error.args[0] == ERROR_DUPLICADO:
                    raise ValueError(
                        "Ya existe un pasajero con el documento "
                        f"{pasajero.numero_documento}."
                    ) from error
                raise  # Cualquier otro error se deja subir tal cual.
            # lastrowid = el id AUTO_INCREMENT recién generado.
            nuevo_id = cursor.lastrowid
        # commit() confirma la transacción: SOLO aquí el cambio queda
        # guardado de verdad en el disco de MySQL.
        conexion.commit()
    return nuevo_id


def buscar_por_documento(numero_documento: str) -> Pasajero | None:
    """Busca un pasajero por su número de documento (SELECT).

    Returns:
        El ``Pasajero`` encontrado o ``None`` si no existe.
    """
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            # OJO: (valor,) con coma es una tupla de un elemento.
            # Sin la coma, (valor) sería solo el texto entre paréntesis.
            cursor.execute(SQL_BUSCAR, (numero_documento,))
            # fetchone() trae la primera fila o None si no hay ninguna.
            fila = cursor.fetchone()
    # Operador ternario: valor_si_verdadero if condicion else otro.
    return _fila_a_pasajero(fila) if fila else None


def listar() -> list[Pasajero]:
    """Devuelve todos los pasajeros ordenados por apellido (SELECT)."""
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(SQL_LISTAR)
            # fetchall() trae TODAS las filas como lista de diccionarios.
            filas = cursor.fetchall()
    # "List comprehension": crea una lista nueva aplicando la función a
    # cada fila. Equivale a un for con append, en una sola línea.
    return [_fila_a_pasajero(fila) for fila in filas]


def actualizar(pasajero: Pasajero) -> bool:
    """Modifica los datos de un pasajero existente (UPDATE).

    El número de documento se usa para encontrar la fila y no se
    modifica (es el identificador de negocio).

    Returns:
        ``True`` si se actualizó; ``False`` si el documento no existe.
    """
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            # execute() devuelve cuántas filas encontró el WHERE.
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
                    pasajero.numero_documento,  # Va en el WHERE.
                ),
            )
        conexion.commit()
    # Si 0 filas cumplieron el WHERE, el documento no existe.
    return filas_afectadas > 0


def eliminar(numero_documento: str) -> bool:
    """Borra un pasajero por su número de documento (DELETE).

    Returns:
        ``True`` si se eliminó; ``False`` si el documento no existe.
    """
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            filas_afectadas = cursor.execute(SQL_ELIMINAR, (numero_documento,))
        conexion.commit()
    return filas_afectadas > 0
