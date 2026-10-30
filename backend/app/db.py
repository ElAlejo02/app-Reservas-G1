"""Conexión a MySQL."""

import pymysql
from pymysql.constants import CLIENT
from pymysql.cursors import DictCursor

from app.config import config


def conectar() -> pymysql.connections.Connection:
    """Abre una conexión. Usarla con `with` para que se cierre sola."""
    return pymysql.connect(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
        # Así un UPDATE sin cambios cuenta la fila como encontrada.
        client_flag=CLIENT.FOUND_ROWS,
    )
