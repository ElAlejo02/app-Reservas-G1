"""App de varias pantallas con navegación: lo que pide la evidencia GA6-AA3-EV02/EV03.

Mapa de navegación (navegación HÍBRIDA, la que recomendó el instructor):

    /login ──► /menu  (JERÁRQUICA: desde el menú entras a cada módulo y vuelves)
                 ├── /reservas              lista de reservas
                 │      └── /reservas/nueva  asistente de 3 pasos (LINEAL: siguiente / atrás)
                 ├── /hoteles
                 └── /usuarios

En Android Studio cada pantalla es una "actividad". En Flet cada pantalla es
una View con su ruta (route), igual que las direcciones de una página web.

Cómo correrlo:
    flet run 03_app_navegacion.py
    flet run --web 03_app_navegacion.py
    flet run --android 03_app_navegacion.py

Usuario de prueba: asesor / 1234
"""
from dataclasses import dataclass, field

import flet as ft

AZUL_HYD = "#1F3A5F"


# ------------------------------------------------------------ MODELO
@dataclass
class Reserva:
    codigo: str          # formato HyD: HD + ciudad de origen + consecutivo, ej. HDMDE001
    destino: str
    hotel: str
    check_in: str
    check_out: str
    pasajeros: list[str] = field(default_factory=list)
    estado: str = "Pendiente"


reservas = [
    Reserva("HDMDE001", "Cartagena", "Hotel Caribe", "2026-11-10", "2026-11-14", ["Ana Pérez", "Carlos Gómez"], "Confirmada"),
    Reserva("HDMDE002", "San Andrés", "Decameron Aquarium", "2026-12-01", "2026-12-05", ["Luis Mora"]),
]
HOTELES = {
    "Cartagena": ["Hotel Caribe", "Almirante Cartagena"],
    "San Andrés": ["Decameron Aquarium", "Sunrise Beach"],
    "Santa Marta": ["Irotama", "Zuana"],
}


def siguiente_codigo() -> str:
    return f"HDMDE{len(reservas) + 1:03d}"


