"""Aplicación integrada: une los módulos (auth y hoteles), la base de datos y el frontend.

Equivale a la clase principal de Spring Boot (@SpringBootApplication con su main) que
arranca el servidor en el puerto 8080 y publica los controladores.

Cómo correrlo (desde la carpeta sistema_reservas):
    pip install "fastapi<0.145" uvicorn sqlalchemy pymysql bcrypt
    uvicorn app.main:app --reload --port 8080
Abrir http://127.0.0.1:8080  (usuario de prueba: admin / 12345)
Documentación de la API: http://127.0.0.1:8080/docs
"""

from contextlib import asynccontextmanager
from pathlib import Path

import bcrypt
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, engine
from app.modelos import Hotel, Usuario
from app.rutas import auth, hoteles


def preparar_base_de_datos() -> None:
    """Crea las tablas si no existen y deja datos iniciales para probar."""
    Base.metadata.create_all(engine)
    with Session(engine) as sesion:
        if not sesion.scalar(select(Usuario).where(Usuario.usuario == "admin")):
            clave = bcrypt.hashpw(b"12345", bcrypt.gensalt())
            sesion.add(Usuario(usuario="admin", clave_hash=clave, rol="ADMIN"))
        if not sesion.scalar(select(Hotel)):
            sesion.add_all(
                [
                    Hotel(
                        nombre="Hotel Nogal", ciudad="Medellín", estrellas=4, tarifa_noche=250000
                    ),
                    Hotel(
                        nombre="Hotel Bahía", ciudad="Cartagena", estrellas=5, tarifa_noche=480000
                    ),
                ]
            )
        sesion.commit()


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    preparar_base_de_datos()  # se ejecuta una vez al arrancar el servidor
    yield


app = FastAPI(title="Sistema de reservas HyD · Módulos integrados", lifespan=ciclo_de_vida)
app.include_router(auth.router)
app.include_router(hoteles.router)
# El frontend (HTML, CSS y JavaScript) se sirve desde el mismo servidor, en la raíz.
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
