"""Reglas de usuarios: registro, inicio de sesión y administración."""

from __future__ import annotations

from app.config import config
from app.esquemas import CambioUsuario, Credenciales, NuevoUsuario, Sesion
from app.repositorios import usuarios
from app.seguridad import (
    NoAutenticadoError,
    cifrar_clave,
    clave_correcta,
    crear_token,
)
from app.servicios import NoEncontradoError, ReglaNoCumplidaError

# Mismo mensaje si el correo no existe o si la clave está mal: así nadie
# puede averiguar qué correos están registrados.
MENSAJE_LOGIN = "Correo o clave incorrectos."


def registrar(nuevo: NuevoUsuario, rol: str = "ASESOR") -> dict:
    """Todo el que se registra queda como ASESOR; el rol lo sube un ADMIN."""
    correo = nuevo.correo.strip().lower()
    try:
        id_usuario = usuarios.crear(
            nuevo.nombre.strip(), correo, cifrar_clave(nuevo.clave), rol
        )
    except usuarios.CorreoRepetidoError:
        raise ReglaNoCumplidaError(
            f"Ya existe un usuario con el correo {correo}."
        ) from None
    return usuarios.buscar_por_id(id_usuario)


def iniciar_sesion(credenciales: Credenciales) -> Sesion:
    usuario = usuarios.buscar_para_login(credenciales.correo.strip().lower())
    if usuario is None or not clave_correcta(
        credenciales.clave, usuario.pop("clave_hash")
    ):
        raise NoAutenticadoError(MENSAJE_LOGIN)
    if not usuario["activo"]:
        raise NoAutenticadoError("El usuario está inactivo.")
    return Sesion(
        access_token=crear_token(usuario),
        vence_en_minutos=config.jwt_minutos,
        usuario=usuario,
    )


def cambiar(id_usuario: int, cambio: CambioUsuario, quien: dict) -> dict:
    datos = cambio.model_dump(exclude_none=True)
    # Que un ADMIN no se quite a sí mismo el acceso por error.
    if id_usuario == quien["id_usuario"] and (
        datos.get("activo") is False or datos.get("rol", "ADMIN") != "ADMIN"
    ):
        raise ReglaNoCumplidaError(
            "No puede quitarse a sí mismo el rol ADMIN ni desactivarse."
        )
    if not usuarios.actualizar(id_usuario, datos):
        raise NoEncontradoError(f"No existe el usuario {id_usuario}.")
    return usuarios.buscar_por_id(id_usuario)
