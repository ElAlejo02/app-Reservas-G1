class Reserva:
    def __init__(self, codigo_reserva, origen, destino, check_in, check_out, hotel):
        self.codigo_reserva = codigo_reserva
        self.origen = origen
        self.destino = destino
        self.check_in = check_in
        self.check_out = check_out
        self.hotel = hotel
        self.pasajeros = []
        self.estado = "Pendiente"

    def __str__(self):
        return f"{self.codigo_reserva} | {self.destino} | {self.cantidad_pasajeros()} | estado: {self.estado}"
    
    def titular(self):
        for pasajero in self.pasajeros:
            if pasajero.es_titular:
                return pasajero
        return None
    
    def adicionar_pasajero(self, pasajero):
        if pasajero.es_titular and self.titular() is not None:
                print("La reserva ya tiene titular")
                return
        self.pasajeros.append(pasajero)
        
    
    def cantidad_pasajeros(self):
        return len(self.pasajeros)
    
    def confirmar(self):
        if self.estado == "Cancelada":
            print(f"La reserva {self.codigo_reserva} no se puede confirmar porque está Cancelada")
            return
        self.estado = "Confirmada"
    
    def cancelar(self):
        self.estado = "Cancelada"