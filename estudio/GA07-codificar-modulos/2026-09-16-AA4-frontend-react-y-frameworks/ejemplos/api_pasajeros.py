"""Backend del registro de pasajeros con FastAPI (lo que en clase se hizo con Spring Boot).

Qué enseña: qué hace un framework de backend. Igual que el proyecto de start.spring.io
(Maven + Spring Web) levanta un servidor local en el puerto 8080, FastAPI + Uvicorn levanta
uno en el 8000, y el frontend en React (carpeta frontend-react) le envía y pide datos.

Equivalencias:
    start.spring.io + Spring Web        -> pip install fastapi uvicorn
    @RestController / @GetMapping       -> @app.get("/api/...")
    @PostMapping + @RequestBody         -> @app.post("/api/...") con un modelo Pydantic
    Puerto 8080 de Tomcat embebido      -> puerto 8000 de Uvicorn
    Hibernate (mapear tablas a clases)  -> SQLAlchemy (ver la clase del 2026-09-03)

Aquí los pasajeros se guardan en una lista en memoria para que el ejemplo sea corto.

Cómo correrlo:
    pip install "fastapi<0.145" uvicorn
    uvicorn api_pasajeros:app --reload --port 8000
    Abrir http://127.0.0.1:8000/docs para ver y probar la API (documentación automática).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="API de pasajeros · Reservas HyD")

# CORS: permite que el frontend de Vite (puerto 5173) llame a esta API (puerto 8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pasajero(BaseModel):
    """Pydantic valida los datos que llegan; si algo no cumple, responde 422 solo."""

    documento: str = Field(pattern=r"^\d{5,12}$")
    nombre: str = Field(min_length=2, max_length=80)
    edad: int = Field(ge=0, le=120)
    genero: str = Field(pattern="^(Masculino|Femenino|Otro)$")


pasajeros: list[Pasajero] = [
    Pasajero(documento="900001", nombre="Ana Ruiz", edad=34, genero="Femenino")
]


@app.get("/api/estado")
def estado() -> dict:
    return {"mensaje": "Conectado con éxito al servidor local"}


@app.get("/api/pasajeros")
def listar() -> list[Pasajero]:
    return pasajeros


@app.post("/api/pasajeros", status_code=201)
def crear(pasajero: Pasajero) -> Pasajero:
    if any(p.documento == pasajero.documento for p in pasajeros):
        raise HTTPException(409, f"Ya existe un pasajero con documento {pasajero.documento}")
    pasajeros.append(pasajero)
    return pasajero


@app.delete("/api/pasajeros/{documento}", status_code=204)
def eliminar(documento: str) -> None:
    for p in pasajeros:
        if p.documento == documento:
            pasajeros.remove(p)
            return
    raise HTTPException(404, "No existe ese documento")
