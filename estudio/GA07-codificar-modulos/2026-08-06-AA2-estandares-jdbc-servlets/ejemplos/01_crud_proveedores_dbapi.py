"""CRUD de proveedores con SQL directo: el equivalente en Python de JDBC (GA7-AA2-EV01).

Qué enseña: lo que el instructor hizo en Eclipse con la tabla "compañía":
conectarse, consultar (SELECT), insertar (INSERT), actualizar (UPDATE) y eliminar (DELETE),
respetando los estándares de nombres de paquetes, clases, métodos y variables.

Equivalencias con JDBC (Java):
    Class.forName("com.mysql.cj.jdbc.Driver")     -> import sqlite3  /  import pymysql
    DriverManager.getConnection(url, "root", ...) -> sqlite3.connect(...) / pymysql.connect(...)
    Statement st = con.createStatement()           -> cursor = conexion.cursor()
    ResultSet rs = st.executeQuery("SELECT ...")   -> cursor.execute(...); cursor.fetchall()
    while (rs.next()) { rs.getInt(1) ... }         -> for fila in cursor.fetchall(): ...
    st.executeUpdate("INSERT/UPDATE/DELETE ...")   -> cursor.execute(...); conexion.commit()

Base de datos: SQLite (archivo proveedores_demo.db) para probar sin instalar nada.
Para MySQL, cambia conectar() por la versión comentada y usa %s en vez de ? en las consultas.

Cómo correrlo:
    python 01_crud_proveedores_dbapi.py
"""

import sqlite3
from pathlib import Path

ARCHIVO_BD = Path(__file__).with_name("proveedores_demo.db")


class Proveedor:
    """Proveedor de servicios turísticos (hoteles, transporte, tours)."""

    def __init__(self, id_proveedor: int, nit: str, nombre: str):
        self.id_proveedor = id_proveedor
        self.nit = nit
        self.nombre = nombre

    def __repr__(self) -> str:
        return f"{self.id_proveedor} | {self.nit} | {self.nombre}"


def conectar() -> sqlite3.Connection:
    """Abre la conexión (en JDBC: DriverManager.getConnection)."""
    return sqlite3.connect(ARCHIVO_BD)
    # Versión MySQL (pip install pymysql):
    # import pymysql
    # return pymysql.connect(host="localhost", user="root", password="TU_CLAVE",
    #                        database="reservas_hyd")


def crear_tabla(conexion: sqlite3.Connection) -> None:
    conexion.execute(
        """CREATE TABLE IF NOT EXISTS proveedor (
               id_proveedor INTEGER PRIMARY KEY,
               nit          VARCHAR(20) NOT NULL UNIQUE,
               nombre       VARCHAR(80) NOT NULL
           )"""
    )
    conexion.commit()


def consultar_proveedores(conexion: sqlite3.Connection) -> list[Proveedor]:
    """SELECT (en JDBC: executeQuery + while rs.next())."""
    cursor = conexion.cursor()
    cursor.execute("SELECT id_proveedor, nit, nombre FROM proveedor ORDER BY id_proveedor")
    return [Proveedor(*fila) for fila in cursor.fetchall()]


def insertar_proveedor(conexion: sqlite3.Connection, proveedor: Proveedor) -> None:
    """INSERT. Los ? evitan la inyección SQL (en JDBC: PreparedStatement)."""
    conexion.execute(
        "INSERT INTO proveedor (id_proveedor, nit, nombre) VALUES (?, ?, ?)",
        (proveedor.id_proveedor, proveedor.nit, proveedor.nombre),
    )
    conexion.commit()


def actualizar_nombre(conexion: sqlite3.Connection, id_proveedor: int, nuevo_nombre: str) -> int:
    """UPDATE con WHERE: sin el WHERE se cambiarían TODOS los registros (advertencia de clase)."""
    cursor = conexion.execute(
        "UPDATE proveedor SET nombre = ? WHERE id_proveedor = ?", (nuevo_nombre, id_proveedor)
    )
    conexion.commit()
    return cursor.rowcount  # cuántas filas cambiaron


def eliminar_proveedor(conexion: sqlite3.Connection, id_proveedor: int) -> int:
    cursor = conexion.execute("DELETE FROM proveedor WHERE id_proveedor = ?", (id_proveedor,))
    conexion.commit()
    return cursor.rowcount


def main() -> None:
    conexion = conectar()
    try:
        crear_tabla(conexion)
        conexion.execute("DELETE FROM proveedor")  # deja la demo repetible
        for p in (
            Proveedor(1, "900111222", "Hoteles Andinos"),
            Proveedor(2, "900333444", "Transportes del Caribe"),
            Proveedor(3, "900555666", "Tours Coral"),
        ):
            insertar_proveedor(conexion, p)
        print("Consulta inicial:", *consultar_proveedores(conexion), sep="\n  ")

        insertar_proveedor(conexion, Proveedor(4, "900777888", "Operador Compacto"))
        print("Después de insertar el 4:", *consultar_proveedores(conexion), sep="\n  ")

        actualizar_nombre(conexion, 4, "Operador Compacto S.A.")
        print("Después de actualizar el 4:", *consultar_proveedores(conexion), sep="\n  ")

        eliminar_proveedor(conexion, 4)
        print("Después de eliminar el 4:", *consultar_proveedores(conexion), sep="\n  ")

        try:
            insertar_proveedor(conexion, Proveedor(1, "900111222", "Duplicado"))
        except sqlite3.IntegrityError as error:  # el "duplicado" que salió en clase
            print("Error controlado:", error)
    finally:
        conexion.close()  # en JDBC: con.close()


if __name__ == "__main__":
    main()
