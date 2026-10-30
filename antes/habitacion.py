class Habitacion:
    def __init__(self, hotel, tipo, categoria, tarifa_adulto, tarifa_nino):
        self.hotel = hotel
        self.tipo = tipo
        self.categoria = categoria
        self.tarifa_adulto = tarifa_adulto
        self.tarifa_nino = tarifa_nino

    def __str__(self):
        return f"{self.tipo} {self.categoria} en {self.hotel.nombre}"
    