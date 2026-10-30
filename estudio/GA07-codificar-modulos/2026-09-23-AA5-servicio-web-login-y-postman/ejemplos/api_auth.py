"""Servicio web (API REST) de registro e inicio de sesión con FastAPI.

Qué enseña: la evidencia GA7-AA5-EV01 que la instructora hizo con Spring Boot:
un DTO que recibe usuario y contraseña en JSON, un controlador con la lógica de
autenticación y respuestas HTTP estándar (200 si es correcto, 401 si no).

Equivalencias con la clase (Java + Spring Boot):
    UsuarioDTO.java (usuario, contraseña, getters/setters) -> class UsuarioDTO(BaseModel)
    @RestController + @RequestMapping("/api/auth")         -> APIRouter(prefix="/api/auth")
    @CrossOrigin                                           -> CORSMiddleware
    @PostMapping("/login") + @RequestBody UsuarioDTO       -> @router.post("/login")
    ResponseEntity.ok(...) / status(401)                   -> return {...} / HTTPException(401)

Mejora frente al ejemplo de clase: allá el usuario era fijo (admin / 1234). Aquí el
registro guarda la contraseña con hash bcrypt, nunca en texto plano.

Cómo correrlo:
    pip install "fastapi<0.145" uvicorn bcrypt
    uvicorn api_auth:app --reload --port 8080
    Documentación y pruebas en el navegador: http://127.0.0.1:8080/docs
"""

import bcrypt
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Servicio de autenticación · Reservas HyD")

# Permite que el formulario servido en otro puerto (8081) consuma la API (arquitectura desacoplada).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://127.0.0.1:8081"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class UsuarioDTO(BaseModel):
    """DTO: la "bandeja" con solo los datos necesarios para autenticarse."""

    usuario: str = Field(min_length=3, max_length=30)
    contrasena: str = Field(min_length=4, max_length=64)


# "Base de datos" en memoria: usuario -> hash de la contraseña. Usuario de prueba: admin / 1234
usuarios: dict[str, bytes] = {"admin": bcrypt.hashpw(b"1234", bcrypt.gensalt())}

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/registro", status_code=201)
def registrar(datos: UsuarioDTO) -> dict:
    """Registra un usuario nuevo. 409 si ya existe."""
    if datos.usuario in usuarios:
        raise HTTPException(409, "El usuario ya existe")
    usuarios[datos.usuario] = bcrypt.hashpw(datos.contrasena.encode(), bcrypt.gensalt())
    return {"mensaje": f"Usuario {datos.usuario} registrado"}


@router.post("/login")
def iniciar_sesion(datos: UsuarioDTO) -> dict:
    """200 si las credenciales son correctas; 401 si no."""
    guardado = usuarios.get(datos.usuario)
    if guardado is None or not bcrypt.checkpw(datos.contrasena.encode(), guardado):
        # El mismo mensaje para usuario inexistente o clave errada: no dar pistas a un atacante.
        raise HTTPException(401, "Error de autenticación: usuario o contraseña incorrectos")
    return {"mensaje": "Autenticación exitosa", "usuario": datos.usuario}


app.include_router(router)
