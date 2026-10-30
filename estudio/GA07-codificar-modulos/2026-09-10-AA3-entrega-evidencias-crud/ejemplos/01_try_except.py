"""try / except: que el programa no se cierre cuando algo falla.

Qué enseña: lo que la instructora explicó del bloque try-catch del botón Guardar.
"Intenta ejecutar este código; si ocurre un error, detente y pásale el control al bloque
catch para resolverlo sin que la aplicación se cierre."

Equivale en Java a:
    try {
        int edad = Integer.parseInt(txtEdad.getText());
        ... INSERT en MySQL ...
        JOptionPane.showMessageDialog(this, "Registro guardado");
    } catch (NumberFormatException e) {
        JOptionPane.showMessageDialog(this, "La edad debe ser un número");
    } catch (SQLException e) {
        JOptionPane.showMessageDialog(this, "Error con la base de datos");
    }

Cómo correrlo:
    python 01_try_except.py
"""

import sqlite3


def guardar_pasajero(conexion: sqlite3.Connection, documento: str, nombre: str, edad_texto: str):
    """Devuelve el mensaje que vería el usuario (el JOptionPane de Java)."""
    try:
        edad = int(edad_texto)  # puede fallar si escriben letras
        conexion.execute(
            "INSERT INTO pasajeros (documento, nombre, edad) VALUES (?, ?, ?)",
            (documento, nombre, edad),  # los ? evitan la inyección SQL (como PreparedStatement)
        )
        conexion.commit()
        return "Registro guardado con éxito"
    except ValueError:  # en Java: NumberFormatException
        return f"La edad debe ser un número (escribiste '{edad_texto}')"
    except sqlite3.IntegrityError:  # llave primaria repetida
        return f"Ya existe un pasajero con documento {documento}"
    except sqlite3.Error as error:  # en Java: SQLException (caída de la base, red...)
        return f"Error con la base de datos: {error}"


def main() -> None:
    conexion = sqlite3.connect(":memory:")  # base temporal en memoria, solo para la demo
    conexion.execute("CREATE TABLE pasajeros (documento TEXT PRIMARY KEY, nombre TEXT, edad INT)")

    print(guardar_pasajero(conexion, "101", "Carlos Fuentes", "28"))
    print(guardar_pasajero(conexion, "102", "José Meléndez", "veintiocho"))
    print(guardar_pasajero(conexion, "101", "Otro Carlos", "30"))

    conexion.close()
    print(guardar_pasajero(conexion, "103", "Ana Ruiz", "34"))  # la conexión ya está cerrada


if __name__ == "__main__":
    main()
