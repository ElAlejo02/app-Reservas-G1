"""Claves cifradas, tokens de sesión y control de quién entra a qué.

Cómo funciona el login:
1. El usuario manda correo y clave a /auth/login.
2. Si la clave cuadra con la huella guardada, la API le entrega un token
   firmado (JWT) que dice quién es, qué rol tiene y cuándo vence.
3. En cada pedido protegido el frontend manda ese token en el encabezado
   Authorization: Bearer <token>. La API revisa la firma y ya sabe quién es,
   sin volver a pedir la clave.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import config
from app.repositorios import usuarios

ALGORITMO = "HS256"


class NoAutenticadoError(Exception):
    """Se responde con 401: falta el token o no sirve."""


class SinPermisoError(Exception):
    """Se responde con 403: sí es un usuario, pero su rol no alcanza."""


# ------------------------------------------------------------------ claves
def cifrar_clave(clave: str) -> str:
    """Huella bcrypt. Cada vez sale distinta por la sal, y no se devuelve."""
    return bcrypt.hashpw(clave.encode(), bcrypt.gensalt()).decode()


def clave_correcta(clave: str, huella: str) -> bool:
    return bcrypt.checkpw(clave.encode(), huella.encode())


# ------------------------------------------------------------------ tokens
def crear_token(usuario: dict) -> str:
    ahora = datetime.now(timezone.utc)
    datos = {
        "sub": str(usuario["id_usuario"]),
        "rol": usuario["rol"],
        "iat": ahora,
        "exp": ahora + timedelta(minutes=config.jwt_minutos),
    }
    return jwt.encode(datos, config.jwt_secreto, algorithm=ALGORITMO)


def leer_token(token: str) -> int:
    """Devuelve el id del usuario o lanza NoAutenticadoError."""
    try:
        datos = jwt.decode(token, config.jwt_secreto, algorithms=[ALGORITMO])
    except jwt.ExpiredSignatureError:
        raise NoAutenticadoError(
            "La sesión venció. Inicie sesión de nuevo."
        ) from None
    except jwt.InvalidTokenError:
        raise NoAutenticadoError("Token inválido.") from None
    return int(datos["sub"])


# ------------------------------------------------- dependencias de FastAPI
# auto_error=False para responder con nuestro propio mensaje en español.
_bearer = HTTPBearer(auto_error=False, description="Token de /auth/login")


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Se pone en una ruta para exigir sesión. Entrega el usuario."""
    if credenciales is None:
        raise NoAutenticadoError("Debe iniciar sesión.")
    usuario = usuarios.buscar_por_id(leer_token(credenciales.credentials))
    # El token puede seguir vigente aunque al usuario lo hayan desactivado.
    if usuario is None or not usuario["activo"]:
        raise NoAutenticadoError("El usuario no existe o está inactivo.")
    return usuario


def solo_roles(*roles: str):
    """Como usuario_actual, pero además exige uno de estos roles."""

    def revisar(usuario: dict = Depends(usuario_actual)) -> dict:
        if usuario["rol"] not in roles:
            raise SinPermisoError(
                f"Esta acción es solo para: {', '.join(roles)}."
            )
        return usuario

    return revisar
