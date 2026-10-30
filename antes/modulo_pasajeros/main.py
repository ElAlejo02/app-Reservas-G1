"""Abre la ventana de pasajeros:  python main.py"""

from pasajeros.interfaz import VentanaPasajeros


def main() -> None:
    ventana = VentanaPasajeros()
    ventana.mainloop()


if __name__ == "__main__":
    main()
