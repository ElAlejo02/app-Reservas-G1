"""Crea el primer administrador desde la terminal.

Uso, dentro de la carpeta backend y con el .venv activo:
    python -m app.crear_admin

La clave se escribe sin que se vea en pantalla y nunca queda guardada en
ningún archivo, solo su huella en la base de datos.
"""

from getpass import getpass

from pydantic import ValidationError

from app import autenticacion
from app.esquemas import NuevoUsuario
from app.servicios import ReglaNoCumplidaError


def main() -> None:
    print("Crear usuario ADMIN de Hoteles y Destinos\n")
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    clave = getpass("Clave (no se ve al escribir): ")
    if clave != getpass("Repita la clave: "):
        print("Las claves no coinciden.")
        return
    try:
        nuevo = NuevoUsuario(nombre=nombre, correo=correo, clave=clave)
        admin = autenticacion.registrar(nuevo, rol="ADMIN")
    except ValidationError as error:
        for detalle in error.errors():
            print("-", detalle["msg"].removeprefix("Value error, "))
        return
    except ReglaNoCumplidaError as error:
        print(error)
        return
    print(f"\nListo: {admin['nombre']} ({admin['correo']}) es ADMIN.")


if __name__ == "__main__":
    main()
