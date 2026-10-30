"""Capa de modelo: las tablas como clases (lo que en Java hace Hibernate/JPA)."""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario: Mapped[str] = mapped_column(String(30), unique=True)
    clave_hash: Mapped[bytes]  # nunca la contraseña en texto plano
    rol: Mapped[str] = mapped_column(String(15), default="ASESOR")


class Hotel(Base):
    __tablename__ = "hoteles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(80))
    ciudad: Mapped[str] = mapped_column(String(40))
    estrellas: Mapped[int] = mapped_column(Integer)
    tarifa_noche: Mapped[float] = mapped_column(Float)
