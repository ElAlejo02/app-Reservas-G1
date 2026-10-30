"""Pruebas de la API completa contra MySQL.

Necesitan la base con 01_esquema.sql y 02_datos_prueba.sql cargados.
Si MySQL no está prendido, se saltan.
"""

import unittest
import warnings

import pymysql

from app.db import conectar
from app.repositorios import cotizaciones

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fastapi.testclient import TestClient

from app.main import app


def hay_base_de_datos() -> bool:
    try:
        with conectar():
            return True
    except pymysql.MySQLError:
        return False


BUSQUEDA = {
    "destino": "CTG",
    "fecha_entrada": "2027-02-10",
    "fecha_salida": "2027-02-14",
    "adultos": 2,
    "ninos": 1,
}


@unittest.skipUnless(hay_base_de_datos(), "MySQL no está disponible")
class PruebasApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = TestClient(app)
        cls.creadas = []

    @classmethod
    def tearDownClass(cls):
        for codigo in cls.creadas:
            cotizaciones.borrar(codigo)

    def _solicitud(self, **cambios):
        opciones = self.api.post("/disponibilidad", json=BUSQUEDA).json()
        actividad = self.api.get("/actividades?destino=CTG").json()[0]
        datos = {
            **BUSQUEDA,
            "id_tarifa": opciones[0]["id_tarifa"],
            "actividades": [
                {"id_actividad": actividad["id_actividad"], "adultos": 2}
            ],
            "descuento_porcentaje": 5,
        }
        datos.update(cambios)
        return datos

    def _guardar(self, **cambios):
        datos = {
            **self._solicitud(**cambios),
            "cliente_nombre": "Agencia de Prueba",
            "cliente_correo": "Prueba@Correo.com",
        }
        respuesta = self.api.post("/cotizaciones", json=datos)
        self.assertEqual(respuesta.status_code, 201, respuesta.text)
        self.creadas.append(respuesta.json()["codigo"])
        return respuesta.json()

    def test_estado_del_servidor(self):
        self.assertEqual(self.api.get("/").json()["estado"], "ok")

    def test_catalogo(self):
        self.assertEqual(len(self.api.get("/destinos").json()), 8)
        hoteles = self.api.get("/hoteles?destino=ctg").json()
        self.assertTrue(all(h["destino_codigo"] == "CTG" for h in hoteles))
        actividad = self.api.get("/actividades?destino=CTG").json()[0]
        self.assertNotIn("costo_adulto", actividad)  # nunca mostrar costos

    def test_disponibilidad_ordenada_por_precio(self):
        opciones = self.api.post("/disponibilidad", json=BUSQUEDA).json()
        precios = [o["precio_estadia"] for o in opciones]
        self.assertTrue(precios)
        self.assertEqual(precios, sorted(precios))

    def test_disponibilidad_sin_cupo_para_tantos(self):
        busqueda = {**BUSQUEDA, "adultos": 6}
        opciones = self.api.post("/disponibilidad", json=busqueda).json()
        self.assertEqual(opciones, [])

    def test_fechas_al_reves(self):
        busqueda = {**BUSQUEDA, "fecha_salida": "2027-02-01"}
        respuesta = self.api.post("/disponibilidad", json=busqueda)
        self.assertEqual(respuesta.status_code, 422)
        self.assertIn("después de la entrada", respuesta.json()["detail"])

    def test_destino_inexistente(self):
        busqueda = {**BUSQUEDA, "destino": "XXX"}
        respuesta = self.api.post("/disponibilidad", json=busqueda)
        self.assertEqual(respuesta.status_code, 404)

    def test_calcular_no_guarda(self):
        antes = len(self.api.get("/cotizaciones?limite=200").json())
        respuesta = self.api.post(
            "/cotizaciones/calcular", json=self._solicitud()
        )
        self.assertEqual(respuesta.status_code, 200)
        desglose = respuesta.json()
        self.assertEqual(
            desglose["total"],
            desglose["subtotal"]
            - desglose["descuento"]
            + desglose["iva"]
            + desglose["tasas"],
        )
        despues = len(self.api.get("/cotizaciones?limite=200").json())
        self.assertEqual(antes, despues)

    def test_tarifa_de_otro_destino(self):
        respuesta = self.api.post(
            "/cotizaciones/calcular", json=self._solicitud(destino="SMR")
        )
        self.assertEqual(respuesta.status_code, 409)

    def test_actividad_con_mas_personas(self):
        solicitud = self._solicitud()
        solicitud["actividades"][0]["adultos"] = 5
        respuesta = self.api.post("/cotizaciones/calcular", json=solicitud)
        self.assertEqual(respuesta.status_code, 409)

    def test_descuento_excesivo(self):
        respuesta = self.api.post(
            "/cotizaciones/calcular",
            json=self._solicitud(descuento_porcentaje=40),
        )
        self.assertEqual(respuesta.status_code, 422)

    def test_guardar_y_consultar(self):
        guardada = self._guardar()
        self.assertRegex(guardada["codigo"], r"^COT-\d{6}$")
        self.assertEqual(guardada["estado"], "ABIERTA")
        self.assertEqual(guardada["cliente_correo"], "prueba@correo.com")
        consultada = self.api.get(f"/cotizaciones/{guardada['codigo']}")
        self.assertEqual(consultada.json()["desglose"], guardada["desglose"])

    def test_cotizacion_inexistente(self):
        respuesta = self.api.get("/cotizaciones/COT-999999")
        self.assertEqual(respuesta.status_code, 404)

    def test_flujo_de_estados(self):
        codigo = self._guardar()["codigo"]
        ruta = f"/cotizaciones/{codigo}/estado"
        saltar = self.api.patch(ruta, json={"estado": "APROBADA"})
        self.assertEqual(saltar.status_code, 409)
        for estado in ("ENVIADA", "APROBADA"):
            respuesta = self.api.patch(ruta, json={"estado": estado})
            self.assertEqual(respuesta.json()["estado"], estado)
        final = self.api.patch(ruta, json={"estado": "ANULADA"})
        self.assertEqual(final.status_code, 409)

    def test_listar_filtra_por_estado(self):
        self._guardar()
        abiertas = self.api.get("/cotizaciones?estado=ABIERTA").json()
        self.assertTrue(all(c["estado"] == "ABIERTA" for c in abiertas))


if __name__ == "__main__":
    unittest.main()
