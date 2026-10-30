"""Pruebas automáticas de las validaciones (insumo para la GA7-AA3-EV02).

Qué enseña: pytest, la herramienta de pruebas de Python (en Java sería JUnit).
Cada fila de las tablas es un caso de prueba: dato de entrada y resultado esperado.
Esas mismas filas se copian al Word de la evidencia como "pruebas de validación".

Cómo correrlo:
    pip install pytest
    pytest -v test_validaciones.py
"""

from datetime import date

import pytest

from validaciones import (
    validar_correo,
    validar_documento,
    validar_edad,
    validar_fechas,
    validar_nombre,
)

HOY = date(2026, 9, 10)


@pytest.mark.parametrize(
    ("documento", "valido"),
    [
        ("1020304050", True),  # caso normal
        ("12345", True),  # longitud mínima
        ("1234", False),  # muy corto
        ("1234567890123", False),  # muy largo
        ("10203A", False),  # letras
        ("10.203.040", False),  # caracteres especiales
        ("", False),  # vacío
    ],
)
def test_documento(documento, valido):
    assert (validar_documento(documento) == "") is valido


@pytest.mark.parametrize(
    ("nombre", "valido"),
    [
        ("Ana Ruiz", True),
        ("José Ñáñez O'Neil", True),  # tildes, eñe y apóstrofo
        ("   ", False),  # solo espacios
        ("Ana123", False),  # números
        ("Ana@Ruiz", False),  # caracteres especiales
        ("A" * 81, False),  # longitud máxima superada
    ],
)
def test_nombre(nombre, valido):
    assert (validar_nombre(nombre) == "") is valido


@pytest.mark.parametrize(
    ("edad", "valido"),
    [("0", True), ("34", True), ("120", True), ("121", False), ("-5", False), ("treinta", False)],
)
def test_edad(edad, valido):
    assert (validar_edad(edad) == "") is valido


@pytest.mark.parametrize(
    ("correo", "valido"),
    [
        ("ana@correo.com", True),
        ("ana.ruiz@hyd.com.co", True),
        ("ana@", False),
        ("anacorreo.com", False),
    ],
)
def test_correo(correo, valido):
    assert (validar_correo(correo) == "") is valido


@pytest.mark.parametrize(
    ("entrada", "salida", "valido"),
    [
        (date(2026, 9, 20), date(2026, 9, 23), True),  # 3 noches
        (date(2026, 9, 1), date(2026, 9, 3), False),  # entrada en el pasado
        (date(2026, 9, 20), date(2026, 9, 20), False),  # mismo día
        (date(2026, 9, 20), date(2026, 9, 18), False),  # salida antes que entrada
        (date(2026, 9, 20), date(2026, 11, 1), False),  # más de 30 noches
    ],
)
def test_fechas(entrada, salida, valido):
    assert (validar_fechas(entrada, salida, hoy=HOY) == "") is valido
