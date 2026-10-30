"""Punto de entrada del módulo de pasajeros de Hoteles y Destinos.

Para abrir la aplicación, desde la carpeta ``modulo_pasajeros``::

    python main.py

Proyecto : Hoteles y Destinos S.A.S. (SENA ADSO, ficha 3134707)
Evidencia: GA7-220501096-AA3-EV01
Equipo   : Angel Daniel Burbano Amaya, Laura María Vergara Mesa,
           David Alejandro Alzate
"""

from pasajeros.interfaz import VentanaPasajeros


def main() -> None:
    """Crea la ventana y la deja escuchando los clics del usuario."""
    ventana = VentanaPasajeros()
    # mainloop() es un ciclo infinito que espera eventos (clics, teclas)
    # hasta que el usuario cierra la ventana. Sin él, la ventana se
    # abriría y se cerraría en un instante.
    ventana.mainloop()


# Este "if" es verdadero solo cuando el archivo se ejecuta directamente
# (python main.py) y NO cuando otro archivo lo importa. Es el
# equivalente al "public static void main(String[] args)" de Java.
if __name__ == "__main__":
    main()
