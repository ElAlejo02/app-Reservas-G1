"""Modelo de datos: la clase ``Pasajero``.

El "modelo" representa una cosa del mundo real del negocio. Aquí, un
pasajero que viaja con Hoteles y Destinos. Cada objeto ``Pasajero``
corresponde a UNA fila de la tabla ``pasajeros`` en MySQL.

En Java esto sería la clase ``Persona`` con atributos privados,
constructor, getters y setters. En Python, ``@dataclass`` escribe
automáticamente el constructor y otros métodos por nosotros.
"""

# "annotations" permite usar tipos como "int | None" sin problemas en
# cualquier versión de Python 3.
from __future__ import annotations

from dataclasses import dataclass  # Genera el constructor automático.
from datetime import date  # Tipo de dato para fechas reales.


# @dataclass es un "decorador": una etiqueta que modifica la clase.
# Le dice a Python: "créame el __init__ (constructor), el __repr__
# (cómo se imprime) y el __eq__ (cómo se comparan dos objetos)
# a partir de los atributos que declaro abajo".
@dataclass
class Pasajero:
    """Pasajero de una reserva de Hoteles y Destinos.

    Attributes:
        nombre: Nombre(s) del pasajero.
        apellido: Apellido(s) del pasajero.
        tipo_documento: CC, CE, TI o PA.
        numero_documento: Número de identificación (único).
        fecha_nacimiento: Fecha de nacimiento como objeto ``date``.
        pais: País de residencia.
        celular: Número de celular solo con dígitos.
        correo: Correo electrónico de contacto.
        id_pasajero: Llave primaria que asigna MySQL. Vale ``None``
            mientras el pasajero no se haya guardado.
    """

    # --- Atributos (equivalen a "private String nombre;" en Java) ---
    # La sintaxis es: nombre_atributo: tipo
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    fecha_nacimiento: date
    pais: str
    celular: str
    correo: str
    # Este va al final porque tiene valor por defecto. Regla de Python:
    # los atributos con valor por defecto van después de los que no.
    id_pasajero: int | None = None

    # --- Métodos propios del negocio ---------------------------------
    def nombre_completo(self) -> str:
        """Devuelve nombre y apellido juntos, listo para mostrar."""
        # f-string: la f antes de las comillas permite meter variables
        # dentro de {llaves}.
        return f"{self.nombre} {self.apellido}"

    def edad(self, hoy: date | None = None) -> int:
        """Calcula la edad en años cumplidos.

        Args:
            hoy: Fecha de referencia. Si no se envía, se usa la fecha
                de hoy. Recibirla como parámetro permite probar el
                método con una fecha fija.

        Returns:
            La edad en años cumplidos.
        """
        # "x or y" devuelve x si x tiene valor; si x es None, devuelve y.
        hoy = hoy or date.today()
        # PEP 8 recomienda nombres de variables solo con letras ASCII,
        # por eso escribimos "anios" y no "años".
        anios = hoy.year - self.fecha_nacimiento.year
        # Si este año todavía no ha cumplido años, se resta uno.
        # Comparar tuplas (mes, día) compara primero el mes y, si es
        # igual, el día. Un True vale 1 y un False vale 0 al restar.
        cumplio = (hoy.month, hoy.day) >= (
            self.fecha_nacimiento.month,
            self.fecha_nacimiento.day,
        )
        return anios - (not cumplio)

    def __str__(self) -> str:
        """Texto que se muestra al hacer ``print(pasajero)``."""
        return (
            f"{self.nombre_completo()} "
            f"({self.tipo_documento} {self.numero_documento})"
        )
