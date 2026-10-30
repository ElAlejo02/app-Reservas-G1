"""Módulo móvil: login y consulta de hoteles desde el celular (base para la GA8-AA2-EV02).

Qué enseña: una app móvil que NO tiene su propia base de datos, sino que consume la API
integrada de la GA8-AA1 (sistema_reservas). Es la misma arquitectura de la vida real:
la app del celular, la web y Postman hablan con el mismo backend.

Pantallas (navegación con rutas, como las actividades de Android):
    /login     -> usuario y contraseña (POST /api/auth/login)
    /hoteles   -> lista de hoteles con filtro por ciudad (GET /api/hoteles)

Cómo correrlo:
    1. Encender la API de la clase anterior, desde la carpeta
       2026-10-07-AA1-integrar-modulos/ejemplos/sistema_reservas:
           uvicorn app.main:app --host 0.0.0.0 --port 8080
    2. En otra terminal:
           flet run 02_app_hoteles_movil.py
    En el celular, la dirección de la API es la IP del PC en la red Wi-Fi (no 127.0.0.1):
           set API_URL=http://192.168.1.50:8080
"""

import os

import flet as ft
import httpx

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8080")
AZUL_HYD = "#1F3A5F"


def main(page: ft.Page):
    page.title = "Reservas HyD"
    page.window.width = 390
    page.window.height = 760
    sesion = {"usuario": "", "rol": ""}

    # ------------------------------------------------------------ pantalla de login
    def vista_login() -> ft.View:
        usuario = ft.TextField(label="Usuario", prefix_icon=ft.Icons.PERSON)
        clave = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        error = ft.Text("", color=ft.Colors.RED_400)

        def ingresar(e):
            try:
                r = httpx.post(
                    f"{API_URL}/api/auth/login",
                    json={"usuario": usuario.value or "", "contrasena": clave.value or ""},
                    timeout=5,
                )
            except httpx.HTTPError:
                error.value = "Sin conexión con el servidor"
                page.update()
                return
            if r.status_code == 200:
                sesion.update(usuario=r.json()["usuario"], rol=r.json()["rol"])
                page.navigate("/hoteles")
            else:
                error.value = "Usuario o contraseña incorrectos"
                page.update()

        return ft.View(
            route="/login",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            padding=28,
            controls=[
                ft.Icon(ft.Icons.HOTEL, size=56, color=AZUL_HYD),
                ft.Text("Reservas HyD", size=26, weight=ft.FontWeight.BOLD, color=AZUL_HYD),
                usuario,
                clave,
                ft.FilledButton(content="Ingresar", on_click=ingresar),
                error,
            ],
        )

    # ---------------------------------------------------------- pantalla de hoteles
    def vista_hoteles() -> ft.View:
        lista = ft.Column(spacing=8)
        ciudad = ft.TextField(label="Filtrar por ciudad", expand=True)

        def cargar(e=None):
            try:
                hoteles = httpx.get(f"{API_URL}/api/hoteles", timeout=5).json()
            except httpx.HTTPError:
                lista.controls = [ft.Text("Sin conexión con el servidor", color=ft.Colors.RED_400)]
                page.update()
                return
            filtro = (ciudad.value or "").strip().lower()
            lista.controls = [
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.APARTMENT, color=AZUL_HYD),
                        title=ft.Text(h["nombre"]),
                        subtitle=ft.Text(f"{h['ciudad']} · {h['estrellas']} estrellas"),
                        trailing=ft.Text(f"${h['tarifa_noche']:,.0f}"),
                    )
                )
                for h in hoteles
                if filtro in h["ciudad"].lower()
            ]
            page.update()

        cargar()
        return ft.View(
            route="/hoteles",
            padding=16,
            appbar=ft.AppBar(
                title=ft.Text("Hoteles"),
                actions=[
                    ft.TextButton(content="Salir", on_click=lambda e: page.navigate("/login"))
                ],
            ),
            controls=[
                ft.Text(f"Hola, {sesion['usuario']} ({sesion['rol']})", color=ft.Colors.GREY_700),
                ft.Row([ciudad, ft.IconButton(ft.Icons.SEARCH, on_click=cargar)]),
                lista,
            ],
        )

    # ------------------------------------------------------------------ enrutador
    def cambiar_ruta(e=None):
        page.views.clear()
        # Sin sesión iniciada, cualquier ruta lleva al login.
        if page.route == "/hoteles" and sesion["usuario"]:
            page.views.append(vista_hoteles())
        else:
            page.views.append(vista_login())
        page.update()

    page.on_route_change = cambiar_ruta
    cambiar_ruta()


if __name__ == "__main__":
    ft.run(main)
