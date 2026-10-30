"""Reglas de validación del módulo de pasajeros y reservas.

Qué enseña: separar las validaciones en funciones pequeñas para poder probarlas una por
una. La GA7-AA3-EV02 pide documentar las pruebas de validación de fechas, números,
textos, caracteres especiales y longitudes: test_validaciones.py las prueba todas.

Cada función devuelve "" si el dato es válido o el mensaje de error si no lo es.
"""

import re
from datetime import date

LETRAS_Y_ESPACIOS = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]+$")


def validar_documento(documento: str) -> str:
    if not documento.isdigit():
        return "El documento solo admite números"
    if not 5 <= len(documento) <= 12:
        return "El documento debe tener entre 5 y 12 dígitos"
    return ""


def validar_nombre(nombre: str) -> str:
    nombre = nombre.strip()
    if not nombre:
        return "El nombre es obligatorio"
    if len(nombre) > 80:
        return "El nombre no puede tener más de 80 caracteres"
    if not LETRAS_Y_ESPACIOS.match(nombre):
        return "El nombre solo admite letras y espacios"
    return ""


def validar_edad(edad_texto: str) -> str:
    if not edad_texto.isdigit():
        return "La edad debe ser un número entero"
    if not 0 <= int(edad_texto) <= 120:
        return "La edad debe estar entre 0 y 120"
    return ""


def validar_correo(correo: str) -> str:
    if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", correo):
        return "El correo no es válido"
    return ""


def validar_fechas(entrada: date, salida: date, hoy: date | None = None) -> str:
    hoy = hoy or date.today()
    if entrada < hoy:
        return "La fecha de entrada no puede ser anterior a hoy"
    if salida <= entrada:
        return "La fecha de salida debe ser posterior a la de entrada"
    if (salida - entrada).days > 30:
        return "Una reserva no puede superar 30 noches"
    return ""
