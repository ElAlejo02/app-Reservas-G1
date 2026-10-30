"""Reglas de validación de los datos de un pasajero.

Validar es revisar que un dato tenga sentido ANTES de guardarlo. Si el
asesor escribe letras en el celular o una fecha imposible, el programa
debe avisar con un mensaje claro y no dañar la base de datos.

Diseño de este módulo:

* Cada función valida UN campo. Así se puede probar cada regla por
  separado (lo exige la evidencia GA7-AA3-EV02).
* Si el dato es correcto, la función lo devuelve "limpio" (sin espacios
  sobrantes, en el tipo correcto, etc.).
* Si el dato es incorrecto, la función lanza ``ValueError`` con un
  mensaje pensado para el usuario final. La interfaz atrapa ese error
  con ``try/except`` y lo muestra en una ventana, igual que
  ``JOptionPane`` en Java.
"""

from __future__ import annotations

import re  # Expresiones regulares: patrones para revisar textos.
from datetime import date, datetime

from pasajeros.modelo import Pasajero

# --- Constantes -----------------------------------------------------------
# PEP 8: las constantes se escriben en MAYÚSCULAS_CON_GUION_BAJO y van
# al inicio del módulo. Si mañana cambia una regla, se cambia aquí y no
# hay que buscarla por todo el código.

# Diccionario: llave = código que se guarda, valor = nombre legible.
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
FORMATO_FECHA = "%Y-%m-%d"  # AAAA-MM-DD, el mismo formato de MySQL.

# re.compile() "prepara" un patrón una sola vez para reusarlo rápido.
# Cómo leer este patrón:
#   ^ ... $        -> el texto COMPLETO debe cumplir, de inicio a fin.
#   [ ... ]        -> cualquiera de estos caracteres.
#   A-Za-z         -> letras sin tilde.
#   ÁÉÍÓÚÜÑáéíóúüñ -> letras del español.
#   ' y -          -> apóstrofo (O'Neill) y guion (Ruiz-Gómez).
#   (espacio)      -> para nombres compuestos.
#   +              -> uno o más de esos caracteres.
PATRON_TEXTO = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")
# Pasaporte: letras y números, sin espacios ni símbolos.
PATRON_ALFANUMERICO = re.compile(r"^[A-Z0-9]+$")
# Correo simple: algo@algo.algo
#   [\w.+-]+   -> usuario: letras, números, _, punto, + o -.
#   @          -> la arroba obligatoria.
#   [\w-]+     -> dominio (gmail, hotelesydestinos...).
#   (\.[\w-]+)+ -> uno o más ".com", ".co", ".edu.co"...
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


# --- Funciones de validación por campo ------------------------------------
def validar_texto(valor: str, campo: str) -> str:
    """Valida nombre, apellido o país.

    Args:
        valor: Texto escrito por el usuario.
        campo: Nombre del campo, solo para armar el mensaje de error.

    Returns:
        El texto sin espacios sobrantes.

    Raises:
        ValueError: si está vacío, es muy corto o muy largo, o tiene
            números o caracteres especiales.
    """
    # " ".join(valor.split()) quita espacios al inicio y al final y
    # convierte varios espacios seguidos en uno solo:
    # "  Ana   María " -> "Ana María".
    limpio = " ".join(valor.split())
    if not limpio:  # Un texto vacío "" se evalúa como False.
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
    # .match() devuelve None si el texto NO cumple el patrón.
    if not PATRON_TEXTO.match(limpio):
        raise ValueError(
            f"El campo {campo} solo admite letras y espacios "
            "(sin números ni caracteres especiales)."
        )
    return limpio


def validar_tipo_documento(valor: str) -> str:
    """Valida que el tipo de documento sea uno de los permitidos.

    Raises:
        ValueError: si el tipo no está en ``TIPOS_DOCUMENTO``.
    """
    limpio = valor.strip().upper()
    # "in" sobre un diccionario busca entre sus llaves.
    if limpio not in TIPOS_DOCUMENTO:
        # ", ".join(...) une las llaves con coma: "CC, CE, TI, PA".
        permitidos = ", ".join(TIPOS_DOCUMENTO)
        raise ValueError(
            f"Seleccione un tipo de documento válido: {permitidos}."
        )
    return limpio


