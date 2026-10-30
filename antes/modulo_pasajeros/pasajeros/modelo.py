"""La clase Pasajero: una fila de la tabla pasajeros."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Pasajero:
    nombre: str
    apellido: str
    tipo_documento: str  # CC, CE, TI o PA
    numero_documento: str
    fecha_nacimiento: date
    pais: str
    celular: str
    correo: str
    id_pasajero: int | None = None  # None hasta que se guarda en MySQL

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def edad(self, hoy: date | None = None) -> int:
        """Años cumplidos. `hoy` se puede pasar para probar con fecha fija."""
        hoy = hoy or date.today()
        anios = hoy.year - self.fecha_nacimiento.year
        cumplio = (hoy.month, hoy.day) >= (
            self.fecha_nacimiento.month,
            self.fecha_nacimiento.day,
        )
        return anios - (not cumplio)

    def __str__(self) -> str:
        return (
            f"{self.nombre_completo()} "
            f"({self.tipo_documento} {self.numero_documento})"
        )
