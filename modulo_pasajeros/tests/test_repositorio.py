"""Pruebas de integración del CRUD contra MySQL real.

A diferencia de las pruebas unitarias, estas SÍ escriben en la base de
datos: crean un pasajero de prueba, lo buscan, lo modifican y lo
eliminan. Así se demuestra que el CRUD completo funciona.

Si MySQL no está disponible, las pruebas se marcan como "omitidas"
(skipped) en vez de fallar.
"""

import unittest
from datetime import date

import pymysql

from pasajeros import repositorio
from pasajeros.conexion import obtener_conexion
from pasajeros.modelo import Pasajero

# Documento que no usaría ninguna persona real, para no chocar con
# datos verdaderos.
DOCUMENTO_PRUEBA = "99999999"


def hay_base_de_datos() -> bool:
    """Indica si es posible conectarse a MySQL."""
    try:
        with obtener_conexion():
            return True
    except pymysql.MySQLError:
        return False


# El decorador salta TODA la clase si no hay conexión.
@unittest.skipUnless(hay_base_de_datos(), "MySQL no está disponible")
class PruebasCrudPasajeros(unittest.TestCase):
    """Ciclo completo: crear, buscar, listar, actualizar y eliminar."""

    def setUp(self):
        """Se ejecuta ANTES de cada prueba: deja la base sin residuos."""
        repositorio.eliminar(DOCUMENTO_PRUEBA)
        self.pasajero = Pasajero(
            nombre="Prueba",
            apellido="Automatica",
            tipo_documento="CC",
            numero_documento=DOCUMENTO_PRUEBA,
            fecha_nacimiento=date(1995, 1, 20),
            pais="Colombia",
            celular="3000000000",
            correo="prueba@ejemplo.com",
        )

    def tearDown(self):
        """Se ejecuta DESPUÉS de cada prueba: borra lo que se creó."""
        repositorio.eliminar(DOCUMENTO_PRUEBA)

    def test_crear_y_buscar(self):
        nuevo_id = repositorio.crear(self.pasajero)
        encontrado = repositorio.buscar_por_documento(DOCUMENTO_PRUEBA)
        self.assertGreater(nuevo_id, 0)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "Prueba")
        self.assertEqual(encontrado.fecha_nacimiento, date(1995, 1, 20))

    def test_documento_duplicado_es_rechazado(self):
        repositorio.crear(self.pasajero)
        with self.assertRaises(ValueError):
            repositorio.crear(self.pasajero)

    def test_listar_incluye_el_pasajero(self):
        repositorio.crear(self.pasajero)
        documentos = [p.numero_documento for p in repositorio.listar()]
        self.assertIn(DOCUMENTO_PRUEBA, documentos)

    def test_actualizar(self):
        repositorio.crear(self.pasajero)
        self.pasajero.celular = "3111111111"
        self.assertTrue(repositorio.actualizar(self.pasajero))
        encontrado = repositorio.buscar_por_documento(DOCUMENTO_PRUEBA)
        self.assertEqual(encontrado.celular, "3111111111")

    def test_actualizar_sin_cambios_reporta_existente(self):
        repositorio.crear(self.pasajero)
        self.assertTrue(repositorio.actualizar(self.pasajero))

    def test_eliminar(self):
        repositorio.crear(self.pasajero)
        self.assertTrue(repositorio.eliminar(DOCUMENTO_PRUEBA))
        self.assertIsNone(repositorio.buscar_por_documento(DOCUMENTO_PRUEBA))

    def test_operaciones_sobre_documento_inexistente(self):
        self.assertIsNone(repositorio.buscar_por_documento("00000"))
        self.assertFalse(repositorio.eliminar("00000"))
        self.pasajero.numero_documento = "00000"
        self.assertFalse(repositorio.actualizar(self.pasajero))


if __name__ == "__main__":
    unittest.main()
