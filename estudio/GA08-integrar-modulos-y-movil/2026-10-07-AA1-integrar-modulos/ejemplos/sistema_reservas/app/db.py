"""Capa de datos: conexión a la base de datos (lo que en Spring Boot se configura en pom.xml
y application.properties con el conector de MySQL).

Por defecto usa SQLite (archivo reservas.db) para probar sin instalar nada.
Para MySQL, antes de arrancar:
    set DATABASE_URL=mysql+pymysql://root:TU_CLAVE@localhost:3306/reservas_hyd
"""

import os
from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

URL_POR_DEFECTO = f"sqlite:///{Path(__file__).resolve().parent.parent / 'reservas.db'}"
engine = create_engine(os.environ.get("DATABASE_URL", URL_POR_DEFECTO))


class Base(DeclarativeBase):
    pass


def obtener_sesion() -> Iterator[Session]:
    """Dependencia: FastAPI la "inyecta" en cada endpoint (como Spring con @Autowired)."""
    with Session(engine) as sesion:
        yield sesion
