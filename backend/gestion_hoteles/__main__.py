"""Menú de consola para gestionar los hoteles.

Se corre desde la carpeta backend:
    python -m gestion_hoteles
"""

import sys

import pymysql

from gestion_hoteles.hotel import Hotel
from gestion_hoteles.hotel_dao import HotelDAO

LINEA = "-" * 66


def leer(mensaje: str) -> str:
    """input() que también muestra lo escrito si llega desde un archivo."""
    texto = input(mensaje)
    if not sys.stdin.isatty():
        print(texto)
    return texto


def mostrar_hoteles(hoteles: list[dict]) -> None:
    """Imprime los hoteles como una tabla."""
    print(LINEA)
    print(f"{'ID':>3}  {'HOTEL':<32} {'DESTINO':<14} ESTRELLAS")
    print(LINEA)
    for hotel in hoteles:
        estrellas = "*" * hotel["estrellas"]
        print(
            f"{hotel['id_hotel']:>3}  {hotel['nombre'][:32]:<32} "
            f"{hotel['destino']:<14} {estrellas}"
        )
    print(LINEA)
    palabra = "hotel" if len(hoteles) == 1 else "hoteles"
    print(f"Total: {len(hoteles)} {palabra}")


def pedir_entero(mensaje: str, por_defecto: int | None = None) -> int:
    """Pide un número. Con Enter deja el valor por defecto, si lo hay."""
    while True:
        texto = leer(mensaje).strip()
        if not texto and por_defecto is not None:
            return por_defecto
        if texto.isdigit():
            return int(texto)
        print("  Escriba solo números.")


def mostrar_destinos(dao: HotelDAO) -> None:
    destinos = dao.listar_destinos()
    print("Destinos: " + ", ".join(d["codigo"] for d in destinos))


def opcion_consultar(dao: HotelDAO) -> None:
    mostrar_hoteles(dao.consultar_todos())


def opcion_agregar(dao: HotelDAO) -> None:
    mostrar_destinos(dao)
    hotel_nuevo = Hotel(
        nombre=leer("Nombre del hotel: "),
        destino_codigo=leer("Código del destino: "),
        estrellas=pedir_entero("Estrellas (1 a 5): "),
    )
    try:
        id_hotel = dao.insertar(hotel_nuevo)
    except pymysql.IntegrityError:
        print("  No se guardó: ese destino no existe.")
        return
    print(f"\nHotel guardado con el ID {id_hotel}:")
    mostrar_hoteles([dao.buscar_por_id(id_hotel)])


def opcion_actualizar(dao: HotelDAO) -> None:
    id_hotel = pedir_entero("ID del hotel a actualizar: ")
    actual = dao.buscar_por_id(id_hotel)
    if actual is None:
        print("  No hay ningún hotel con ese ID.")
        return
    mostrar_hoteles([actual])
    print("Escriba el dato nuevo o pulse Enter para dejarlo igual.")
    mostrar_destinos(dao)
    hotel_editado = Hotel(
        nombre=leer(f"Nombre [{actual['nombre']}]: ") or actual["nombre"],
        destino_codigo=leer(f"Destino [{actual['destino_codigo']}]: ")
        or actual["destino_codigo"],
        estrellas=pedir_entero(
            f"Estrellas [{actual['estrellas']}]: ", actual["estrellas"]
        ),
        id_hotel=id_hotel,
    )
    try:
        dao.actualizar(hotel_editado)
    except pymysql.IntegrityError:
        print("  No se guardó: ese destino no existe.")
        return
    print("\nHotel actualizado:")
    mostrar_hoteles([dao.buscar_por_id(id_hotel)])


def opcion_eliminar(dao: HotelDAO) -> None:
    id_hotel = pedir_entero("ID del hotel a eliminar: ")
    actual = dao.buscar_por_id(id_hotel)
    if actual is None:
        print("  No hay ningún hotel con ese ID.")
        return
    mostrar_hoteles([actual])
    if leer("¿Seguro que lo elimina? (s/n): ").strip().lower() != "s":
        print("  No se eliminó nada.")
        return
    try:
        dao.eliminar(id_hotel)
    except pymysql.IntegrityError:
        print("  No se puede eliminar: el hotel ya tiene tarifas guardadas.")
        return
    print(f"  Hotel {id_hotel} eliminado.")


OPCIONES = {
    "1": ("Consultar hoteles", opcion_consultar),
    "2": ("Agregar hotel", opcion_agregar),
    "3": ("Actualizar hotel", opcion_actualizar),
    "4": ("Eliminar hotel", opcion_eliminar),
}


def main() -> None:
    dao = HotelDAO()
    while True:
        print("\n===== HOTELES Y DESTINOS · Gestión de hoteles =====")
        for numero, (texto, _) in OPCIONES.items():
            print(f"{numero}. {texto}")
        print("0. Salir")
        opcion = leer("Opción: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            break
        if opcion not in OPCIONES:
            print("  Esa opción no existe.")
            continue
        print()
        try:
            OPCIONES[opcion][1](dao)
        except ValueError as error:
            print(f"  No se guardó: {error}")
        except pymysql.OperationalError as error:
            print("  No hay conexión con MySQL: revise que esté prendido")
            print("  y que la clave del archivo .env sea la correcta.")
            print(f"  Detalle: {error}")
            break


if __name__ == "__main__":
    main()
