"""Conexión a la base de datos MySQL del proyecto HyD.

Este módulo tiene una sola responsabilidad: entregar una conexión
abierta a MySQL. Es el equivalente en Python a la clase ``Conexion``
que la instructora hizo en Java con ``DriverManager.getConnection()``
de JDBC.

Los datos de acceso (servidor, usuario, clave) NO se escriben aquí.
Se leen del archivo ``.env``, que nunca se sube a GitHub (está en el
``.gitignore``). Así, si alguien ve el repositorio, no ve la clave.
"""

# --- Importaciones -------------------------------------------------------
# PEP 8 pide importar en este orden, separado por una línea en blanco:
#   1) librería estándar de Python, 2) librerías de terceros,
#   3) módulos propios del proyecto.
import os  # Librería estándar: leer variables de entorno.

import pymysql  # Tercero: el "driver" que habla con MySQL (como JDBC).
from dotenv import load_dotenv  # Tercero: carga el archivo .env.
from pymysql.constants import CLIENT  # Opciones del cliente MySQL.
from pymysql.cursors import DictCursor  # Filas como diccionarios.

# --- Carga de configuración ---------------------------------------------
# load_dotenv() busca un archivo llamado .env y copia cada línea
# CLAVE=valor a las variables de entorno del programa. Se llama una sola
# vez, cuando Python importa este módulo por primera vez.
load_dotenv()


def obtener_conexion() -> pymysql.connections.Connection:
    """Abre y devuelve una conexión nueva a la base de datos.

    Quien llama a esta función debe cerrar la conexión cuando termine.
    La forma recomendada es usarla con ``with``, que la cierra sola
    aunque ocurra un error::

        with obtener_conexion() as conexion:
            ...

    Returns:
        Una conexión abierta de PyMySQL lista para crear cursores.

    Raises:
        pymysql.err.OperationalError: si MySQL está apagado, la clave
            es incorrecta o la base de datos no existe.
    """
    # os.getenv("NOMBRE", "por_defecto") lee una variable de entorno.
    # Si no existe, usa el valor por defecto (segundo argumento).
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        # El puerto llega como texto desde el .env; MySQL lo necesita
        # como número entero, por eso se convierte con int().
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "hyd_app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "reservas_hyd"),
        # utf8mb4 para que las tildes y la ñ lleguen bien.
        charset="utf8mb4",
        # DictCursor hace que cada fila llegue como diccionario:
        # {"nombre": "Ana", ...} en vez de una tupla ("Ana", ...).
        # Es más legible porque se accede por nombre de columna.
        cursorclass=DictCursor,
        # autocommit=False: los cambios NO se guardan hasta que se
        # llame a conexion.commit(). Igual que en JDBC con
        # setAutoCommit(false). Nos da control sobre cuándo guardar.
        autocommit=False,
        # Por defecto MySQL responde cuántas filas CAMBIARON en un
        # UPDATE. Si el usuario pulsa "Modificar" sin cambiar nada, la
        # respuesta sería 0 y pensaríamos que el pasajero no existe.
        # FOUND_ROWS hace que responda cuántas filas ENCONTRÓ el WHERE.
        client_flag=CLIENT.FOUND_ROWS,
    )
