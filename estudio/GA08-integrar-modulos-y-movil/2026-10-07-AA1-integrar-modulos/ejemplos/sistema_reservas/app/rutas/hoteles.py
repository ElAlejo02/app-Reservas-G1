"""Módulo de hoteles: el CRUD de la GA7-AA5 pero ahora sobre la base de datos.

En clase se cambió la lista "static" de ProductoController por sentencias SQL dentro de
try-catch. Aquí se cambia la lista en memoria por consultas de SQLAlchemy.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import obtener_sesion
from app.esquemas import HotelDTO, HotelSalida
from app.modelos import Hotel

router = APIRouter(prefix="/api/hoteles", tags=["Hoteles"])


def buscar(sesion: Session, hotel_id: int) -> Hotel:
    hotel = sesion.get(Hotel, hotel_id)
    if hotel is None:
        raise HTTPException(404, f"Hotel {hotel_id} no encontrado")
    return hotel


@router.get("", response_model=list[HotelSalida])
def listar(sesion: Session = Depends(obtener_sesion)):
    return sesion.scalars(select(Hotel).order_by(Hotel.nombre)).all()


@router.post("", status_code=201, response_model=HotelSalida)
def crear(datos: HotelDTO, sesion: Session = Depends(obtener_sesion)):
    hotel = Hotel(**datos.model_dump())
    sesion.add(hotel)
    sesion.commit()
    sesion.refresh(hotel)  # trae el id autoincremental que asignó la base de datos
    return hotel


@router.put("/{hotel_id}", response_model=HotelSalida)
def actualizar(hotel_id: int, datos: HotelDTO, sesion: Session = Depends(obtener_sesion)):
    hotel = buscar(sesion, hotel_id)
    for campo, valor in datos.model_dump().items():
        setattr(hotel, campo, valor)
    sesion.commit()
    sesion.refresh(hotel)
    return hotel


@router.delete("/{hotel_id}")
def eliminar(hotel_id: int, sesion: Session = Depends(obtener_sesion)) -> dict:
    sesion.delete(buscar(sesion, hotel_id))
    sesion.commit()
    return {"mensaje": f"Hotel {hotel_id} eliminado"}
