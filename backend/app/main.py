"""Arranque de la API.

Correr desde la carpeta backend:  uvicorn app.main:app --reload
Documentación con botones de prueba:  http://127.0.0.1:8000/docs
"""

import pymysql
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.calculos import CalculoError
from app.config import config
from app.rutas import catalogo, cotizaciones
from app.servicios import NoEncontradoError, ReglaNoCumplidaError

app = FastAPI(
    title="Cotizador Hoteles y Destinos",
    version="0.1.0",
    description="API para cotizar hoteles y actividades. Proyecto SENA "
    "ADSO, ficha 3134707.",
    openapi_tags=[
        {"name": "Sistema", "description": "Saber si la API está viva."},
        {
            "name": "Catálogo",
            "description": "Destinos, hoteles y "
            "actividades que se pueden vender.",
        },
        {
            "name": "Disponibilidad",
            "description": "Qué hoteles tienen habitación para unas fechas.",
        },
        {
            "name": "Cotizaciones",
            "description": "Calcular, guardar y "
            "hacer seguimiento a las cotizaciones.",
        },
    ],
)

# Sin esto el navegador bloquea a la página de Laura (error de CORS).
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.origenes_permitidos),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalogo.router)
app.include_router(cotizaciones.router)


# Cada error del negocio se vuelve una respuesta clara con su código HTTP.
# Los mensajes de Pydantic vienen en inglés; estos son los más comunes.
MENSAJES = {
    "missing": "es obligatorio",
    "greater_than_equal": "debe ser mayor o igual a {ge}",
    "less_than_equal": "debe ser menor o igual a {le}",
    "string_too_short": "debe tener mínimo {min_length} caracteres",
    "string_too_long": "debe tener máximo {max_length} caracteres",
    "string_pattern_mismatch": "no tiene el formato correcto",
    "int_parsing": "debe ser un número entero",
    "date_from_datetime_parsing": "debe ser una fecha AAAA-MM-DD",
    "date_parsing": "debe ser una fecha AAAA-MM-DD",
    "literal_error": "debe ser uno de: {expected}",
}


@app.exception_handler(RequestValidationError)
def _datos_invalidos(_: Request, error: RequestValidationError):
    # FastAPI manda una lista técnica; acá la vuelvo una frase legible.
    mensajes = []
    for e in error.errors():
        plantilla = MENSAJES.get(e["type"])
        texto = (
            plantilla.format(**e.get("ctx", {}))
            if plantilla
            else e["msg"].removeprefix("Value error, ")
        )
        campo = e["loc"][-1] if len(e["loc"]) > 1 else None
        mensajes.append(f"{campo}: {texto}" if campo else texto)
    return JSONResponse(
        status_code=422,
        content={
            "detail": " | ".join(mensajes),
            "errores": jsonable_encoder(error.errors()),
        },
    )


@app.exception_handler(NoEncontradoError)
def _no_encontrado(_: Request, error: NoEncontradoError):
    return JSONResponse(status_code=404, content={"detail": str(error)})


@app.exception_handler(ReglaNoCumplidaError)
def _regla(_: Request, error: ReglaNoCumplidaError):
    return JSONResponse(status_code=409, content={"detail": str(error)})


@app.exception_handler(CalculoError)
def _calculo(_: Request, error: CalculoError):
    return JSONResponse(status_code=422, content={"detail": str(error)})


@app.exception_handler(pymysql.MySQLError)
def _sin_base_de_datos(_: Request, __: pymysql.MySQLError):
    return JSONResponse(
        status_code=503,
        content={"detail": "No hay conexión con la base de datos."},
    )


@app.get("/", tags=["Sistema"], summary="Estado del servidor")
def estado():
    return {"estado": "ok", "documentacion": "/docs"}
