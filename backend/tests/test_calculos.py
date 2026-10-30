"""Pruebas de las cuentas. No necesitan base de datos."""

import unittest
from datetime import date
from decimal import Decimal

from app import calculos as c

MARGEN = Decimal("0.20")
IVA = Decimal("0.19")


def totales(**cambios):
    datos = {
        "costo_del_hotel": 2_100_000,
        "costos_actividades": [240_000],
        "margen": MARGEN,
        "descuento_porcentaje": 0,
        "descuento_maximo": 15,
        "tasa_iva": IVA,
        "exento_iva": False,
        "tasa_por_persona": 0,
        "personas": 3,
    }
    datos.update(cambios)
    return c.calcular_totales(**datos)


class PruebasNoches(unittest.TestCase):
    def test_cuenta_noches(self):
        self.assertEqual(
            c.contar_noches(date(2027, 2, 10), date(2027, 2, 14), 30), 4
        )

    def test_salida_igual_a_entrada(self):
        with self.assertRaises(c.CalculoError):
            c.contar_noches(date(2027, 2, 10), date(2027, 2, 10), 30)

    def test_demasiadas_noches(self):
        with self.assertRaises(c.CalculoError):
            c.contar_noches(date(2027, 2, 1), date(2027, 3, 10), 30)


class PruebasPrecios(unittest.TestCase):
    def test_margen_sobre_precio(self):
        # 800.000 / (1 - 0,20) = 1.000.000
        self.assertEqual(c.precio_de_venta(800_000, MARGEN), 1_000_000)

    def test_redondeo_a_peso(self):
        # 100.001 / 0,8 = 125.001,25 -> 125.001
        self.assertEqual(c.precio_de_venta(100_001, MARGEN), 125_001)

    def test_margen_invalido(self):
        with self.assertRaises(c.CalculoError):
            c.precio_de_venta(1000, Decimal("1"))

    def test_costo_hotel(self):
        # 4 noches x (2 x 210.000 + 1 x 105.000)
        self.assertEqual(c.costo_hotel(4, 2, 1, 210_000, 105_000), 2_100_000)

    def test_costo_actividad(self):
        self.assertEqual(c.costo_actividad(2, 1, 90_000, 60_000), 240_000)


class PruebasTotales(unittest.TestCase):
    def test_sin_descuento(self):
        t = totales()
        self.assertEqual(t.precio_hotel, 2_625_000)
        self.assertEqual(t.precio_actividades, 300_000)
        self.assertEqual(t.subtotal, 2_925_000)
        self.assertEqual(t.iva, 555_750)
        self.assertEqual(t.total, 3_480_750)

    def test_con_descuento_el_iva_va_despues(self):
        t = totales(descuento_porcentaje=5)
        self.assertEqual(t.descuento, 146_250)
        self.assertEqual(t.iva, 527_963)  # 19 % de 2.778.750
        self.assertEqual(t.total, 3_306_713)

    def test_destino_exento(self):
        t = totales(exento_iva=True)
        self.assertEqual((t.iva, t.iva_porcentaje), (0, 0))
        self.assertEqual(t.total, t.subtotal)

    def test_tasa_por_persona(self):
        t = totales(exento_iva=True, tasa_por_persona=150_000)
        self.assertEqual(t.tasas, 450_000)
        self.assertEqual(t.total, t.subtotal + 450_000)

    def test_descuento_mayor_al_permitido(self):
        with self.assertRaises(c.CalculoError):
            totales(descuento_porcentaje=16)

    def test_sin_actividades(self):
        t = totales(costos_actividades=[])
        self.assertEqual(t.precio_actividades, 0)
        self.assertEqual(t.subtotal, t.precio_hotel)


if __name__ == "__main__":
    unittest.main()
