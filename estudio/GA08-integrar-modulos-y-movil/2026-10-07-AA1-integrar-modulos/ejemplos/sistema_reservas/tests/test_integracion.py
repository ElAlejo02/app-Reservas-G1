"""Pruebas de integración: login + CRUD de hoteles sobre una base de datos real (SQLite temporal).

La GA8-AA1-EV01 pide "realizar las pruebas unitarias de cada módulo" y la EV02 "informar las
pruebas realizadas y su resultado": la salida de `pytest -v` sirve para ese informe.

Cómo correrlo (desde la carpeta sistema_reservas):
    pip install pytest httpx
    pytest -v
"""

import os
import tempfile

# Base de datos de prueba aparte, para no tocar la real. Debe definirse ANTES de importar la app.
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/prueba.db"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

HOTEL = {"nombre": "Hotel Coral", "ciudad": "San Andrés", "estrellas": 3, "tarifa_noche": 310000}


def test_flujo_completo():
    with TestClient(app) as cliente:  # el "with" ejecuta el arranque (crea tablas y datos)
        # Módulo de autenticación
        bien = cliente.post("/api/auth/login", json={"usuario": "admin", "contrasena": "12345"})
        mal = cliente.post("/api/auth/login", json={"usuario": "admin", "contrasena": "0000"})
        assert bien.status_code == 200
        assert mal.status_code == 401

        # Módulo de hoteles contra la base de datos
        iniciales = cliente.get("/api/hoteles").json()
        assert len(iniciales) == 2

        creado = cliente.post("/api/hoteles", json=HOTEL)
        assert creado.status_code == 201
        hotel_id = creado.json()["id"]

        cambio = cliente.put(f"/api/hoteles/{hotel_id}", json={**HOTEL, "tarifa_noche": 350000})
        assert cambio.json()["tarifa_noche"] == 350000

        assert cliente.delete(f"/api/hoteles/{hotel_id}").status_code == 200
        assert cliente.delete(f"/api/hoteles/{hotel_id}").status_code == 404
        assert len(cliente.get("/api/hoteles").json()) == 2


def test_registro_de_usuario_y_login():
    with TestClient(app) as cliente:
        datos = {"usuario": "asesor1", "contrasena": "clave123"}
        assert cliente.post("/api/auth/registro", json=datos).status_code == 201
        assert cliente.post("/api/auth/registro", json=datos).status_code == 409
        r = cliente.post("/api/auth/login", json=datos)
        assert r.status_code == 200 and r.json()["rol"] == "ASESOR"


def test_frontend_se_sirve_en_la_raiz():
    with TestClient(app) as cliente:
        r = cliente.get("/")
        assert r.status_code == 200 and "Reservas HyD" in r.text
