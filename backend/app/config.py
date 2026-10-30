"""Configuración leída del archivo .env."""

import logging
import os
import secrets
from dataclasses import dataclass
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()


def _lista(texto: str) -> list[str]:
    return [parte.strip() for parte in texto.split(",") if parte.strip()]


@dataclass(frozen=True)
class Config:
    """Todo lo que se puede cambiar sin tocar el código."""

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_user: str = os.getenv("DB_USER", "hyd_app")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "reservas_hyd")

    # Reglas de precio. Los porcentajes van como decimal: 0.20 = 20 %.
    margen: Decimal = Decimal(os.getenv("MARGEN", "0.20"))
    iva: Decimal = Decimal(os.getenv("IVA", "0.19"))
    descuento_maximo: int = int(os.getenv("DESCUENTO_MAXIMO", "15"))
    noches_maximas: int = int(os.getenv("NOCHES_MAXIMAS", "30"))

    # Páginas que pueden llamar la API (5500 es el puerto de Live Server).
    origenes_permitidos: tuple[str, ...] = tuple(
        _lista(
            os.getenv(
                "ORIGENES_PERMITIDOS",
                "http://127.0.0.1:5500,http://localhost:5500",
            )
        )
    )

    # Login: con qué se firman los tokens y cuánto duran (8 h = jornada).
    # Si el .env no trae secreto se inventa uno, pero al reiniciar la API
    # todos los tokens dejan de servir: sirve para probar, no para usar.
    jwt_secreto: str = os.getenv("JWT_SECRETO") or secrets.token_urlsafe(32)
    jwt_minutos: int = int(os.getenv("JWT_MINUTOS", "480"))


config = Config()

if not os.getenv("JWT_SECRETO"):
    logging.getLogger("uvicorn.error").warning(
        "JWT_SECRETO vacío en .env: se usa uno temporal."
    )
