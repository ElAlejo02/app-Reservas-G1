class Reserva:
    def __init__(self, codigo, origen, destino, check_in, check_out, hotel,
                 cantidad_habitaciones, cantidad_adultos, cantidad_ninos, titular):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.check_in = check_in
        self.check_out = check_out
        self.hotel = hotel
        self.cantidad_habitaciones = cantidad_habitaciones
        self.cantidad_adultos = cantidad_adultos
        self.cantidad_ninos = cantidad_ninos
        self.titular = titular
        self.estado = "Pendiente"

r1 = Reserva("HDMDE001", "Medellin", "Cartagena", "2026-10-10", "2026-10-14",
             "Hotel Caribe", 1, 2, 1, "Laura Vergara")
print(r1.titular)