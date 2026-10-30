"""Pantalla 1: inicio de sesión del sistema de reservas.

Equivale a la primera "actividad" que el instructor creó en Android Studio
(activity_main.xml + MainActivity.java), pero escrita en Python con Flet.

Cómo correrlo (con el entorno virtual activo):
    flet run 01_login.py            -> ventana de escritorio
    flet run --web 01_login.py      -> en el navegador
    flet run --android 01_login.py  -> en tu celular con la app "Flet" (escanea el QR)

Usuario de prueba: asesor / 1234
"""
import flet as ft

# Datos de prueba. En el proyecto real esto vendrá de la tabla Usuarios de la base de datos.
USUARIOS_PRUEBA = {"asesor": "1234", "admin": "admin"}

AZUL_HYD = "#1F3A5F"


def main(page: ft.Page):
    # 1. Configuración de la "pantalla" (lo que en Android es el contenedor principal).
    page.title = "Reservas HyD | Inicio de sesión"
    page.window.width = 400   # tamaño parecido a un celular para probar en escritorio
    page.window.height = 720
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 24

    # 2. Controles (en Android serían TextView, EditText y Button dentro del XML).
    usuario = ft.TextField(label="Usuario", prefix_icon=ft.Icons.PERSON, width=300, autofocus=True)
    clave = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,              # oculta lo que se escribe
        can_reveal_password=True,   # ícono de ojo para mostrarla
        width=300,
    )
    mensaje = ft.Text(value="", color=ft.Colors.RED_400)

    # 3. Evento del botón (en Android sería el setOnClickListener en el .java).
    def ingresar(e):
        if not usuario.value or not clave.value:
            mensaje.value = "Escribe usuario y contraseña."
        elif USUARIOS_PRUEBA.get(usuario.value.strip().lower()) == clave.value:
            mensaje.color = ft.Colors.GREEN_600
            mensaje.value = f"Bienvenido, {usuario.value}."
        else:
            mensaje.color = ft.Colors.RED_400
            mensaje.value = "Usuario o contraseña incorrectos."
        page.update()  # redibuja la pantalla con el mensaje nuevo

    clave.on_submit = ingresar  # Enter en la contraseña también ingresa

    # 4. Layout: una columna vertical, como un LinearLayout vertical en Android.
    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.Icon(ft.Icons.HOTEL, size=72, color=AZUL_HYD),
                ft.Text("INICIO DE SESIÓN", size=22, weight=ft.FontWeight.BOLD, color=AZUL_HYD),
                usuario,
                clave,
                ft.FilledButton(content="Ingresar", width=300, on_click=ingresar,
                                style=ft.ButtonStyle(bgcolor=AZUL_HYD)),
                mensaje,
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