def validar_numero_documento(valor: str, tipo_documento: str) -> str:
    """Valida el número de documento según su tipo.

    Regla de negocio: CC, CE y TI solo llevan dígitos. El pasaporte
    (PA) puede llevar letras y números.

    Raises:
        ValueError: si está vacío, tiene una longitud fuera de rango o
            caracteres no permitidos para su tipo.
    """
    # Quitamos espacios y puntos que la gente suele escribir:
    # "1.020.304.050" -> "1020304050".
    limpio = valor.strip().replace(".", "").replace(" ", "").upper()
    if not limpio:
        raise ValueError("El número de documento es obligatorio.")
    # Comparación encadenada: equivale a (5 <= n) and (n <= 12).
    if not LONGITUD_MIN_DOCUMENTO <= len(limpio) <= LONGITUD_MAX_DOCUMENTO:
        raise ValueError(
            "El número de documento debe tener entre "
            f"{LONGITUD_MIN_DOCUMENTO} y {LONGITUD_MAX_DOCUMENTO} "
            "caracteres."
        )
    if tipo_documento == "PA":
        if not PATRON_ALFANUMERICO.match(limpio):
            raise ValueError("El pasaporte solo admite letras y números.")
    # .isdigit() es True solo si TODOS los caracteres son dígitos.
    elif not limpio.isdigit():
        raise ValueError("Para CC, CE y TI el documento solo admite números.")
    return limpio


def validar_fecha_nacimiento(valor: str, hoy: date | None = None) -> date:
    """Convierte el texto AAAA-MM-DD en fecha y revisa que sea lógica.

    Args:
        valor: Fecha escrita por el usuario, por ejemplo "1990-04-15".
        hoy: Fecha de referencia (se recibe para poder probar).

    Returns:
        Un objeto ``date`` listo para guardar en MySQL.

    Raises:
        ValueError: si el formato es incorrecto, la fecha no existe
            (31 de febrero), es futura o da una edad mayor a 120 años.
    """
    hoy = hoy or date.today()
    try:
        # strptime = "string parse time": convierte texto en fecha
        # siguiendo el formato indicado. .date() se queda solo con la
        # fecha (sin hora). Si el texto no cumple o la fecha no existe,
        # Python lanza ValueError.
        fecha = datetime.strptime(valor.strip(), FORMATO_FECHA).date()
    except ValueError:
        # Atrapamos el error técnico de Python y lanzamos uno nuevo con
        # un mensaje que el asesor entienda. "from None" oculta el error
        # original para que el mensaje quede limpio.
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
    """Valida un celular nacional o internacional (solo dígitos).

    Raises:
        ValueError: si tiene letras o símbolos, o longitud inválida.
    """
    # Se aceptan espacios y guiones al escribir ("300 111-2233") pero
    # se guardan solo los dígitos.
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
    """Valida el formato del correo y lo guarda en minúsculas.

    Raises:
        ValueError: si está vacío, es muy largo o no tiene formato
            usuario@dominio.ext.
    """
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


# --- Validación del formulario completo -----------------------------------
def validar_pasajero(
    datos: dict[str, str], hoy: date | None = None
) -> Pasajero:
    """Valida todos los campos y arma un objeto ``Pasajero``.

    Es la única función que llama la interfaz: recibe lo que el usuario
    escribió (todo llega como texto) y devuelve un ``Pasajero`` limpio.

    Args:
        datos: Diccionario con las llaves nombre, apellido,
            tipo_documento, numero_documento, fecha_nacimiento, pais,
            celular y correo.
        hoy: Fecha de referencia para las reglas de edad.

    Returns:
        Un ``Pasajero`` con todos sus datos validados.

    Raises:
        ValueError: con el mensaje del PRIMER campo que falle.
    """
    hoy = hoy or date.today()
    # .get(llave, "") devuelve "" si la llave no existe, en vez de
    # lanzar un KeyError. Así un campo faltante se trata como vacío.
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
    # Regla que cruza dos campos (por eso va al final): la tarjeta de
    # identidad es para menores de edad y la cédula para mayores.
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
