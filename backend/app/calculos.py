"""Cuentas de una cotización.

Acá no hay base de datos ni internet, solo matemática. Por eso es lo
primero que se prueba.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_HALF_UP, Decimal


class CalculoError(ValueError):
    """Datos que no permiten calcular (fechas al revés, margen raro...)."""


def a_pesos(valor: Decimal) -> int:
    """Redondea a peso entero: 0,5 sube."""
    return int(valor.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def contar_noches(entrada: date, salida: date, maximo: int) -> int:
    noches = (salida - entrada).days
    if noches < 1:
        raise CalculoError("La salida debe ser después de la entrada.")
    if noches > maximo:
        raise CalculoError(f"Máximo {maximo} noches por cotización.")
    return noches


def precio_de_venta(costo: int, margen: Decimal) -> int:
    """Costo / (1 - margen).

    Es margen sobre el precio, como se hace en HyD: con 20 %, un costo
    de 800.000 se vende en 1.000.000 y el 20 % de eso es la ganancia.
    """
    if not Decimal("0") <= margen < Decimal("1"):
        raise CalculoError("El margen debe estar entre 0 y 1.")
    return a_pesos(Decimal(costo) / (Decimal("1") - margen))


def costo_hotel(
    noches: int, adultos: int, ninos: int, adulto_noche: int, nino_noche: int
) -> int:
    return noches * (adultos * adulto_noche + ninos * nino_noche)


def costo_actividad(
    adultos: int, ninos: int, costo_adulto: int, costo_nino: int
) -> int:
    return adultos * costo_adulto + ninos * costo_nino


@dataclass
class Totales:
    """Las líneas que se le muestran al cliente, ya calculadas."""

    precio_hotel: int
    precio_actividades: int
    subtotal: int
    descuento_porcentaje: int
    descuento: int
    iva_porcentaje: int
    iva: int
    tasas: int
    total: int
    precios_por_actividad: list[int] = field(default_factory=list)


def calcular_totales(
    costo_del_hotel: int,
    costos_actividades: list[int],
    margen: Decimal,
    descuento_porcentaje: int,
    descuento_maximo: int,
    tasa_iva: Decimal,
    exento_iva: bool,
    tasa_por_persona: int,
    personas: int,
) -> Totales:
    """Arma el desglose completo.

    Orden: venta con margen -> descuento -> IVA sobre lo que queda ->
    tasas del destino. El IVA va sobre el valor ya con descuento porque
    eso es lo que realmente se le cobra al cliente.
    """
    if not 0 <= descuento_porcentaje <= descuento_maximo:
        raise CalculoError(
            f"El descuento debe estar entre 0 y {descuento_maximo} %."
        )

    precio_hotel = precio_de_venta(costo_del_hotel, margen)
    precios_act = [precio_de_venta(c, margen) for c in costos_actividades]
    precio_actividades = sum(precios_act)
    subtotal = precio_hotel + precio_actividades

    descuento = a_pesos(
        Decimal(subtotal) * Decimal(descuento_porcentaje) / Decimal("100")
    )
    base = subtotal - descuento
    iva = 0 if exento_iva else a_pesos(Decimal(base) * tasa_iva)
    tasas = tasa_por_persona * personas

    return Totales(
        precio_hotel=precio_hotel,
        precio_actividades=precio_actividades,
        subtotal=subtotal,
        descuento_porcentaje=descuento_porcentaje,
        descuento=descuento,
        iva_porcentaje=0 if exento_iva else a_pesos(tasa_iva * 100),
        iva=iva,
        tasas=tasas,
        total=base + iva + tasas,
        precios_por_actividad=precios_act,
    )
