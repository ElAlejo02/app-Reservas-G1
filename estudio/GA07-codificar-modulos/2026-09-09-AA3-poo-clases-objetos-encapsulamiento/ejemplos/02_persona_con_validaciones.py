"""El ejercicio exacto de la clase (Persona + Main) traducido a Python, más input().

Qué enseña: el mismo programa que la instructora hizo en NetBeans, línea por línea:
crear la persona Carlos de 25 años, saludar, probar la regla del setter con -50,
modificar a "Carlos Alberto" de 26 y mostrar el resultado. Al final pide los datos
por teclado, que fue la pregunta que se hizo en clase ("¿cuál es el input?").

Equivale en Java a:
    Persona.java  -> private String nombre; private int edad; constructor; getters y
                     setters con if/else y System.out.println("Error: ...")
    Main.java     -> Persona p1 = new Persona("Carlos", 25); p1.saludar(); ...
    En Java el input se hace con Scanner: new Scanner(System.in).nextLine()

Cómo correrlo:
    python 02_persona_con_validaciones.py
"""


class Persona:
    def __init__(self, nombre: str, edad: int):
        self._nombre = nombre
        self._edad = edad

    # ---- getters ----
    def get_nombre(self) -> str:
        return self._nombre

    def get_edad(self) -> int:
        return self._edad

    # ---- setters con validación (igual que en clase) ----
    def set_nombre(self, nuevo_nombre: str) -> None:
        if nuevo_nombre is not None and nuevo_nombre.strip() != "":
            self._nombre = nuevo_nombre.strip()
        else:
            print("Error: el nombre no puede estar vacío")

    def set_edad(self, nueva_edad: int) -> None:
        if 0 < nueva_edad < 120:
            self._edad = nueva_edad
        else:
            print("Error: ingrese una edad desde 1 hasta 119")

    def saludar(self) -> None:
        print("Hola, mi nombre es " + self._nombre + " y tengo " + str(self._edad) + " años")


def main() -> None:
    p1 = Persona("Carlos", 25)  # en Java: Persona p1 = new Persona("Carlos", 25);
    print("--- Datos iniciales ---")
    p1.saludar()

    print("--- Regla de seguridad del setter ---")
    p1.set_edad(-50)  # muestra el error y NO cambia la edad
    p1.set_nombre("   ")  # tampoco deja un nombre vacío

    print("--- Modificación correcta ---")
    p1.set_nombre("Carlos Alberto")
    p1.set_edad(26)

    print("--- Consultar datos ---")
    print("Nombre actualizado:  " + p1.get_nombre())
    print("Edad actualizada:  " + str(p1.get_edad()))

    print("--- Resultado final ---")
    p1.saludar()

    print("--- Ahora con datos escritos por teclado ---")
    nombre = input("Escribe tu nombre: ")
    edad_texto = input("Escribe tu edad: ")
    # input() siempre devuelve texto (str). Para usarlo como número hay que convertirlo.
    edad = int(edad_texto) if edad_texto.isdigit() else 0
    p2 = Persona("Sin nombre", 1)
    p2.set_nombre(nombre)
    p2.set_edad(edad)
    p2.saludar()


if __name__ == "__main__":
    main()
