"""Sentencias SQL de la tabla hoteles: el CRUD completo.

Equivale a lo que en Java se hace con JDBC (Statement, executeQuery,
executeUpdate y ResultSet). Los %s pasan los datos aparte del SQL, como
un PreparedStatement, para evitar la inyección SQL.
"""

from gestion_hoteles.conexion import conectar
from gestion_hoteles.hotel import Hotel

SELECT_HOTELES = (
    "SELECT h.id_hotel, h.nombre, h.destino_codigo, d.nombre AS destino, "
    "h.estrellas FROM hoteles h "
    "JOIN destinos d ON d.codigo = h.destino_codigo "
)


class HotelDAO:
    """Todo lo que toca la tabla hoteles pasa por esta clase."""

    def insertar(self, hotel: Hotel) -> int:
        """INSERT. Devuelve el id que le dio MySQL al hotel nuevo."""
        hotel.validar()
        with conectar() as conexion, conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO hoteles (nombre, destino_codigo, estrellas) "
                "VALUES (%s, %s, %s)",
                (hotel.nombre, hotel.destino_codigo, hotel.estrellas),
            )
            conexion.commit()
            hotel.id_hotel = cursor.lastrowid
        return hotel.id_hotel

    def consultar_todos(self) -> list[dict]:
        """SELECT de los hoteles activos, del más viejo al más nuevo."""
        with conectar() as conexion, conexion.cursor() as cursor:
            cursor.execute(
                SELECT_HOTELES + "WHERE h.activo ORDER BY h.id_hotel"
            )
            return list(cursor.fetchall())

    def buscar_por_id(self, id_hotel: int) -> dict | None:
        """SELECT de un solo hotel. Devuelve None si no existe."""
        with conectar() as conexion, conexion.cursor() as cursor:
            cursor.execute(
                SELECT_HOTELES + "WHERE h.id_hotel = %s", (id_hotel,)
            )
            return cursor.fetchone()

    def actualizar(self, hotel: Hotel) -> bool:
        """UPDATE. Sin el WHERE cambiaría todos los hoteles."""
        hotel.validar()
        with conectar() as conexion, conexion.cursor() as cursor:
            filas = cursor.execute(
                "UPDATE hoteles SET nombre = %s, destino_codigo = %s, "
                "estrellas = %s WHERE id_hotel = %s",
                (
                    hotel.nombre,
                    hotel.destino_codigo,
                    hotel.estrellas,
                    hotel.id_hotel,
                ),
            )
            conexion.commit()
        return filas == 1

    def eliminar(self, id_hotel: int) -> bool:
        """DELETE. MySQL no deja borrar un hotel que ya tiene tarifas."""
        with conectar() as conexion, conexion.cursor() as cursor:
            filas = cursor.execute(
                "DELETE FROM hoteles WHERE id_hotel = %s", (id_hotel,)
            )
            conexion.commit()
        return filas == 1

    def listar_destinos(self) -> list[dict]:
        """Destinos que se pueden escoger al crear o cambiar un hotel."""
        with conectar() as conexion, conexion.cursor() as cursor:
            cursor.execute(
                "SELECT codigo, nombre FROM destinos ORDER BY codigo"
            )
            return list(cursor.fetchall())
