"""La clase Persona de la clase, pasada a Python como Pasajero.

Qué enseña: atributos privados, constructor, getters y setters (con @property) y por qué
en Python se escriben menos. Es la primera parte del ejercicio de la instructora.

Equivale en Java a: la clase Persona del paquete del modelo, con
    private String codigo; private int edad; ...
    public Persona(...) {...}          <- "Insertar código > Constructor" en NetBeans
    public String getCodigo() {...}    <- "Insertar código > Getter y Setter"
    public void setEdad(int edad) {...}

Cómo correrlo:
    python 01_clase_pasajero.py
"""

GENEROS = ("Masculino", "Femenino", "Otro")


class Pasajero:
    """Pasajero de una reserva. Mismos campos del formulario de clase."""

    def __init__(self, documento: str, nombre: str, edad: int, genero: str):
        # Al asignar con self.edad = ... se ejecuta el setter de abajo y se valida.
        self.documento = documento
        self.nombre = nombre
        self.edad = edad
        self.genero = genero

    # ---- getter y setter de edad: aquí sí vale la pena porque validamos ----
    @property
    def edad(self) -> int:  # getter: en Java, public int getEdad()
        return self._edad

    @edad.setter
    def edad(self, valor: int) -> None:  # setter: en Java, public void setEdad(int edad)
        if not 0 <= valor <= 120:
            raise ValueError("La edad debe estar entre 0 y 120")
        self._edad = valor

    @property
    def genero(self) -> str:
        return self._genero

    @genero.setter
    def genero(self, valor: str) -> None:
        if valor not in GENEROS:
            raise ValueError(f"Género no válido: {valor}")
        self._genero = valor

    # documento y nombre no necesitan validación especial: atributos normales.
    # En Python NO se escriben getters y setters "por si acaso" como en Java.

    def es_menor(self) -> bool:
        return self.edad < 18

    def __repr__(self) -> str:
        return f"Pasajero({self.documento}, {self.nombre}, {self.edad}, {self.genero})"


def demo() -> None:
    ana = Pasajero("1020304050", "Ana Ruiz", 34, "Femenino")
    print(ana)
    print("Edad (getter):", ana.edad)

    ana.edad = 35  # setter
    print("Nueva edad:", ana.edad, "| ¿Menor?", ana.es_menor())

    try:
        ana.edad = 200  # el setter lo impide
    except ValueError as error:
        print("Error controlado:", error)


if __name__ == "__main__":
    demo()
