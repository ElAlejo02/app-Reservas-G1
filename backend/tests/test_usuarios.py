"""Pruebas de registro, inicio de sesión y permisos."""

import unittest
import warnings

from app import seguridad
from app.repositorios import usuarios
from tests.test_api import hay_base_de_datos

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fastapi.testclient import TestClient

from app.main import app

ASESOR = "login.asesor@hyd.test"
ADMIN = "login.admin@hyd.test"
CLAVE = "Clave2026"


class PruebasClaves(unittest.TestCase):
    """No necesitan base de datos."""

    def test_la_clave_no_se_guarda_tal_cual(self):
        huella = seguridad.cifrar_clave(CLAVE)
        self.assertNotIn(CLAVE, huella)
        self.assertTrue(seguridad.clave_correcta(CLAVE, huella))
        self.assertFalse(seguridad.clave_correcta("Otra2026", huella))

    def test_token_de_ida_y_vuelta(self):
        token = seguridad.crear_token({"id_usuario": 7, "rol": "ASESOR"})
        self.assertEqual(seguridad.leer_token(token), 7)

    def test_token_alterado(self):
        token = seguridad.crear_token({"id_usuario": 7, "rol": "ASESOR"})
        with self.assertRaises(seguridad.NoAutenticadoError):
            seguridad.leer_token(token[:-2] + "xx")


@unittest.skipUnless(hay_base_de_datos(), "MySQL no está disponible")
class PruebasLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = TestClient(app)
        for correo in (ASESOR, ADMIN):
            usuarios.borrar(correo)
        cls.api.post(
            "/auth/registro",
            json={"nombre": "Asesor Login", "correo": ASESOR, "clave": CLAVE},
        )
        id_admin = cls.api.post(
            "/auth/registro",
            json={"nombre": "Admin Login", "correo": ADMIN, "clave": CLAVE},
        ).json()["id_usuario"]
        usuarios.actualizar(id_admin, {"rol": "ADMIN"})
        cls.id_admin = id_admin

    @classmethod
    def tearDownClass(cls):
        for correo in (ASESOR, ADMIN):
            usuarios.borrar(correo)

    def _token(self, correo):
        sesion = self.api.post(
            "/auth/login", json={"correo": correo, "clave": CLAVE}
        ).json()
        return {"Authorization": f"Bearer {sesion['access_token']}"}

    def test_registro_queda_como_asesor(self):
        yo = self.api.get("/auth/yo", headers=self._token(ASESOR)).json()
        self.assertEqual(yo["rol"], "ASESOR")
        self.assertNotIn("clave_hash", yo)

    def test_correo_repetido(self):
        respuesta = self.api.post(
            "/auth/registro",
            json={"nombre": "Repetido", "correo": ASESOR, "clave": CLAVE},
        )
        self.assertEqual(respuesta.status_code, 409)

    def test_clave_debil(self):
        for clave in ("corta1", "sololetras", "1234567890"):
            with self.subTest(clave=clave):
                respuesta = self.api.post(
                    "/auth/registro",
                    json={
                        "nombre": "Debil",
                        "correo": "debil@hyd.test",
                        "clave": clave,
                    },
                )
                self.assertEqual(respuesta.status_code, 422)

    def test_login_correcto(self):
        respuesta = self.api.post(
            "/auth/login",
            json={"correo": ASESOR.upper(), "clave": CLAVE},
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["token_type"], "bearer")

    def test_login_con_clave_mala_o_correo_inexistente(self):
        for correo, clave in ((ASESOR, "Mala2026"), ("nadie@hyd.test", CLAVE)):
            with self.subTest(correo=correo):
                respuesta = self.api.post(
                    "/auth/login", json={"correo": correo, "clave": clave}
                )
                self.assertEqual(respuesta.status_code, 401)
                self.assertEqual(
                    respuesta.json()["detail"], "Correo o clave incorrectos."
                )

    def test_sin_token_o_token_falso(self):
        self.assertEqual(self.api.get("/auth/yo").status_code, 401)
        falso = {"Authorization": "Bearer abc.def.ghi"}
        self.assertEqual(
            self.api.get("/auth/yo", headers=falso).status_code, 401
        )

    def test_solo_admin_ve_usuarios(self):
        asesor = self.api.get("/usuarios", headers=self._token(ASESOR))
        admin = self.api.get("/usuarios", headers=self._token(ADMIN))
        self.assertEqual(asesor.status_code, 403)
        self.assertEqual(admin.status_code, 200)

    def test_admin_no_se_quita_el_rol(self):
        respuesta = self.api.patch(
            f"/usuarios/{self.id_admin}",
            json={"rol": "ASESOR"},
            headers=self._token(ADMIN),
        )
        self.assertEqual(respuesta.status_code, 409)

    def test_usuario_inactivo_no_entra(self):
        token_asesor = self._token(ASESOR)
        id_asesor = self.api.get("/auth/yo", headers=token_asesor).json()[
            "id_usuario"
        ]
        cambio = self.api.patch(
            f"/usuarios/{id_asesor}",
            json={"activo": False},
            headers=self._token(ADMIN),
        )
        self.assertEqual(cambio.status_code, 200)
        try:
            # El token viejo deja de servir y tampoco puede volver a entrar.
            self.assertEqual(
                self.api.get("/auth/yo", headers=token_asesor).status_code,
                401,
            )
            login = self.api.post(
                "/auth/login", json={"correo": ASESOR, "clave": CLAVE}
            )
            self.assertEqual(login.status_code, 401)
        finally:
            usuarios.actualizar(id_asesor, {"activo": True})


if __name__ == "__main__":
    unittest.main()
