"""Pantalla 2: gestión de usuarios (el segundo boceto que hizo el instructor).

Campos del boceto: código, nombre, tipo, teléfono y correo.
Botones del boceto: nuevo, guardar, modificar y eliminar.

El archivo está separado en tres partes para practicar el patrón MVC que
mencionó el instructor:
    MODELO      -> la clase Usuario y la lista que hace de "base de datos"
    CONTROLADOR -> funciones que validan y cambian los datos
    VISTA       -> los controles de Flet que ve el usuario

Cómo correrlo:
    flet run 02_gestion_usuarios.py
    flet run --web 02_gestion_usuarios.py
"""
from dataclasses import dataclass

import flet as ft

AZUL_HYD = "#1F3A5F"
ROLES = ["ADMIN", "ASESOR", "OPERACION", "COMERCIAL"]


# ---------------------------------------------------------------- MODELO
@dataclass
class Usuario:
    codigo: str
    nombre: str
    rol: str
    telefono: str
    correo: str


# Mientras no hay base de datos, una lista en memoria hace de tabla.
usuarios: list[Usuario] = [
    Usuario("U001", "Ana Pérez", "ASESOR", "3001234567", "ana@correo.com"),
    Usuario("U002", "Carlos Gómez", "OPERACION", "3007654321", "carlos@correo.com"),
]


# ----------------------------------------------------------- CONTROLADOR
def buscar(codigo: str) -> Usuario | None:
    return next((u for u in usuarios if u.codigo == codigo), None)


def validar(u: Usuario) -> str:
    """Devuelve el error encontrado o "" si todo está bien."""
    if not all([u.codigo, u.nombre, u.rol, u.correo]):
        return "Código, nombre, tipo y correo son obligatorios."
    if "@" not in u.correo:
        return "El correo no es válido."
    return ""


def guardar(u: Usuario) -> str:
    error = validar(u)
    if error:
        return error
    if buscar(u.codigo):
        return f"Ya existe un usuario con código {u.codigo}. Usa Modificar."
    # Regla que en HyD dañaba los LOOKUP: no puede haber correos repetidos.
    if any(x.correo.lower() == u.correo.lower() for x in usuarios):
        return "Ese correo ya está registrado."
    usuarios.append(u)
    return ""


def modificar(u: Usuario) -> str:
    error = validar(u)
    if error:
        return error
    actual = buscar(u.codigo)
    if not actual:
        return "No existe ese código."
    if any(x is not actual and x.correo.lower() == u.correo.lower() for x in usuarios):
        return "Ese correo ya lo tiene otro usuario."
    actual.nombre, actual.rol, actual.telefono, actual.correo = u.nombre, u.rol, u.telefono, u.correo
    return ""


def eliminar(codigo: str) -> str:
    actual = buscar(codigo)
    if not actual:
        return "No existe ese código."
    usuarios.remove(actual)
    return ""


# ----------------------------------------------------------------- VISTA
def main(page: ft.Page):
    page.title = "Reservas HyD | Gestión de usuarios"
    page.window.width = 420
    page.window.height = 800
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    codigo = ft.TextField(label="Código", width=150)
    nombre = ft.TextField(label="Nombre")
    rol = ft.Dropdown(label="Tipo", options=[ft.DropdownOption(r) for r in ROLES], width=220)
    telefono = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE)
    correo = ft.TextField(label="Correo", keyboard_type=ft.KeyboardType.EMAIL)
    mensaje = ft.Text("")

    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(t)) for t in ("Código", "Nombre", "Tipo")],
        rows=[],
    )

    def leer_formulario() -> Usuario:
        return Usuario(
            codigo=(codigo.value or "").strip().upper(),
            nombre=(nombre.value or "").strip(),
            rol=rol.value or "",
            telefono=(telefono.value or "").strip(),
            correo=(correo.value or "").strip(),
        )

    def cargar_en_formulario(u: Usuario):
        codigo.value, nombre.value, rol.value = u.codigo, u.nombre, u.rol
        telefono.value, correo.value = u.telefono, u.correo
        page.update()

    def refrescar_tabla():
        tabla.rows = [
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(u.codigo)), ft.DataCell(ft.Text(u.nombre)), ft.DataCell(ft.Text(u.rol))],
                on_select_change=lambda e, u=u: cargar_en_formulario(u),  # clic en la fila la carga arriba
            )
            for u in usuarios
        ]

    def mostrar(error: str, ok: str):
        mensaje.value = error or ok
        mensaje.color = ft.Colors.RED_400 if error else ft.Colors.GREEN_600
        refrescar_tabla()
        page.update()

    def nuevo(e):
        for campo in (codigo, nombre, telefono, correo):
            campo.value = ""
        rol.value = None
        mostrar("", "Formulario limpio.")

    def on_guardar(e):
        mostrar(guardar(leer_formulario()), "Usuario guardado.")

    def on_modificar(e):
        mostrar(modificar(leer_formulario()), "Usuario modificado.")

    def on_eliminar(e):
        mostrar(eliminar((codigo.value or "").strip().upper()), "Usuario eliminado.")

    def boton(texto, icono, accion):
        return ft.OutlinedButton(content=texto, icon=icono, on_click=accion, col={"xs": 6, "sm": 3})

    refrescar_tabla()
    page.add(
        ft.Row([ft.Icon(ft.Icons.MANAGE_ACCOUNTS, color=AZUL_HYD, size=36),
                ft.Text("GESTIÓN DE USUARIOS", size=20, weight=ft.FontWeight.BOLD, color=AZUL_HYD)]),
        codigo, nombre, rol, telefono, correo,
        # ResponsiveRow: en celular quedan 2 botones por fila y en pantalla ancha los 4 en una fila.
        ft.ResponsiveRow([
            boton("Nuevo", ft.Icons.ADD, nuevo),
            boton("Guardar", ft.Icons.SAVE, on_guardar),
            boton("Modificar", ft.Icons.EDIT, on_modificar),
            boton("Eliminar", ft.Icons.DELETE, on_eliminar),
        ]),
        mensaje,
        tabla,
    )


if __name__ == "__main__":
    ft.run(main)
