"""Clase, objeto, estado, comportamiento, constructor y encapsulamiento.

Qué enseña: los seis conceptos de la clase con un ejemplo del sistema de reservas
(la habitación de un hotel), igual que la instructora los explicó con un carro y un celular.

Equivale en Java a: el ejercicio de clase con dos archivos, Persona.java (la clase) y
Main.java (public static void main, donde se hace new Persona("Carlos", 25)).
Aquí la clase y el "main" van en el mismo archivo para verlo completo.

Cómo correrlo:
    python 01_clases_y_objetos.py
"""


# CLASE = el molde o plano. No ocupa memoria con datos hasta que se crea un objeto.
class Habitacion:
    """Habitación de un hotel."""

    # CONSTRUCTOR = inicializa el objeto. En Java lleva el mismo nombre de la clase.
    def __init__(self, numero: str, tipo: str, tarifa_noche: float):
        # ESTADO = los atributos (lo que el objeto "sabe" de sí mismo).
        self.numero = numero  # str   -> en Java String
        self.tipo = tipo  # str
        self.tarifa_noche = tarifa_noche  # float -> en Java double (pasa por el setter)
        self.ocupada = False  # bool  -> en Java boolean

    # ENCAPSULAMIENTO: la tarifa no se puede poner en negativo ni en cero.
    @property
    def tarifa_noche(self) -> float:  # getter: solo lee
        return self._tarifa_noche

    @tarifa_noche.setter
    def tarifa_noche(self, nueva_tarifa: float) -> None:  # setter: guarda y revisa
        if nueva_tarifa <= 0:
            raise ValueError("La tarifa debe ser mayor que cero")
        self._tarifa_noche = nueva_tarifa

    # COMPORTAMIENTO = los métodos (lo que el objeto "sabe hacer").
    # "-> None" es el void de Java: hace su trabajo y no devuelve nada.
    def ocupar(self) -> None:
        if self.ocupada:
            print(f"  La habitación {self.numero} ya está ocupada")
            return
        self.ocupada = True

    def liberar(self) -> None:
        self.ocupada = False

    # Este método SÍ devuelve un valor (en Java: public double cotizar(int noches)).
    def cotizar(self, noches: int) -> float:
        return noches * self.tarifa_noche

    def describir(self) -> str:
        estado = "ocupada" if self.ocupada else "libre"
        return f"Habitación {self.numero} ({self.tipo}) · ${self.tarifa_noche:,.0f} · {estado}"


def main() -> None:
    # OBJETO = la instancia real, ocupa memoria. En Java: new Habitacion("101", ...)
    h101 = Habitacion("101", "Estándar", 250_000)
    h305 = Habitacion("305", "Suite", 480_000)

    print("Datos iniciales:")
    print(" ", h101.describir())
    print(" ", h305.describir())

    print("Comportamiento:")
    h101.ocupar()
    h101.ocupar()  # el método se protege solo
    print(" ", h101.describir())
    print(f"  Cotización 3 noches en la 305: ${h305.cotizar(3):,.0f}")

    print("Regla de seguridad del setter:")
    try:
        h305.tarifa_noche = -50  # igual que setEdad(-50) en la clase
    except ValueError as error:
        print("  Error:", error)
    h305.tarifa_noche = 500_000
    print("  Modificación correcta:", h305.describir())


if __name__ == "__main__":  # la "puerta de entrada", como public static void main
    main()
