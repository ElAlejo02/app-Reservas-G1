"""Módulo de autenticación: registro e inicio de sesión contra la tabla usuarios."""

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import obtener_sesion
from app.esquemas import CredencialesDTO
from app.modelos import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/registro", status_code=201)
def registrar(datos: CredencialesDTO, sesion: Session = Depends(obtener_sesion)) -> dict:
    if sesion.scalar(select(Usuario).where(Usuario.usuario == datos.usuario)):
        raise HTTPException(409, "El usuario ya existe")
    clave_hash = bcrypt.hashpw(datos.contrasena.encode(), bcrypt.gensalt())
    sesion.add(Usuario(usuario=datos.usuario, clave_hash=clave_hash))
    sesion.commit()
    return {"mensaje": f"Usuario {datos.usuario} registrado"}


@router.post("/login")
def iniciar_sesion(datos: CredencialesDTO, sesion: Session = Depends(obtener_sesion)) -> dict:
    usuario = sesion.scalar(select(Usuario).where(Usuario.usuario == datos.usuario))
    if usuario is None or not bcrypt.checkpw(datos.contrasena.encode(), usuario.clave_hash):
        raise HTTPException(401, "Usuario o contraseña incorrectos")
    return {"mensaje": "Autenticación exitosa", "usuario": usuario.usuario, "rol": usuario.rol}
