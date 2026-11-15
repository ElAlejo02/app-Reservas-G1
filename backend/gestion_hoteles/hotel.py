"""Clase Hotel: una fila de la tabla hoteles."""

from dataclasses import dataclass

ESTRELLAS_MINIMAS = 1
ESTRELLAS_MAXIMAS = 5


@dataclass
class Hotel:
    """Hotel del catálogo de Hoteles y Destinos."""

    nombre: str
    destino_codigo: str
    estrellas: int
    id_hotel: int | None = None  # lo asigna MySQL al insertar

    def validar(self) -> None:
        """Revisa los datos antes de mandarlos a la base."""
        self.nombre = self.nombre.strip()
        self.destino_codigo = self.destino_codigo.strip().upper()
        if not self.nombre:
            raise ValueError("el nombre no puede quedar vacío.")
        if len(self.destino_codigo) != 3:
            raise ValueError("el destino es un código de 3 letras (CTG).")
        if not ESTRELLAS_MINIMAS <= self.estrellas <= ESTRELLAS_MAXIMAS:
            raise ValueError("las estrellas van de 1 a 5.")
