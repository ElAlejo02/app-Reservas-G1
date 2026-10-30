"""Primera aplicación móvil: la misma app de la clase (escribir el nombre y recibir la bienvenida).

Qué enseña: la sección 2 del taller GA8-AA2-EV01 ("crear la primera aplicación que
muestre algún mensaje"), hecha en Python con Flet en vez de Java con Android Studio.

Equivalencias con la clase (Android Studio, plantilla Empty Views Activity):
    activity_main.xml (LinearLayout vertical, centrado)  -> ft.Column centrada
    EditText "Ingrese su nombre completo"                -> ft.TextField
    Button "Conectar"                                    -> ft.FilledButton
    TextView del mensaje                                 -> ft.Text
    MainActivity.onCreate(...)                           -> función main(page)
    setOnClickListener + if/else                         -> on_click=conectar con if/else

Cómo correrlo:
    flet run 01_app_bienvenida.py              -> ventana del tamaño de un celular
    flet run --android 01_app_bienvenida.py    -> en tu celular con la app "Flet" (escanea el QR)
    flet build apk                             -> genera el .apk (ver README, sección 7)
"""

import flet as ft

AZUL_HYD = "#1F3A5F"


def main(page: ft.Page):
    page.title = "Reservas HyD"
    page.window.width = 390  # tamaño de un celular para probar en el PC
    page.window.height = 760
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 24

    nombre = ft.TextField(label="Ingrese su nombre completo", width=300, autofocus=True)
    estado = ft.Text("Esperando interacción…", color=ft.Colors.GREY_600)
    mensaje = ft.Text("", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def conectar(e):
        texto = (nombre.value or "").strip()
        if texto:  # validación correcta
            estado.value = "Conexión exitosa"
            estado.color = ft.Colors.GREEN_700
            mensaje.value = f"¡Bienvenido al sistema, {texto}!"
            mensaje.color = AZUL_HYD
        else:  # campo vacío
            estado.value = "Campo requerido vacío"
            estado.color = ft.Colors.RED_400
            mensaje.value = ""
        page.update()

    page.add(
        ft.Column(
            [
                ft.Icon(ft.Icons.HOTEL, size=64, color=AZUL_HYD),
                ft.Text("Bienvenido", size=28, weight=ft.FontWeight.BOLD, color=AZUL_HYD),
                nombre,
                ft.FilledButton(content="Conectar", icon=ft.Icons.LOGIN, on_click=conectar),
                estado,
                mensaje,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )
    )


if __name__ == "__main__":
    ft.run(main)
