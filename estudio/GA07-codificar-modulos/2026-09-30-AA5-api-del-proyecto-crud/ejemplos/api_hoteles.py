"""API del proyecto: CRUD de hoteles con los cuatro verbos HTTP (GA7-AA5-EV03).

Qué enseña: lo que la instructora hizo con ProductoDTO y ProductoController en Spring Boot,
pero con el recurso "hoteles" del sistema de reservas:
    GET    /api/hoteles          listar           -> 200
    GET    /api/hoteles/{id}     consultar uno     -> 200 o 404
    POST   /api/hoteles          crear            -> 201
    PUT    /api/hoteles/{id}     actualizar        -> 200 o 404
    DELETE /api/hoteles/{id}     eliminar          -> 200 o 404

Equivalencias con la clase:
    ProductoDTO (id long, nombre, precio)       -> class HotelDTO(BaseModel)
    @RequestMapping("/api/productos")           -> APIRouter(prefix="/api/hoteles")
    static List<ProductoDTO> + bloque static    -> lista "hoteles" con dos datos iniciales
    @GetMapping / @PostMapping / @PutMapping    -> @router.get / .post / .put / .delete
    @PathVariable Long id                       -> parámetro id en la ruta
    @RequestBody ProductoDTO                    -> parámetro datos: HotelDTO
    removeIf(p -> p.getId() == id)              -> lista por comprensión sin ese id

Como en clase, los datos viven en memoria ("simulador de persistencia"): al reiniciar el
servidor vuelven los dos hoteles iniciales. Para usar MySQL se cambia la lista por las
funciones de SQLAlchemy de la clase del 2026-09-03.

Cómo correrlo:
    pip install "fastapi<0.145" uvicorn
    uvicorn api_hoteles:app --reload --port 8080
    Documentación: http://127.0.0.1:8080/docs
"""

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API del proyecto · Hoteles · Reservas HyD")


class HotelDTO(BaseModel):
    """Lo que el cliente envía para crear o actualizar un hotel."""

    nombre: str = Field(min_length=2, max_length=80)
    ciudad: str = Field(min_length=2, max_length=40)
    estrellas: int = Field(ge=1, le=5)
    tarifa_noche: float = Field(gt=0)


class Hotel(HotelDTO):
    """Lo que la API devuelve: los mismos datos más el id."""

    id: int


# Simulador de persistencia: dos datos iniciales para probar (el bloque static de la clase).
hoteles: list[Hotel] = [
    Hotel(id=1, nombre="Hotel Nogal", ciudad="Medellín", estrellas=4, tarifa_noche=250_000),
    Hotel(id=2, nombre="Hotel Bahía", ciudad="Cartagena", estrellas=5, tarifa_noche=480_000),
]

router = APIRouter(prefix="/api/hoteles", tags=["Hoteles"])


def buscar(hotel_id: int) -> Hotel:
    for hotel in hoteles:
        if hotel.id == hotel_id:
            return hotel
    raise HTTPException(404, f"Hotel {hotel_id} no encontrado")


@router.get("")
def listar(ciudad: str | None = None) -> list[Hotel]:
    """GET: lista todos, o solo los de una ciudad con ?ciudad=Medellín."""
    if ciudad:
        return [h for h in hoteles if h.ciudad.lower() == ciudad.lower()]
    return hoteles


@router.get("/{hotel_id}")
def consultar(hotel_id: int) -> Hotel:
    return buscar(hotel_id)


@router.post("", status_code=201)
def crear(datos: HotelDTO) -> Hotel:
    """POST: el id lo asigna el servidor, no el cliente."""
    nuevo_id = max((h.id for h in hoteles), default=0) + 1
    hotel = Hotel(id=nuevo_id, **datos.model_dump())
    hoteles.append(hotel)
    return hotel


@router.put("/{hotel_id}")
def actualizar(hotel_id: int, datos: HotelDTO) -> Hotel:
    hotel = buscar(hotel_id)  # 404 si no existe
    for campo, valor in datos.model_dump().items():
        setattr(hotel, campo, valor)  # el "setter" de cada campo
    return hotel


@router.delete("/{hotel_id}")
def eliminar(hotel_id: int) -> dict:
    hotel = buscar(hotel_id)
    hoteles.remove(hotel)
    return {"mensaje": f"Hotel {hotel_id} eliminado"}


app.include_router(router)
