"""Comunicación entre clases: asociación, agregación, composición y herencia.

Qué enseña: las cuatro relaciones de UML que el instructor pidió mostrar con ejemplos en
la evidencia GA7-AA1-EV02, escritas en Python con las clases del sistema de reservas.

Equivale en Java a: los ejemplos del componente "Aplicación del paradigma orientado a
objetos" (extends, atributos que son objetos, ArrayList de objetos).

Cómo correrlo:
    python 02_comunicacion_entre_clases.py
"""

from dataclasses import dataclass, field


# ---------- Herencia (generalización / especialización) ----------
# Persona es la clase madre; Pasajero y Usuario heredan sus datos (en Java: extends).
@dataclass
class Persona:
    nombre: str
    documento: str

    def presentarse(self) -> str:
        return f"{self.nombre} ({self.documento})"


@dataclass
class Pasajero(Persona):
    es_menor: bool = False


@dataclass
class Usuario(Persona):
    rol: str = "ASESOR"  # ADMIN, ASESOR, OPERACION o COMERCIAL

    # Polimorfismo: el mismo método se comporta distinto en la clase hija.
    def presentarse(self) -> str:
        return f"{self.rol}: {self.nombre}"


# ---------- Composición ----------
# Una Habitacion no existe sin su Hotel: el hotel la crea y, si el hotel se borra, se borran.
@dataclass
class Habitacion:
    tipo: str
    tarifa_noche: float


@dataclass
class Hotel:
    nombre: str
    ciudad: str
    habitaciones: list[Habitacion] = field(default_factory=list)

    def agregar_habitacion(self, tipo: str, tarifa: float) -> Habitacion:
        habitacion = Habitacion(tipo, tarifa)  # la crea el propio hotel
        self.habitaciones.append(habitacion)
        return habitacion


# ---------- Agregación ----------
# Un Proveedor agrupa hoteles, pero los hoteles existen por su cuenta
# (si el proveedor deja de trabajar con HyD, el hotel sigue existiendo).
@dataclass
class Proveedor:
    nombre: str
    hoteles: list[Hotel] = field(default_factory=list)

    def vincular(self, hotel: Hotel) -> None:
        self.hoteles.append(hotel)  # recibe un hotel que ya existía


# ---------- Asociación ----------
# La Reserva "conoce" a un Usuario (quien la hizo), una Habitacion y unos Pasajeros.
@dataclass
class Reserva:
    codigo: str
    asesor: Usuario
    habitacion: Habitacion
    noches: int
    pasajeros: list[Pasajero] = field(default_factory=list)

    def total(self) -> float:
        return self.noches * self.habitacion.tarifa_noche


def demo() -> None:
    hotel = Hotel("Hotel Nogal", "Medellín")
    estandar = hotel.agregar_habitacion("Estándar", 250_000)
    hotel.agregar_habitacion("Suite", 480_000)

    proveedor = Proveedor("Operador Andino")
    proveedor.vincular(hotel)

    asesor = Usuario("Sara Gómez", "1001", rol="ASESOR")
    reserva = Reserva("HDMDE001", asesor, estandar, noches=3)
    reserva.pasajeros.append(Pasajero("Ana Ruiz", "2002"))
    reserva.pasajeros.append(Pasajero("Tomás Ruiz", "2003", es_menor=True))

    print("Herencia:", [p.presentarse() for p in reserva.pasajeros], "|", asesor.presentarse())
    print("Composición:", hotel.nombre, "tiene", [h.tipo for h in hotel.habitaciones])
    print("Agregación:", proveedor.nombre, "trabaja con", [h.nombre for h in proveedor.hoteles])
    print(
        "Asociación:",
        reserva.codigo,
        "hecha por",
        reserva.asesor.nombre,
        f"| total ${reserva.total():,.0f}",
    )


if __name__ == "__main__":
    demo()
