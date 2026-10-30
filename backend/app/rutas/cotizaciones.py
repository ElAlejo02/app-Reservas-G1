"""Calcular, guardar, consultar y mover de estado las cotizaciones."""

from fastapi import APIRouter, Query, status

from app import servicios
from app.esquemas import (
    CambioEstado,
    Cotizacion,
    Desglose,
    Estado,
    NuevaCotizacion,
    ResumenCotizacion,
    SolicitudCotizacion,
)
from app.repositorios import cotizaciones

router = APIRouter(prefix="/cotizaciones", tags=["Cotizaciones"])


@router.post(
    "/calcular",
    response_model=Desglose,
    summary="Calcular cotización (sin guardar)",
)
def calcular_cotizacion(solicitud: SolicitudCotizacion):
    """Para mostrar el resumen mientras el asesor arma la cotización."""
    return servicios.calcular(solicitud)


@router.post(
    "",
    response_model=Cotizacion,
    status_code=status.HTTP_201_CREATED,
    summary="Guardar cotización",
)
def guardar_cotizacion(nueva: NuevaCotizacion):
    return servicios.crear(nueva)


@router.get(
    "",
    response_model=list[ResumenCotizacion],
    summary="Ver cotizaciones (las más nuevas primero)",
)
def ver_cotizaciones(
    estado: Estado | None = None,
    limite: int = Query(default=50, ge=1, le=200),
):
    return cotizaciones.listar(estado, limite)


@router.get(
    "/{codigo}",
    response_model=Cotizacion,
    summary="Ver una cotización",
)
def ver_cotizacion(codigo: str):
    return servicios.obtener(codigo)


@router.patch(
    "/{codigo}/estado",
    response_model=Cotizacion,
    summary="Cambiar estado de una cotización",
)
def cambiar_estado(codigo: str, cambio: CambioEstado):
    """ABIERTA → ENVIADA → APROBADA o RECHAZADA. Se puede ANULAR antes de
    que el cliente responda. Aprobada, rechazada y anulada son finales.
    """
    return servicios.cambiar_estado(codigo, cambio.estado)
