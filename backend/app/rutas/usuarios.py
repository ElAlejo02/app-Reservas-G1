"""Registro, inicio de sesión y administración de usuarios."""

from fastapi import APIRouter, Depends, status

from app import autenticacion
from app.esquemas import (
    CambioUsuario,
    Credenciales,
    NuevoUsuario,
    Sesion,
    Usuario,
)
from app.repositorios import usuarios
from app.seguridad import solo_roles, usuario_actual

router = APIRouter(tags=["Usuarios"])
solo_admin = solo_roles("ADMIN")


@router.post(
    "/auth/registro",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
)
def registrar_usuario(nuevo: NuevoUsuario):
    """Queda como ASESOR. La clave necesita mínimo 8 caracteres, con
    letras y números.
    """
    return autenticacion.registrar(nuevo)


@router.post("/auth/login", response_model=Sesion, summary="Iniciar sesión")
def iniciar_sesion(credenciales: Credenciales):
    """Devuelve el token. En /docs se pega en el botón **Authorize**."""
    return autenticacion.iniciar_sesion(credenciales)


@router.get("/auth/yo", response_model=Usuario, summary="Ver mi usuario")
def ver_mi_usuario(usuario: dict = Depends(usuario_actual)):
    return usuario


@router.get(
    "/usuarios",
    response_model=list[Usuario],
    summary="Ver usuarios (solo ADMIN)",
    dependencies=[Depends(solo_admin)],
)
def ver_usuarios():
    return usuarios.listar()


@router.patch(
    "/usuarios/{id_usuario}",
    response_model=Usuario,
    summary="Cambiar rol o activar/desactivar (solo ADMIN)",
)
def cambiar_usuario(
    id_usuario: int,
    cambio: CambioUsuario,
    admin: dict = Depends(solo_admin),
):
    return autenticacion.cambiar(id_usuario, cambio, admin)
