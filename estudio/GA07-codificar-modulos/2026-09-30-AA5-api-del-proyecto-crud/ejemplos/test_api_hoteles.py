"""Pruebas de la API de hoteles: el mismo recorrido que la instructora hizo en Postman.

Listar, actualizar, eliminar, crear y volver a listar, revisando el código HTTP de cada paso.

Cómo correrlo:
    pip install pytest httpx
    pytest -v test_api_hoteles.py
"""

from fastapi.testclient import TestClient

from api_hoteles import app

cliente = TestClient(app)
NUEVO = {"nombre": "Hotel Coral", "ciudad": "San Andrés", "estrellas": 3, "tarifa_noche": 310000}


def test_listar_trae_los_datos_iniciales():
    r = cliente.get("/api/hoteles")
    assert r.status_code == 200
    assert {h["nombre"] for h in r.json()} >= {"Hotel Nogal", "Hotel Bahía"}


def test_filtrar_por_ciudad():
    r = cliente.get("/api/hoteles", params={"ciudad": "medellín"})
    assert [h["nombre"] for h in r.json()] == ["Hotel Nogal"]


def test_crear_responde_201_y_asigna_id():
    r = cliente.post("/api/hoteles", json=NUEVO)
    assert r.status_code == 201
    assert r.json()["id"] > 2


def test_actualizar():
    cambios = {**NUEVO, "nombre": "Hotel Nogal Plaza", "ciudad": "Medellín"}
    r = cliente.put("/api/hoteles/1", json=cambios)
    assert r.status_code == 200
    assert cliente.get("/api/hoteles/1").json()["nombre"] == "Hotel Nogal Plaza"


def test_eliminar_y_ya_no_existe():
    creado = cliente.post("/api/hoteles", json=NUEVO).json()
    r = cliente.delete(f"/api/hoteles/{creado['id']}")
    assert r.status_code == 200
    assert cliente.get(f"/api/hoteles/{creado['id']}").status_code == 404


def test_id_inexistente_responde_404():
    assert cliente.put("/api/hoteles/999", json=NUEVO).status_code == 404
    assert cliente.delete("/api/hoteles/999").status_code == 404


def test_datos_invalidos_responden_422():
    malo = {**NUEVO, "estrellas": 7, "tarifa_noche": -5}
    assert cliente.post("/api/hoteles", json=malo).status_code == 422
