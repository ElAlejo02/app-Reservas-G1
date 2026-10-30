"""Pruebas unitarias de las reglas de validación (GA7-AA3-EV02).

Una prueba unitaria revisa UNA regla de forma automática: le da un dato
al código y compara el resultado con lo esperado. Se usa ``unittest``,
que viene con Python (es el equivalente a JUnit en Java).

Ejecutar desde la carpeta ``modulo_pasajeros``::

    python -m unittest -v

Las pruebas están agrupadas por el tipo de validación que pide la guía:
textos, caracteres especiales, longitudes, números, fechas y correo.
"""

import unittest
from datetime import date

from pasajeros import validaciones as v

# Fecha fija para que las pruebas den siempre el mismo resultado, sin
# importar el día en que se ejecuten.
HOY = date(2026, 10, 28)


def datos_validos(**cambios: str) -> dict[str, str]:
    """Devuelve un formulario correcto, cambiando solo lo indicado.

    Ejemplo: ``datos_validos(correo="malo")`` arma un formulario
    perfecto excepto el correo. Así cada prueba cambia UN solo campo.
    """
    datos = {
        "nombre": "Ana María",
        "apellido": "Ruiz Gómez",
        "tipo_documento": "CC",
        "numero_documento": "1020304050",
        "fecha_nacimiento": "1990-04-15",
        "pais": "Colombia",
        "celular": "3001112233",
        "correo": "ana.ruiz@ejemplo.com",
    }
    datos.update(cambios)  # Sobrescribe solo las llaves enviadas.
    return datos


class PruebasTextos(unittest.TestCase):
    """Validaciones de textos: obligatorio, letras y longitudes."""

    def test_texto_valido_se_limpia(self):
        # assertEqual(a, b) falla si a y b son distintos.
        self.assertEqual(
            v.validar_texto("  Ana   María ", "nombre"), "Ana María"
        )

    def test_texto_con_tildes_y_enie_es_valido(self):
        self.assertEqual(
            v.validar_texto("Muñoz Peña", "apellido"), "Muñoz Peña"
        )

    def test_texto_vacio_es_rechazado(self):
        # assertRaises verifica que el bloque LANCE el error esperado.
        with self.assertRaises(ValueError):
            v.validar_texto("   ", "nombre")

    def test_texto_con_numeros_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_texto("Ana123", "nombre")


class PruebasCaracteresEspeciales(unittest.TestCase):
    """Validaciones de caracteres especiales y ataques comunes."""

    def test_simbolos_en_nombre_son_rechazados(self):
        for malo in ("Ana@", "Luis#", "<script>", "Ana; DROP TABLE"):
            # subTest muestra cuál valor falló si alguno falla.
            with self.subTest(valor=malo):
                with self.assertRaises(ValueError):
                    v.validar_texto(malo, "nombre")

    def test_apostrofo_y_guion_son_validos(self):
        self.assertEqual(
            v.validar_texto("O'Neill-Ruiz", "apellido"), "O'Neill-Ruiz"
        )

    def test_pasaporte_con_simbolos_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_numero_documento("AB-12#34", "PA")


class PruebasLongitudes(unittest.TestCase):
    """Validaciones de longitud mínima y máxima."""

    def test_nombre_de_un_caracter_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_texto("A", "nombre")

    def test_nombre_de_51_caracteres_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_texto("A" * 51, "nombre")

    def test_nombre_de_50_caracteres_es_valido(self):
        self.assertEqual(len(v.validar_texto("A" * 50, "nombre")), 50)

    def test_documento_muy_corto_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_numero_documento("1234", "CC")

    def test_documento_muy_largo_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_numero_documento("1234567890123", "CC")

    def test_correo_de_mas_de_100_caracteres_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_correo("a" * 95 + "@x.com")


class PruebasNumeros(unittest.TestCase):
    """Validaciones de campos numéricos."""

    def test_cedula_con_letras_es_rechazada(self):
        with self.assertRaises(ValueError):
            v.validar_numero_documento("10203A4050", "CC")

    def test_cedula_con_puntos_se_limpia(self):
        self.assertEqual(
            v.validar_numero_documento("1.020.304.050", "CC"),
            "1020304050",
        )

    def test_pasaporte_alfanumerico_es_valido(self):
        self.assertEqual(
            v.validar_numero_documento("ab123456", "PA"), "AB123456"
        )

    def test_celular_con_letras_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_celular("300ABC2233")

    def test_celular_con_espacios_y_guion_se_limpia(self):
        self.assertEqual(v.validar_celular("300 111-2233"), "3001112233")

    def test_celular_muy_corto_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_celular("12345")


class PruebasFechas(unittest.TestCase):
    """Validaciones de la fecha de nacimiento."""

    def test_fecha_valida_se_convierte_a_date(self):
        self.assertEqual(
            v.validar_fecha_nacimiento("1990-04-15", HOY), date(1990, 4, 15)
        )

    def test_formato_incorrecto_es_rechazado(self):
        for mala in ("15/04/1990", "1990-4", "hoy", ""):
            with self.subTest(valor=mala):
                with self.assertRaises(ValueError):
                    v.validar_fecha_nacimiento(mala, HOY)

    def test_fecha_inexistente_es_rechazada(self):
        with self.assertRaises(ValueError):
            v.validar_fecha_nacimiento("2001-02-30", HOY)

    def test_fecha_futura_es_rechazada(self):
        with self.assertRaises(ValueError):
            v.validar_fecha_nacimiento("2030-01-01", HOY)

    def test_edad_mayor_a_120_es_rechazada(self):
        with self.assertRaises(ValueError):
            v.validar_fecha_nacimiento("1890-01-01", HOY)


class PruebasCorreo(unittest.TestCase):
    """Validaciones del correo electrónico."""

    def test_correo_valido_se_guarda_en_minusculas(self):
        self.assertEqual(
            v.validar_correo(" Ana.Ruiz@Ejemplo.COM "), "ana.ruiz@ejemplo.com"
        )

    def test_correos_invalidos_son_rechazados(self):
        for malo in ("anaejemplo.com", "ana@", "ana@ejemplo", "@x.com"):
            with self.subTest(valor=malo):
                with self.assertRaises(ValueError):
                    v.validar_correo(malo)


class PruebasFormularioCompleto(unittest.TestCase):
    """Validación del pasajero completo y reglas que cruzan campos."""

    def test_formulario_valido_crea_pasajero(self):
        pasajero = v.validar_pasajero(datos_validos(), HOY)
        self.assertEqual(pasajero.nombre_completo(), "Ana María Ruiz Gómez")
        self.assertEqual(pasajero.edad(HOY), 36)

    def test_tipo_documento_invalido_es_rechazado(self):
        with self.assertRaises(ValueError):
            v.validar_pasajero(datos_validos(tipo_documento="XX"), HOY)

    def test_tarjeta_identidad_para_adulto_es_rechazada(self):
        with self.assertRaises(ValueError):
            v.validar_pasajero(datos_validos(tipo_documento="TI"), HOY)

    def test_cedula_para_menor_es_rechazada(self):
        with self.assertRaises(ValueError):
            v.validar_pasajero(
                datos_validos(fecha_nacimiento="2015-06-01"), HOY
            )

    def test_tarjeta_identidad_para_menor_es_valida(self):
        pasajero = v.validar_pasajero(
            datos_validos(tipo_documento="TI", fecha_nacimiento="2015-06-01"),
            HOY,
        )
        self.assertEqual(pasajero.tipo_documento, "TI")


# Permite correr este archivo solo: python tests/test_validaciones.py
if __name__ == "__main__":
    unittest.main()
