"""DTOs: los datos que entran y salen de la API (UsuarioDTO y ProductoDTO de la clase)."""

from pydantic import BaseModel, ConfigDict, Field


class CredencialesDTO(BaseModel):
    usuario: str = Field(min_length=3, max_length=30)
    contrasena: str = Field(min_length=4, max_length=64)


class HotelDTO(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    ciudad: str = Field(min_length=2, max_length=40)
    estrellas: int = Field(ge=1, le=5)
    tarifa_noche: float = Field(gt=0)


class HotelSalida(HotelDTO):
    # from_attributes permite convertir directamente un objeto de la base de datos al DTO.
    model_config = ConfigDict(from_attributes=True)
    id: int
