"""Conexión a MySQL. Los datos de acceso se leen del archivo .env."""

import os

import pymysql
from dotenv import load_dotenv
from pymysql.constants import CLIENT
from pymysql.cursors import DictCursor

load_dotenv()


def obtener_conexion() -> pymysql.connections.Connection:
    """Abre una conexión. Usarla con `with` para que se cierre sola."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "hyd_app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "reservas_hyd"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
        # Así un UPDATE sin cambios cuenta la fila como encontrada y no
        # parece que el pasajero no existe.
        client_flag=CLIENT.FOUND_ROWS,
    )
