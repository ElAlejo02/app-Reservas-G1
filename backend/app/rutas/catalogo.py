"""Destinos, hoteles, actividades y búsqueda de disponibilidad."""

from fastapi import APIRouter, Query

from app import servicios
from app.esquemas import Actividad, Busqueda, Destino, Hotel, OpcionHotel
from app.repositorios import catalogo

router = APIRouter()
FiltroDestino = Query(
    default=None, min_length=3, max_length=3, description="Ej: CTG"
)


@router.get(
    "/destinos",
    response_model=list[Destino],
    tags=["Catálogo"],
    summary="Ver destinos",
)
def ver_destinos():
    return catalogo.listar_destinos()


@router.get(
    "/hoteles",
    response_model=list[Hotel],
    tags=["Catálogo"],
    summary="Ver hoteles",
)
def ver_hoteles(destino: str | None = FiltroDestino):
    return catalogo.listar_hoteles(destino.upper() if destino else None)


@router.get(
    "/actividades",
    response_model=list[Actividad],
    tags=["Catálogo"],
    summary="Ver actividades con precio de venta",
)
def ver_actividades(destino: str | None = FiltroDestino):
    return servicios.actividades_con_precio(
        destino.upper() if destino else None
    )


@router.post(
    "/disponibilidad",
    response_model=list[OpcionHotel],
    tags=["Disponibilidad"],
    summary="Buscar hoteles disponibles",
)
def buscar_hoteles_disponibles(busqueda: Busqueda):
    """Hoteles con habitación para esas fechas y personas, del más barato
    al más caro. El `id_tarifa` de la opción elegida se usa para cotizar.
    """
    return servicios.buscar_disponibilidad(busqueda)