# ------------------------------------------------------------- VISTA
def main(page: ft.Page):
    page.title = "Reservas HyD"
    page.window.width = 400
    page.window.height = 760
    page.theme = ft.Theme(color_scheme_seed=AZUL_HYD)

    # Datos del asistente "nueva reserva" mientras el usuario avanza por los pasos.
    borrador = {"paso": 1, "destino": None, "hotel": None, "check_in": "", "check_out": "", "pasajeros": ""}

    def barra(titulo: str, volver: bool = True) -> ft.AppBar:
        acciones = [ft.IconButton(ft.Icons.LOGOUT, tooltip="Salir", on_click=lambda e: page.navigate("/login"))]
        return ft.AppBar(title=ft.Text(titulo), bgcolor=AZUL_HYD, color=ft.Colors.WHITE,
                         automatically_imply_leading=volver, actions=acciones if volver else None)

    # ---------- Pantalla: login
    def vista_login() -> ft.View:
        usuario = ft.TextField(label="Usuario", prefix_icon=ft.Icons.PERSON)
        clave = ft.TextField(label="Contraseña", prefix_icon=ft.Icons.LOCK, password=True, can_reveal_password=True)
        error = ft.Text("", color=ft.Colors.RED_400)

        def ingresar(e):
            if (usuario.value or "").lower() == "asesor" and clave.value == "1234":
                page.navigate("/menu")
            else:
                error.value = "Usuario o contraseña incorrectos."
                page.update()

        return ft.View(
            route="/login",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=32,
            controls=[
                ft.Icon(ft.Icons.HOTEL, size=72, color=AZUL_HYD),
                ft.Text("INICIO DE SESIÓN", size=22, weight=ft.FontWeight.BOLD, color=AZUL_HYD),
                usuario, clave,
                ft.FilledButton(content="Ingresar", on_click=ingresar, width=400),
                error,
            ],
        )

    # ---------- Pantalla: menú principal (navegación jerárquica)
    def vista_menu() -> ft.View:
        def opcion(icono, titulo, detalle, ruta):
            return ft.Card(
                col={"xs": 12, "sm": 6},
                content=ft.ListTile(leading=ft.Icon(icono, color=AZUL_HYD), title=ft.Text(titulo),
                                    subtitle=ft.Text(detalle), on_click=lambda e: page.navigate(ruta)),
            )

        return ft.View(
            route="/menu",
            appbar=barra("Menú principal", volver=False),
            controls=[ft.ResponsiveRow([
                opcion(ft.Icons.BOOK_ONLINE, "Reservas", "Crear y consultar reservas", "/reservas"),
                opcion(ft.Icons.BED, "Hoteles", "Hoteles y tipos de habitación", "/hoteles"),
                opcion(ft.Icons.PEOPLE, "Usuarios", "Asesores y roles", "/usuarios"),
            ])],
        )

    # ---------- Pantalla: lista de reservas
    def vista_reservas() -> ft.View:
        colores = {"Confirmada": ft.Colors.GREEN_600, "Pendiente": ft.Colors.ORANGE_600, "Cancelada": ft.Colors.RED_400}
        filas = [
            ft.Card(content=ft.ListTile(
                leading=ft.Icon(ft.Icons.CIRCLE, color=colores.get(r.estado), size=14),
                title=ft.Text(f"{r.codigo} · {r.destino}"),
                subtitle=ft.Text(f"{r.hotel} | {r.check_in} a {r.check_out} | {len(r.pasajeros)} pax | {r.estado}"),
            ))
            for r in reservas
        ]
        return ft.View(
            route="/reservas",
            appbar=barra("Reservas"),
            floating_action_button=ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: nueva_reserva()),
            controls=filas,
            scroll=ft.ScrollMode.AUTO,
        )

    def nueva_reserva():
        borrador.update(paso=1, destino=None, hotel=None, check_in="", check_out="", pasajeros="")
        page.navigate("/reservas/nueva")

    # ---------- Pantalla: nueva reserva (navegación lineal en 3 pasos)
    def vista_nueva() -> ft.View:
        paso = borrador["paso"]
        aviso = ft.Text("", color=ft.Colors.RED_400)

        if paso == 1:
            destino = ft.Dropdown(label="Destino", value=borrador["destino"],
                                  options=[ft.DropdownOption(d) for d in HOTELES])
            entrada = ft.TextField(label="Check-in (AAAA-MM-DD)", value=borrador["check_in"])
            salida = ft.TextField(label="Check-out (AAAA-MM-DD)", value=borrador["check_out"])
            campos = [destino, entrada, salida]

            def guardar_paso():
                borrador.update(destino=destino.value, check_in=entrada.value, check_out=salida.value)
                return all([destino.value, entrada.value, salida.value])
        elif paso == 2:
            hotel = ft.Dropdown(label="Hotel", value=borrador["hotel"],
                                options=[ft.DropdownOption(h) for h in HOTELES.get(borrador["destino"], [])])
            campos = [ft.Text(f"Destino: {borrador['destino']}"), hotel]

            def guardar_paso():
                borrador.update(hotel=hotel.value)
                return bool(hotel.value)
        else:
            pax = ft.TextField(label="Pasajeros (separados por coma)", value=borrador["pasajeros"], multiline=True)
            resumen = ft.Text(f"{siguiente_codigo()} · {borrador['destino']} · {borrador['hotel']}\n"
                              f"{borrador['check_in']} a {borrador['check_out']}")
            campos = [resumen, pax]

            def guardar_paso():
                borrador.update(pasajeros=pax.value)
                return bool((pax.value or "").strip())

        def atras(e):
            guardar_paso()
            borrador["paso"] = max(1, paso - 1)
            mostrar_ruta()

        def siguiente(e):
            if not guardar_paso():
                aviso.value = "Completa los datos de este paso."
                page.update()
                return
            if paso < 3:
                borrador["paso"] = paso + 1
                mostrar_ruta()
            else:
                nombres = [p.strip() for p in borrador["pasajeros"].split(",") if p.strip()]
                reservas.append(Reserva(siguiente_codigo(), borrador["destino"], borrador["hotel"],
                                        borrador["check_in"], borrador["check_out"], nombres))
                page.navigate("/reservas")

        return ft.View(
            route="/reservas/nueva",
            appbar=barra(f"Nueva reserva · paso {paso} de 3"),
            padding=24,
            controls=[
                ft.ProgressBar(value=paso / 3, color=AZUL_HYD),
                *campos,
                aviso,
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.OutlinedButton(content="Atrás", icon=ft.Icons.ARROW_BACK, on_click=atras, disabled=paso == 1),
                        ft.FilledButton(content="Confirmar" if paso == 3 else "Siguiente", on_click=siguiente),
                    ],
                ),
            ],
        )

    def vista_simple(ruta: str, titulo: str, texto: str) -> ft.View:
        return ft.View(route=ruta, appbar=barra(titulo), padding=24, controls=[ft.Text(texto)])

    # ---------- Enrutador: decide qué pantallas apilar según la ruta
    def mostrar_ruta(e=None):
        ruta = page.route if page.route not in ("", "/") else "/login"
        page.views.clear()
        if ruta == "/login":
            page.views.append(vista_login())
        else:
            page.views.append(vista_menu())       # el menú queda debajo: la flecha "atrás" vuelve a él
            if ruta.startswith("/reservas"):
                page.views.append(vista_reservas())
            if ruta == "/reservas/nueva":
                page.views.append(vista_nueva())
            if ruta == "/hoteles":
                page.views.append(vista_simple(ruta, "Hoteles", "Aquí irá el CRUD de hoteles y habitaciones."))
            if ruta == "/usuarios":
                page.views.append(vista_simple(ruta, "Usuarios", "Aquí va la pantalla de 02_gestion_usuarios.py."))
        page.update()

    async def al_volver(e: ft.ViewPopEvent):
        # Flecha "atrás" del AppBar o botón atrás del celular: se quita la pantalla de arriba.
        page.views.remove(e.view)
        await page.push_route(page.views[-1].route)

    page.on_route_change = mostrar_ruta
    page.on_view_pop = al_volver
    mostrar_ruta()


if __name__ == "__main__":
    ft.run(main)
