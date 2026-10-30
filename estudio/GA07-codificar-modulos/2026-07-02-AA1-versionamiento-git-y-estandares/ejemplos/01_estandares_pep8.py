"""Estándares de codificación en Python (PEP 8) con una clase del sistema de reservas.

Qué enseña: cómo se nombran variables, constantes, clases y métodos en Python, cómo se
declara una clase con su docstring, atributos, constructor y métodos, y qué tipos de datos
básicos usamos. Es el contenido de la evidencia GA7-AA1-EV02.

Equivale en Java a: la diapositiva de estándares del instructor (clase con paquete,
comentarios, atributos privados, constructor, getters y métodos con visibilidad).

Cómo correrlo:
    python 01_estandares_pep8.py
Cómo revisar el estilo automáticamente:
    pip install ruff
    ruff check 01_estandares_pep8.py
    ruff format --check 01_estandares_pep8.py
"""

from datetime import date

# Constantes: MAYÚSCULAS_CON_GUION_BAJO (en Java: static final IVA = 0.19).
IVA = 0.19
PREFIJO_CODIGO = "HD"
# Código IATA de la ciudad para armar el código de reserva (HD + MDE + consecutivo).
CODIGOS_CIUDAD = {"Medellín": "MDE", "Cartagena": "CTG", "San Andrés": "ADZ"}


class Reserva:  # Clases: PascalCase, sustantivo en singular (igual que en Java).
    """Reserva de hotel hecha por un asesor.

    Los docstrings reemplazan al comentario /** ... */ de Java (Javadoc).
    """

    # Variable de clase: la comparten todas las reservas (en Java: static int consecutivo).
    _consecutivo = 0

    def __init__(self, ciudad: str, fecha_entrada: date, fecha_salida: date, tarifa_noche: float):
        """Constructor. En Java sería public Reserva(String ciudad, ...)."""
        if fecha_salida <= fecha_entrada:
            raise ValueError("La fecha de salida debe ser posterior a la de entrada")

        Reserva._consecutivo += 1
        # Atributos y variables: snake_case (en Java serían camelCase: fechaEntrada).
        codigo_ciudad = CODIGOS_CIUDAD.get(ciudad, ciudad[:3].upper())
        self.codigo = f"{PREFIJO_CODIGO}{codigo_ciudad}{Reserva._consecutivo:03d}"
        self.ciudad = ciudad
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.tarifa_noche = tarifa_noche
        # Un guion bajo al inicio = "privado por convención" (en Java: private).
        self._estado = "PENDIENTE"

    # Propiedad de solo lectura: reemplaza el getter de Java (getEstado()).
    @property
    def estado(self) -> str:
        return self._estado

    # Métodos: snake_case y con verbo (en Java: calcularTotal()).
    def noches(self) -> int:
        return (self.fecha_salida - self.fecha_entrada).days

    def calcular_total(self) -> float:
        """Devuelve el valor total con IVA, redondeado a pesos."""
        subtotal = self.noches() * self.tarifa_noche
        return round(subtotal * (1 + IVA))

    def confirmar(self) -> None:
        if self._estado == "CANCELADA":
            raise ValueError("Una reserva cancelada no se puede confirmar")
        self._estado = "CONFIRMADA"

    def cancelar(self) -> None:
        self._estado = "CANCELADA"

    def __str__(self) -> str:
        # Equivale a sobrescribir toString() en Java.
        return f"{self.codigo} | {self.ciudad} | {self.noches()} noches | {self.estado}"


def demo() -> None:
    # Tipos de datos básicos (la tabla de tipos que pidió el instructor).
    noches: int = 3  # entero        (Java: int)
    tarifa: float = 250_000.0  # real          (Java: double)
    ciudad: str = "Medellín"  # cadena        (Java: String)
    pagada: bool = False  # lógico        (Java: boolean)
    pasajeros: list[str] = ["Ana Ruiz", "Luis Mora"]  # lista (Java: ArrayList<String>)
    tarifas: dict[str, float] = {"Estándar": 250_000, "Suite": 480_000}  # (Java: HashMap)
    print(
        type(noches).__name__,
        type(tarifa).__name__,
        type(ciudad).__name__,
        type(pagada).__name__,
        type(pasajeros).__name__,
        type(tarifas).__name__,
    )

    reserva = Reserva(ciudad, date(2026, 12, 20), date(2026, 12, 23), tarifa)
    reserva.confirmar()
    print(reserva)
    print(f"Total con IVA: ${reserva.calcular_total():,.0f}")


# Solo corre si se ejecuta el archivo directamente (en Java: public static void main).
if __name__ == "__main__":
    demo()
