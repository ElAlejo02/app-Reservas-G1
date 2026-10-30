"""Forma de los datos que entran y salen de la API.

Pydantic revisa cada pedido antes de que llegue a la lógica. Si algo no
cuadra, FastAPI responde 422 con el detalle y no hay que validar a mano.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

Estado = Literal["ABIERTA", "ENVIADA", "APROBADA", "RECHAZADA", "ANULADA"]


# ---------------------------------------------------------------- catálogo
class Destino(BaseModel):
    codigo: str = Field(examples=["CTG"])
    nombre: str = Field(examples=["Cartagena"])
    exento_iva: bool
    tasa_por_persona: int


class Hotel(BaseModel):
    id_hotel: int
    nombre: str
    destino_codigo: str
    estrellas: int


class Actividad(BaseModel):
    id_actividad: int
    nombre: str
    destino_codigo: str
    descripcion: str
    precio_adulto: int = Field(description="Precio de venta, ya con margen.")
    precio_nino: int


# ----------------------------------------------------------- disponibilidad
class Busqueda(BaseModel):
    destino: str = Field(min_length=3, max_length=3, examples=["CTG"])
    fecha_entrada: date = Field(examples=["2027-02-10"])
    fecha_salida: date = Field(examples=["2027-02-14"])
    adultos: int = Field(ge=1, le=10, examples=[2])
    ninos: int = Field(default=0, ge=0, le=10, examples=[1])

    @model_validator(mode="after")
    def revisar_fechas(self) -> Busqueda:
        self.destino = self.destino.upper()
        if self.fecha_salida <= self.fecha_entrada:
            raise ValueError("La salida debe ser después de la entrada.")
        if self.fecha_entrada < date.today():
            raise ValueError("La entrada no puede ser en el pasado.")
        return self


class OpcionHotel(BaseModel):
    id_tarifa: int = Field(description="Se manda en la cotización.")
    id_hotel: int
    hotel: str
    estrellas: int
    tipo_habitacion: str
    temporada: str
    noches: int
    precio_estadia: int = Field(description="Total del hotel con margen.")


# ------------------------------------------------------------- cotización
class ActividadPedida(BaseModel):
    id_actividad: int
    adultos: int = Field(ge=0, le=10)
    ninos: int = Field(default=0, ge=0, le=10)


class SolicitudCotizacion(Busqueda):
    id_tarifa: int = Field(examples=[11])
    actividades: list[ActividadPedida] = Field(default_factory=list)
    descuento_porcentaje: int = Field(default=0, ge=0, examples=[5])


class NuevaCotizacion(SolicitudCotizacion):
    cliente_nombre: str = Field(
        min_length=3, max_length=100, examples=["Agencia Viajes del Sol"]
    )
    cliente_correo: str = Field(
        max_length=100,
        pattern=r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$",
        examples=["ventas@viajesdelsol.com"],
    )


class LineaActividad(BaseModel):
    id_actividad: int
    nombre: str
    adultos: int
    ninos: int
    precio: int


class Desglose(BaseModel):
    """Todo ya calculado: el frontend solo lo pinta."""

    destino: str
    hotel: str
    tipo_habitacion: str
    temporada: str
    noches: int
    precio_hotel: int
    actividades: list[LineaActividad]
    precio_actividades: int
    subtotal: int
    descuento_porcentaje: int
    descuento: int
    iva_porcentaje: int
    iva: int
    tasas: int
    total: int


class Cotizacion(BaseModel):
    codigo: str = Field(examples=["COT-000001"])
    estado: Estado
    cliente_nombre: str
    cliente_correo: str
    destino_codigo: str
    fecha_entrada: date
    fecha_salida: date
    adultos: int
    ninos: int
    fecha_creacion: datetime
    desglose: Desglose


class ResumenCotizacion(BaseModel):
    codigo: str
    estado: Estado
    cliente_nombre: str
    destino_codigo: str
    fecha_entrada: date
    total: int
    fecha_creacion: datetime


class CambioEstado(BaseModel):
    estado: Estado = Field(examples=["ENVIADA"])
