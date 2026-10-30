"""Validaciones de los datos del pasajero.

Cada función revisa un campo: si está bien lo devuelve limpio y si no,
lanza ValueError con el mensaje que ve el asesor.
"""

from __future__ import annotations

import re
from datetime import date, datetime

from pasajeros.modelo import Pasajero

TIPOS_DOCUMENTO = {
    "CC": "Cédula de ciudadanía",
    "CE": "Cédula de extranjería",
    "TI": "Tarjeta de identidad",
    "PA": "Pasaporte",
}
LONGITUD_MIN_TEXTO = 2
LONGITUD_MAX_TEXTO = 50
LONGITUD_MIN_DOCUMENTO = 5
LONGITUD_MAX_DOCUMENTO = 12
LONGITUD_MIN_CELULAR = 7
LONGITUD_MAX_CELULAR = 15
LONGITUD_MAX_CORREO = 100
EDAD_MAXIMA = 120
MAYORIA_DE_EDAD = 18
FORMATO_FECHA = "%Y-%m-%d"

# Letras con tildes y ñ, espacios, apóstrofo (O'Neill) y guion.
PATRON_TEXTO = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")
PATRON_ALFANUMERICO = re.compile(r"^[A-Z0-9]+$")
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def validar_texto(valor: str, campo: str) -> str:
    """Nombre, apellido o país."""
    limpio = " ".join(valor.split())  # quita espacios de sobra
    if not limpio:
        raise ValueError(f"El campo {campo} es obligatorio.")
    if len(limpio) < LONGITUD_MIN_TEXTO:
        raise ValueError(
            f"El campo {campo} debe tener mínimo "
            f"{LONGITUD_MIN_TEXTO} caracteres."
        )
    if len(limpio) > LONGITUD_MAX_TEXTO:
        raise ValueError(
            f"El campo {campo} admite máximo {LONGITUD_MAX_TEXTO} caracteres."
        )
    if not PATRON_TEXTO.match(limpio):
        raise ValueError(
            f"El campo {campo} solo admite letras y espacios "
            "(sin números ni caracteres especiales)."
        )
    return limpio


def validar_tipo_documento(valor: str) -> str:
    limpio = valor.strip().upper()
    if limpio not in TIPOS_DOCUMENTO:
        permitidos = ", ".join(TIPOS_DOCUMENTO)
        raise ValueError(
            f"Seleccione un tipo de documento válido: {permitidos}."
        )
    return limpio


def validar_numero_documento(valor: str, tipo_documento: str) -> str:
    """CC, CE y TI solo números; el pasaporte acepta letras."""
    # La gente escribe 1.020.304.050; se guarda sin puntos.
    limpio = valor.strip().replace(".", "").replace(" ", "").upper()
    if not limpio:
        raise ValueError("El número de documento es obligatorio.")
    if not LONGITUD_MIN_DOCUMENTO <= len(limpio) <= LONGITUD_MAX_DOCUMENTO:
        raise ValueError(
            "El número de documento debe tener entre "
            f"{LONGITUD_MIN_DOCUMENTO} y {LONGITUD_MAX_DOCUMENTO} "
            "caracteres."
        )
    if tipo_documento == "PA":
        if not PATRON_ALFANUMERICO.match(limpio):
            raise ValueError("El pasaporte solo admite letras y números.")
    elif not limpio.isdigit():
        raise ValueError("Para CC, CE y TI el documento solo admite números.")
    return limpio


def validar_fecha_nacimiento(valor: str, hoy: date | None = None) -> date:
    """Convierte AAAA-MM-DD en fecha y revisa que tenga sentido."""
    hoy = hoy or date.today()
    try:
        fecha = datetime.strptime(valor.strip(), FORMATO_FECHA).date()
    except ValueError:
        # Cambio el error de Python por uno que el asesor entienda.
        raise ValueError(
            "La fecha de nacimiento debe tener el formato AAAA-MM-DD "
            "y ser una fecha real (ejemplo: 1990-04-15)."
        ) from None
    if fecha > hoy:
        raise ValueError("La fecha de nacimiento no puede ser futura.")
    if hoy.year - fecha.year > EDAD_MAXIMA:
        raise ValueError(f"La edad no puede superar {EDAD_MAXIMA} años.")
    return fecha


def validar_celular(valor: str) -> str:
    limpio = valor.strip().replace(" ", "").replace("-", "")
    if not limpio.isdigit():
        raise ValueError("El celular solo admite números.")
    if not LONGITUD_MIN_CELULAR <= len(limpio) <= LONGITUD_MAX_CELULAR:
        raise ValueError(
            f"El celular debe tener entre {LONGITUD_MIN_CELULAR} y "
            f"{LONGITUD_MAX_CELULAR} dígitos."
        )
    return limpio


def validar_correo(valor: str) -> str:
    limpio = valor.strip().lower()
    if not limpio:
        raise ValueError("El correo es obligatorio.")
    if len(limpio) > LONGITUD_MAX_CORREO:
        raise ValueError(
            f"El correo admite máximo {LONGITUD_MAX_CORREO} caracteres."
        )
    if not PATRON_CORREO.match(limpio):
        raise ValueError(
            "El correo no es válido (ejemplo: nombre@dominio.com)."
        )
    return limpio


def validar_pasajero(
    datos: dict[str, str], hoy: date | None = None
) -> Pasajero:
    """Valida todo el formulario y arma el Pasajero.

    Avisa el primer error que encuentre.
    """
    hoy = hoy or date.today()
    tipo = validar_tipo_documento(datos.get("tipo_documento", ""))
    pasajero = Pasajero(
        nombre=validar_texto(datos.get("nombre", ""), "nombre"),
        apellido=validar_texto(datos.get("apellido", ""), "apellido"),
        tipo_documento=tipo,
        numero_documento=validar_numero_documento(
            datos.get("numero_documento", ""), tipo
        ),
        fecha_nacimiento=validar_fecha_nacimiento(
            datos.get("fecha_nacimiento", ""), hoy
        ),
        pais=validar_texto(datos.get("pais", ""), "país"),
        celular=validar_celular(datos.get("celular", "")),
        correo=validar_correo(datos.get("correo", "")),
    )
    # Esta va al final porque necesita el tipo y la fecha ya revisados.
    edad = pasajero.edad(hoy)
    if tipo == "TI" and edad >= MAYORIA_DE_EDAD:
        raise ValueError(
            "La tarjeta de identidad es solo para menores de 18 años."
        )
    if tipo == "CC" and edad < MAYORIA_DE_EDAD:
        raise ValueError(
            "La cédula de ciudadanía es solo para mayores de 18 años."
        )
    return pasajero
