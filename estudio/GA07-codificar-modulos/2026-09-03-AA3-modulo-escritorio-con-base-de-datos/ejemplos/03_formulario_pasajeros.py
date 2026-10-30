"""Formulario de escritorio de pasajeros conectado a la base de datos (CRUD completo).

Qué enseña: el mismo ejercicio que la instructora hizo en NetBeans con Java Swing
(campos código, nombre, edad, género, botón Guardar y una tabla), hecho en Python con Flet
y guardando de verdad en la base de datos, más Modificar, Eliminar y Limpiar, que es lo
que pide la GA7-AA3-EV01.

Equivalencias con la clase:
    JFrame Form "FormularioPersona"   -> función main(page) de Flet
    JTextField txtCodigo / txtNombre  -> ft.TextField
    JSpinner jsEdad                   -> ft.TextField numérico
    JComboBox jcGenero                -> ft.Dropdown
    JButton jGuardar + ActionPerformed -> ft.FilledButton con on_click
    JTable + DefaultTableModel        -> ft.DataTable
    JOptionPane.showMessageDialog     -> mensaje de color debajo de los botones
    Clase Conexion (JDBC)             -> 02_repositorio_pasajeros.py (SQLAlchemy)

Cómo correrlo (desde esta carpeta, con el entorno virtual activo):
    flet run 03_formulario_pasajeros.py         -> ventana de escritorio
    flet run --web 03_formulario_pasajeros.py   -> en el navegador
Para usar MySQL en vez de SQLite, define antes DATABASE_URL (ver 02_repositorio_pasajeros.py).
"""

import importlib

import flet as ft

# El nombre del archivo empieza por un número, por eso se importa así.
repo = importlib.import_module("02_repositorio_pasajeros")

AZUL_HYD = "#1F3A5F"
GENEROS = ["Masculino", "Femenino", "Otro"]


def main(page: ft.Page):
    page.title = "Reservas HyD | Pasajeros"
    page.window.width = 760
    page.window.height = 720
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    repo.crear_tablas()

    # ------------------------------------------------------------ controles
    documento = ft.TextField(label="Documento", width=200)
    nombre = ft.TextField(label="Nombre completo", expand=True)
    edad = ft.TextField(
        label="Edad",
        width=120,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),  # solo deja escribir números
    )
    genero = ft.Dropdown(label="Género", width=200, options=[ft.DropdownOption(g) for g in GENEROS])
    mensaje = ft.Text("")
    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(t)) for t in ("Documento", "Nombre", "Edad", "Género")],
        rows=[],
    )

    # ------------------------------------------------------------ acciones
    def leer_formulario() -> tuple[str, str, int, str]:
        """Lee y valida los campos. Lanza ValueError con un mensaje claro."""
        doc = (documento.value or "").strip()
        nom = (nombre.value or "").strip()
        if not doc or not nom or not edad.value or not genero.value:
            raise ValueError("Todos los campos son obligatorios.")
        return doc, nom, int(edad.value), genero.value

    def mostrar(texto: str, es_error: bool = False):
        mensaje.value = texto
        mensaje.color = ft.Colors.RED_400 if es_error else ft.Colors.GREEN_700
        refrescar_tabla()
        page.update()

    def refrescar_tabla():
        tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p.documento)),
                    ft.DataCell(ft.Text(p.nombre)),
                    ft.DataCell(ft.Text(str(p.edad))),
                    ft.DataCell(ft.Text(p.genero)),
                ],
                on_select_change=lambda e, p=p: cargar(p),  # clic en la fila la sube al formulario
            )
            for p in repo.consultar_todos()
        ]

    def cargar(p):
        documento.value, nombre.value = p.documento, p.nombre
        edad.value, genero.value = str(p.edad), p.genero
        page.update()

    def limpiar(e=None):
        documento.value = nombre.value = edad.value = ""
        genero.value = None
        mostrar("Formulario limpio.")

    def ejecutar(accion, texto_ok: str):
        """Ejecuta una operación del repositorio y muestra el resultado."""
        try:
            accion()
            mostrar(texto_ok)
        except ValueError as error:
            mostrar(str(error), es_error=True)

    def on_guardar(e):
        ejecutar(lambda: repo.insertar(*leer_formulario()), "Pasajero guardado.")

    def on_modificar(e):
        ejecutar(lambda: repo.actualizar(*leer_formulario()), "Pasajero modificado.")

    def on_eliminar(e):
        ejecutar(lambda: repo.eliminar((documento.value or "").strip()), "Pasajero eliminado.")

    # --------------------------------------------------------------- vista
    refrescar_tabla()
    page.add(
        ft.Row(
            [
                ft.Icon(ft.Icons.PERSON_ADD, color=AZUL_HYD, size=34),
                ft.Text("REGISTRO DE PASAJEROS", size=22, weight="bold", color=AZUL_HYD),
            ]
        ),
        ft.Row([documento, nombre]),
        ft.Row([edad, genero]),
        ft.Row(
            [
                ft.FilledButton(content="Guardar", icon=ft.Icons.SAVE, on_click=on_guardar),
                ft.OutlinedButton(content="Modificar", icon=ft.Icons.EDIT, on_click=on_modificar),
                ft.OutlinedButton(content="Eliminar", icon=ft.Icons.DELETE, on_click=on_eliminar),
                ft.TextButton(content="Limpiar", icon=ft.Icons.CLEAR, on_click=limpiar),
            ],
            wrap=True,
        ),
        mensaje,
        ft.Text("Pasajeros guardados (clic en una fila para editarla)", color=ft.Colors.GREY_700),
        tabla,
    )


if __name__ == "__main__":
    ft.run(main)
