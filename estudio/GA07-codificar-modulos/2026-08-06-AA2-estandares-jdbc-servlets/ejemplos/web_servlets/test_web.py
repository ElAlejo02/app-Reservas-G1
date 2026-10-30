"""Pruebas del módulo web: GET y POST con usuario correcto e incorrecto, y las plantillas.

Cómo correrlo (desde la carpeta web_servlets):
    pip install pytest httpx
    pytest -v test_web.py
"""

from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)


def test_index_tiene_los_dos_formularios():
    html = cliente.get("/").text
    assert 'method="get"' in html and 'method="post"' in html


def test_get_correcto_y_datos_visibles_en_la_url():
    r = cliente.get("/ingreso", params={"usuario": "root", "clave": "root"})
    assert "Ingreso exitoso" in r.text
    assert "clave=root" in str(r.url)  # por esto GET es inseguro


def test_post_incorrecto():
    r = cliente.post("/ingreso", data={"usuario": "root", "clave": "mala"})
    assert "incorrectos" in r.text and "POST" in r.text


def test_plantilla_con_expresiones_ciclo_y_funcion():
    html = cliente.get("/ejemplos-plantilla").text
    assert "SOFÍA HERRERA" in html
    assert "Habitación 105" in html
    assert "La suma es 15" in html
