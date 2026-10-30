"""Conexión a la base de datos y CRUD de pasajeros con SQLAlchemy (lo que en Java es JDBC).

Qué enseña: crear la conexión, mapear una clase a una tabla y las cuatro operaciones
que pide la GA7-AA3-EV01: inserción, consulta, actualización y eliminación.

Equivale en Java a: el paquete "conexion" con la clase Conexion (DriverManager.getConnection)
más los PreparedStatement de INSERT, SELECT, UPDATE y DELETE.

Base de datos:
    - Por defecto usa SQLite (un archivo reservas_demo.db aquí mismo) para probar sin instalar nada.
    - Para MySQL, primero crea la base con 04_crear_bd_mysql.sql y luego, en la terminal:
        set DATABASE_URL=mysql+pymysql://root:TU_CLAVE@localhost:3306/reservas_hyd
      (la clave no se escribe en el código ni se sube a GitHub).

Cómo correrlo:
    pip install sqlalchemy pymysql
    python 02_repositorio_pasajeros.py
"""

import os
from pathlib import Path

from sqlalchemy import CheckConstraint, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

URL_POR_DEFECTO = f"sqlite:///{Path(__file__).with_name('reservas_demo.db')}"
DATABASE_URL = os.environ.get("DATABASE_URL", URL_POR_DEFECTO)

# El "engine" es la conexión. En Java: Connection con = DriverManager.getConnection(url, user, pass)
engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Pasajero(Base):
    """Cada objeto Pasajero es una fila de la tabla pasajeros."""

    __tablename__ = "pasajeros"
    __table_args__ = (CheckConstraint("edad BETWEEN 0 AND 120", name="ck_edad"),)

    documento: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    edad: Mapped[int] = mapped_column(Integer)
    genero: Mapped[str] = mapped_column(String(10))

    def __repr__(self) -> str:
        return f"Pasajero({self.documento}, {self.nombre}, {self.edad}, {self.genero})"


def crear_tablas() -> None:
    """CREATE TABLE IF NOT EXISTS: solo crea lo que falta."""
    Base.metadata.create_all(engine)


# ------------------------------------------------------------------ CRUD
def insertar(documento: str, nombre: str, edad: int, genero: str) -> None:
    with Session(engine) as sesion:  # abre la conexión y la cierra al salir del bloque
        if sesion.get(Pasajero, documento):
            raise ValueError(f"Ya existe un pasajero con documento {documento}")
        sesion.add(Pasajero(documento=documento, nombre=nombre, edad=edad, genero=genero))
        sesion.commit()  # sin commit no queda guardado (igual que en JDBC)


def consultar_todos() -> list[Pasajero]:
    with Session(engine) as sesion:
        return list(sesion.scalars(select(Pasajero).order_by(Pasajero.nombre)))


def buscar(documento: str) -> Pasajero | None:
    with Session(engine) as sesion:
        return sesion.get(Pasajero, documento)


def actualizar(documento: str, nombre: str, edad: int, genero: str) -> None:
    with Session(engine) as sesion:
        pasajero = sesion.get(Pasajero, documento)
        if pasajero is None:
            raise ValueError(f"No existe el documento {documento}")
        pasajero.nombre, pasajero.edad, pasajero.genero = nombre, edad, genero
        sesion.commit()


def eliminar(documento: str) -> None:
    with Session(engine) as sesion:
        pasajero = sesion.get(Pasajero, documento)
        if pasajero is None:
            raise ValueError(f"No existe el documento {documento}")
        sesion.delete(pasajero)
        sesion.commit()


def demo() -> None:
    motor = (
        "SQLite (archivo reservas_demo.db)"
        if engine.url.get_backend_name() == "sqlite"
        else "MySQL"
    )
    print("Base de datos:", motor)
    crear_tablas()
    for doc in ("900001", "900002"):  # deja la demo repetible
        if buscar(doc):
            eliminar(doc)

    insertar("900001", "Ana Ruiz", 34, "Femenino")
    insertar("900002", "Luis Mora", 41, "Masculino")
    print("Después de insertar:", consultar_todos())

    actualizar("900002", "Luis Mora Díaz", 42, "Masculino")
    print("Después de actualizar:", buscar("900002"))

    eliminar("900001")
    print("Después de eliminar:", consultar_todos())


if __name__ == "__main__":
    demo()
