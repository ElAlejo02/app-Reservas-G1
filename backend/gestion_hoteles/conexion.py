"""Conexión a MySQL.

En Java esto es la clase que usa DriverManager.getConnection (JDBC).
Los datos salen del mismo archivo .env del backend, así la clave no
queda escrita en el código.
"""

import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv
from pymysql.constants import CLIENT
from pymysql.cursors import DictCursor

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def conectar() -> pymysql.connections.Connection:
    """Abre la conexión. Usarla con `with` para que se cierre sola."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "hyd_app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "reservas_hyd"),
        charset="utf8mb4",
        cursorclass=DictCursor,  # cada fila llega como diccionario
        # Así un UPDATE que deja los mismos datos cuenta la fila.
        client_flag=CLIENT.FOUND_ROWS,
    )
