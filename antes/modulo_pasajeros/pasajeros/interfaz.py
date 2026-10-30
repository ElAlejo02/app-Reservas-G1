"""Ventana de escritorio (Tkinter) del módulo de pasajeros.

Cada botón es una historia de usuario: Guardar, Buscar, Modificar,
Eliminar y Limpiar.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

import pymysql

from pasajeros import repositorio
from pasajeros.modelo import Pasajero
from pasajeros.validaciones import TIPOS_DOCUMENTO, validar_pasajero

TITULO = "Hoteles y Destinos S.A.S. | Gestión de pasajeros"
TAMANO_VENTANA = "900x620"

CAMPOS = (
    ("nombre", "Nombre"),
    ("apellido", "Apellido"),
    ("tipo_documento", "Tipo de documento"),
    ("numero_documento", "Número de documento"),
    ("fecha_nacimiento", "Fecha de nacimiento (AAAA-MM-DD)"),
    ("pais", "País"),
    ("celular", "Celular"),
    ("correo", "Correo electrónico"),
)

COLUMNAS_TABLA = (
    ("numero_documento", "Documento", 110),
    ("tipo_documento", "Tipo", 50),
    ("nombre", "Nombre", 120),
    ("apellido", "Apellido", 120),
    ("fecha_nacimiento", "Nacimiento", 95),
    ("pais", "País", 90),
    ("celular", "Celular", 100),
    ("correo", "Correo", 190),
)

MENSAJE_SIN_CONEXION = (
    "No se pudo conectar con la base de datos.\n"
    "Revise que MySQL esté encendido y que los datos del archivo .env "
    "sean correctos."
)


class VentanaPasajeros(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TITULO)
        self.geometry(TAMANO_VENTANA)
        self.minsize(820, 560)

        self.entradas: dict[str, ttk.Entry | ttk.Combobox] = {}
        self.estado = tk.StringVar(value="Listo.")

        self._crear_encabezado()
        self._crear_formulario()
        self._crear_botones()
        self._crear_tabla()
        self._crear_barra_estado()
        self.refrescar_tabla()

    def _crear_encabezado(self) -> None:
        encabezado = ttk.Label(
            self,
            text="Gestión de pasajeros",
            font=("Segoe UI", 16, "bold"),
        )
        encabezado.pack(pady=(12, 4))

    def _crear_formulario(self) -> None:
        marco = ttk.LabelFrame(self, text="Datos del pasajero", padding=10)
        marco.pack(fill="x", padx=12, pady=6)

        for indice, (llave, texto) in enumerate(CAMPOS):
            fila, columna = divmod(indice, 2)  # 8 campos en 4 filas x 2
            ttk.Label(marco, text=texto).grid(
                row=fila, column=columna * 2, sticky="w", padx=4, pady=4
            )
            if llave == "tipo_documento":
                caja = ttk.Combobox(
                    marco,
                    values=list(TIPOS_DOCUMENTO),
                    state="readonly",
                    width=27,
                )
            else:
                caja = ttk.Entry(marco, width=30)
            caja.grid(
                row=fila,
                column=columna * 2 + 1,
                sticky="we",
                padx=4,
                pady=4,
            )
            self.entradas[llave] = caja

        self.entradas["pais"].insert(0, "Colombia")
        marco.columnconfigure(1, weight=1)
        marco.columnconfigure(3, weight=1)

    def _crear_botones(self) -> None:
        marco = ttk.Frame(self)
        marco.pack(pady=6)
        # Sin paréntesis: se entrega la función para que Tkinter la llame
        # al hacer clic, no se ejecuta todavía.
        acciones = (
            ("Guardar", self.guardar),
            ("Buscar", self.buscar),
            ("Modificar", self.modificar),
            ("Eliminar", self.eliminar),
            ("Limpiar", self.limpiar),
        )
        for columna, (texto, comando) in enumerate(acciones):
            ttk.Button(marco, text=texto, command=comando, width=14).grid(
                row=0, column=columna, padx=5
            )

    def _crear_tabla(self) -> None:
        marco = ttk.LabelFrame(self, text="Pasajeros registrados", padding=6)
        marco.pack(fill="both", expand=True, padx=12, pady=6)

        llaves = [llave for llave, _, _ in COLUMNAS_TABLA]
        self.tabla = ttk.Treeview(
            marco, columns=llaves, show="headings", height=10
        )
        for llave, titulo, ancho in COLUMNAS_TABLA:
            self.tabla.heading(llave, text=titulo)
            self.tabla.column(llave, width=ancho, anchor="w")

        barra = ttk.Scrollbar(
            marco, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

    def _crear_barra_estado(self) -> None:
        ttk.Label(
            self, textvariable=self.estado, relief="sunken", anchor="w"
        ).pack(fill="x", side="bottom")

    def _leer_formulario(self) -> dict[str, str]:
        return {llave: caja.get() for llave, caja in self.entradas.items()}

    def _llenar_formulario(self, pasajero: Pasajero) -> None:
        self.limpiar(mensaje=False)
        for llave, caja in self.entradas.items():
            valor = str(getattr(pasajero, llave))
            if isinstance(caja, ttk.Combobox):
                caja.set(valor)
            else:
                caja.delete(0, tk.END)
                caja.insert(0, valor)

    def _documento_escrito(self) -> str:
        return self.entradas["numero_documento"].get().strip().upper()

    def _avisar(self, mensaje: str) -> None:
        self.estado.set(mensaje)

    # Cada botón atrapa dos errores: ValueError (dato malo) y MySQLError
    # (sin base de datos). Así la ventana nunca se cierra de golpe.
    def guardar(self) -> None:
        """HU-01: registrar un pasajero nuevo."""
        try:
            pasajero = validar_pasajero(self._leer_formulario())
            repositorio.crear(pasajero)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
            return
        except pymysql.MySQLError:
            messagebox.showerror("Error de conexión", MENSAJE_SIN_CONEXION)
            return
        messagebox.showinfo(
            "Pasajero guardado",
            f"Se registró a {pasajero.nombre_completo()}.",
        )
        self._avisar(f"Guardado: {pasajero}")
        self.limpiar(mensaje=False)
        self.refrescar_tabla()

    def buscar(self) -> None:
        """HU-02: consultar un pasajero por número de documento."""
        documento = self._documento_escrito()
        if not documento:
            messagebox.showwarning(
                "Falta el documento",
                "Escriba el número de documento que desea buscar.",
            )
            return
        try:
            pasajero = repositorio.buscar_por_documento(documento)
        except pymysql.MySQLError:
            messagebox.showerror("Error de conexión", MENSAJE_SIN_CONEXION)
            return
        if pasajero is None:
            messagebox.showinfo(
                "Sin resultados",
                f"No existe un pasajero con el documento {documento}.",
            )
            return
        self._llenar_formulario(pasajero)
        self._avisar(f"Encontrado: {pasajero}")

    def modificar(self) -> None:
        """HU-04: actualizar los datos de un pasajero existente."""
        try:
            pasajero = validar_pasajero(self._leer_formulario())
            actualizado = repositorio.actualizar(pasajero)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
            return
        except pymysql.MySQLError:
            messagebox.showerror("Error de conexión", MENSAJE_SIN_CONEXION)
            return
        if not actualizado:
            messagebox.showinfo(
                "Sin cambios",
                "No existe un pasajero con el documento "
                f"{pasajero.numero_documento}. Use Guardar para crearlo.",
            )
            return
        messagebox.showinfo(
            "Pasajero modificado",
            f"Se actualizaron los datos de {pasajero.nombre_completo()}.",
        )
        self._avisar(f"Modificado: {pasajero}")
        self.refrescar_tabla()

    def eliminar(self) -> None:
        """HU-05: eliminar un pasajero, pidiendo confirmación."""
        documento = self._documento_escrito()
        if not documento:
            messagebox.showwarning(
                "Falta el documento",
                "Busque o seleccione el pasajero que desea eliminar.",
            )
            return
        confirmado = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que desea eliminar el pasajero {documento}?\n"
            "Esta acción no se puede deshacer.",
        )
        if not confirmado:
            return
        try:
            eliminado = repositorio.eliminar(documento)
        except pymysql.MySQLError:
            messagebox.showerror("Error de conexión", MENSAJE_SIN_CONEXION)
            return
        if not eliminado:
            messagebox.showinfo(
                "Sin resultados",
                f"No existe un pasajero con el documento {documento}.",
            )
            return
        messagebox.showinfo("Pasajero eliminado", "Registro eliminado.")
        self._avisar(f"Eliminado el documento {documento}.")
        self.limpiar(mensaje=False)
        self.refrescar_tabla()

    def limpiar(self, mensaje: bool = True) -> None:
        """Deja el formulario listo para otro registro.

        Con mensaje=False no tapa el aviso de quien lo llamó.
        """
        for caja in self.entradas.values():
            if isinstance(caja, ttk.Combobox):
                caja.set("")
            else:
                caja.delete(0, tk.END)
        self.entradas["pais"].insert(0, "Colombia")
        self.entradas["nombre"].focus()
        if mensaje:
            self._avisar("Formulario limpio.")

    def refrescar_tabla(self) -> None:
        """HU-03: listar todos los pasajeros en la tabla."""
        self.tabla.delete(*self.tabla.get_children())
        try:
            pasajeros = repositorio.listar()
        except pymysql.MySQLError:
            self._avisar("Sin conexión a la base de datos.")
            return
        for pasajero in pasajeros:
            valores = [
                getattr(pasajero, llave) for llave, _, _ in COLUMNAS_TABLA
            ]
            self.tabla.insert(
                "", tk.END, iid=pasajero.numero_documento, values=valores
            )
        self._avisar(f"{len(pasajeros)} pasajero(s) registrado(s).")

    def _al_seleccionar_fila(self, _evento: tk.Event) -> None:
        """Al hacer clic en una fila, carga ese pasajero."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        try:
            pasajero = repositorio.buscar_por_documento(seleccion[0])
        except pymysql.MySQLError:
            messagebox.showerror("Error de conexión", MENSAJE_SIN_CONEXION)
            return
        if pasajero:
            self._llenar_formulario(pasajero)
            self._avisar(f"Seleccionado: {pasajero}")
