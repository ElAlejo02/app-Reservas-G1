"""Reglas del negocio: une el catálogo, las cuentas y el guardado.

Las rutas solo reciben y responden; lo que se decide, se decide acá.
"""

from __future__ import annotations

from app import calculos
from app.config import config
from app.esquemas import (
    Busqueda,
    Cotizacion,
    Desglose,
    LineaActividad,
    NuevaCotizacion,
    OpcionHotel,
    SolicitudCotizacion,
)
from app.repositorios import catalogo, cotizaciones


class NoEncontradoError(Exception):
    """Se responde con 404."""


class ReglaNoCumplidaError(Exception):
    """Se responde con 409: el pedido está bien escrito pero no se puede."""


# A qué estado puede pasar cada uno. Los que no tienen salida son finales.
TRANSICIONES = {
    "ABIERTA": {"ENVIADA", "ANULADA"},
    "ENVIADA": {"APROBADA", "RECHAZADA", "ANULADA"},
    "APROBADA": set(),
    "RECHAZADA": set(),
    "ANULADA": set(),
}


def _destino(codigo: str) -> dict:
    destino = catalogo.buscar_destino(codigo)
    if destino is None:
        raise NoEncontradoError(f"No existe el destino {codigo}.")
    return destino


def actividades_con_precio(destino: str | None) -> list[dict]:
    """El asesor ve el precio de venta, nunca el costo."""
    salida = []
    for act in catalogo.listar_actividades(destino):
        act["precio_adulto"] = calculos.precio_de_venta(
            act.pop("costo_adulto"), config.margen
        )
        act["precio_nino"] = calculos.precio_de_venta(
            act.pop("costo_nino"), config.margen
        )
        salida.append(act)
    return salida


def buscar_disponibilidad(busqueda: Busqueda) -> list[OpcionHotel]:
    _destino(busqueda.destino)
    noches = calculos.contar_noches(
        busqueda.fecha_entrada, busqueda.fecha_salida, config.noches_maximas
    )
    tarifas = catalogo.tarifas_disponibles(
        busqueda.destino,
        busqueda.fecha_entrada,
        busqueda.fecha_salida,
        busqueda.adultos + busqueda.ninos,
    )
    opciones = []
    for t in tarifas:
        costo = calculos.costo_hotel(
            noches,
            busqueda.adultos,
            busqueda.ninos,
            t["costo_adulto_noche"],
            t["costo_nino_noche"],
        )
        opciones.append(
            OpcionHotel(
                id_tarifa=t["id_tarifa"],
                id_hotel=t["id_hotel"],
                hotel=t["hotel"],
                estrellas=t["estrellas"],
                tipo_habitacion=t["tipo_habitacion"],
                temporada=t["temporada"],
                noches=noches,
                precio_estadia=calculos.precio_de_venta(costo, config.margen),
            )
        )
    return sorted(opciones, key=lambda o: o.precio_estadia)


