"""Pruebas automáticas del servicio de autenticación (lo mismo que se prueba en Postman).

Qué enseña: probar una API sin abrir Postman, con el cliente de pruebas de FastAPI.
Cada prueba es un caso que también se puede mostrar en Postman para la GA7-AA5-EV02.

Cómo correrlo:
    pip install pytest httpx
    pytest -v test_api_auth.py
"""

from fastapi.testclient import TestClient

from api_auth import app

cliente = TestClient(app)


def test_login_correcto_responde_200():
    r = cliente.post("/api/auth/login", json={"usuario": "admin", "contrasena": "1234"})
    assert r.status_code == 200
    assert r.json()["mensaje"] == "Autenticación exitosa"


def test_login_con_clave_errada_responde_401():
    r = cliente.post("/api/auth/login", json={"usuario": "admin", "contrasena": "0000"})
    assert r.status_code == 401


def test_login_usuario_inexistente_responde_401():
    r = cliente.post("/api/auth/login", json={"usuario": "nadie", "contrasena": "1234"})
    assert r.status_code == 401


def test_registro_y_luego_login():
    r = cliente.post("/api/auth/registro", json={"usuario": "asesor1", "contrasena": "clave123"})
    assert r.status_code == 201
    r = cliente.post("/api/auth/login", json={"usuario": "asesor1", "contrasena": "clave123"})
    assert r.status_code == 200


def test_registro_repetido_responde_409():
    cliente.post("/api/auth/registro", json={"usuario": "asesor2", "contrasena": "clave123"})
    r = cliente.post("/api/auth/registro", json={"usuario": "asesor2", "contrasena": "otra123"})
    assert r.status_code == 409


def test_json_incompleto_responde_422():
    r = cliente.post("/api/auth/login", json={"usuario": "admin"})  # falta la contraseña
    assert r.status_code == 422