def _armar(solicitud: SolicitudCotizacion) -> tuple[Desglose, list[dict]]:
    """Calcula todo. Devuelve el desglose y las líneas para guardar."""
    destino = _destino(solicitud.destino)
    noches = calculos.contar_noches(
        solicitud.fecha_entrada, solicitud.fecha_salida, config.noches_maximas
    )

    # La tarifa tiene que servir para ESTAS fechas, destino y personas.
    disponibles = catalogo.tarifas_disponibles(
        solicitud.destino,
        solicitud.fecha_entrada,
        solicitud.fecha_salida,
        solicitud.adultos + solicitud.ninos,
    )
    tarifa = next(
        (t for t in disponibles if t["id_tarifa"] == solicitud.id_tarifa),
        None,
    )
    if tarifa is None:
        raise ReglaNoCumplidaError(
            "Esa tarifa no aplica para el destino, las fechas o la "
            "cantidad de personas. Busque disponibilidad de nuevo."
        )

    pedidas = solicitud.actividades
    ids = [a.id_actividad for a in pedidas]
    encontradas = catalogo.buscar_actividades(ids)
    costos, lineas = [], []
    for pedida in pedidas:
        act = encontradas.get(pedida.id_actividad)
        if act is None or act["destino_codigo"] != solicitud.destino:
            raise ReglaNoCumplidaError(
                f"La actividad {pedida.id_actividad} no existe en "
                f"{destino['nombre']}."
            )
        if pedida.adultos + pedida.ninos == 0:
            raise ReglaNoCumplidaError(
                f"{act['nombre']}: indique cuántas personas."
            )
        if (
            pedida.adultos > solicitud.adultos
            or pedida.ninos > solicitud.ninos
        ):
            raise ReglaNoCumplidaError(
                f"{act['nombre']}: hay más personas que en la cotización."
            )
        costos.append(
            calculos.costo_actividad(
                pedida.adultos,
                pedida.ninos,
                act["costo_adulto"],
                act["costo_nino"],
            )
        )
        lineas.append({**pedida.model_dump(), "nombre": act["nombre"]})

    totales = calculos.calcular_totales(
        costo_del_hotel=calculos.costo_hotel(
            noches,
            solicitud.adultos,
            solicitud.ninos,
            tarifa["costo_adulto_noche"],
            tarifa["costo_nino_noche"],
        ),
        costos_actividades=costos,
        margen=config.margen,
        descuento_porcentaje=solicitud.descuento_porcentaje,
        descuento_maximo=config.descuento_maximo,
        tasa_iva=config.iva,
        exento_iva=destino["exento_iva"],
        tasa_por_persona=destino["tasa_por_persona"],
        personas=solicitud.adultos + solicitud.ninos,
    )
    precios = totales.precios_por_actividad
    for linea, precio in zip(lineas, precios, strict=True):
        linea["precio"] = precio

    desglose = Desglose(
        destino=destino["nombre"],
        hotel=tarifa["hotel"],
        tipo_habitacion=tarifa["tipo_habitacion"],
        temporada=tarifa["temporada"],
        noches=noches,
        precio_hotel=totales.precio_hotel,
        actividades=[LineaActividad(**ln) for ln in lineas],
        precio_actividades=totales.precio_actividades,
        subtotal=totales.subtotal,
        descuento_porcentaje=totales.descuento_porcentaje,
        descuento=totales.descuento,
        iva_porcentaje=totales.iva_porcentaje,
        iva=totales.iva,
        tasas=totales.tasas,
        total=totales.total,
    )
    return desglose, lineas


def calcular(solicitud: SolicitudCotizacion) -> Desglose:
    desglose, _ = _armar(solicitud)
    return desglose


def crear(nueva: NuevaCotizacion) -> Cotizacion:
    desglose, lineas = _armar(nueva)
    datos = {
        "cliente_nombre": nueva.cliente_nombre.strip(),
        "cliente_correo": nueva.cliente_correo.strip().lower(),
        "destino_codigo": nueva.destino,
        "fecha_entrada": nueva.fecha_entrada,
        "fecha_salida": nueva.fecha_salida,
        "adultos": nueva.adultos,
        "ninos": nueva.ninos,
        "id_tarifa": nueva.id_tarifa,
        **desglose.model_dump(
            include={
                "noches",
                "precio_hotel",
                "precio_actividades",
                "subtotal",
                "descuento_porcentaje",
                "descuento",
                "iva_porcentaje",
                "iva",
                "tasas",
                "total",
            }
        ),
    }
    codigo = cotizaciones.guardar(datos, lineas)
    return obtener(codigo)


def obtener(codigo: str) -> Cotizacion:
    fila = cotizaciones.buscar(codigo.upper())
    if fila is None:
        raise NoEncontradoError(f"No existe la cotización {codigo}.")
    return Cotizacion(**fila, desglose=Desglose(**fila))


def cambiar_estado(codigo: str, nuevo: str) -> Cotizacion:
    actual = obtener(codigo)
    if nuevo not in TRANSICIONES[actual.estado]:
        opciones = sorted(TRANSICIONES[actual.estado])
        permitidos = ", ".join(opciones) or "ninguno"
        raise ReglaNoCumplidaError(
            f"Una cotización {actual.estado} no puede pasar a {nuevo}. "
            f"Puede pasar a: {permitidos}."
        )
    cotizaciones.cambiar_estado(actual.codigo, nuevo)
    return obtener(actual.codigo)
