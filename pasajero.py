
class Proveedor:
    def __init__(self, razon_social, nombre_comercial, 
                 numero_documento, correo):
        self.razon_social = razon_social
        self.nombre_comercial = nombre_comercial
        self.numero_documento = numero_documento
        self.correo = correo
    
    def __str__(self):
        return f"{self.nombre_comercial}"

class Hotel:
    def __init__(self, nombre, ciudad, direccion, categoria, 
                 correo, proveedor):
        self.nombre = nombre
        self.ciudad = ciudad
        self.direccion = direccion
        self.categoria = categoria
        self.correo = correo
        self.proveedor = proveedor
        self.estado = "Activo"

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"


class Habitacion:
    def __init__(self, hotel, tipo, categoria, tarifa_adulto, tarifa_nino):
        self.hotel = hotel
        self.tipo = tipo
        self.categoria = categoria
        self.tarifa_adulto = tarifa_adulto
        self.tarifa_nino = tarifa_nino

    def __str__(self):
        return f"{self.tipo} {self.categoria} en {self.hotel.nombre}"
    
class Pasajero:
    def __init__(self, nombre, apellido, tipo_documento, 
                 numero_documento, fecha_nacimiento, pais, es_titular, celular, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.fecha_nacimiento = fecha_nacimiento
        self.pais = pais
        self.es_titular = es_titular
        self.celular = celular
        self.correo = correo
        
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

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
        
    
class Usuario:
    def __init__(self, nombre_usuario, contrasena, correo, rol):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.correo = correo
        self.rol = rol
    
    def __str__(self):
        return f"{self.nombre_usuario}"

#Objetos:

proveedor = Proveedor("Inversiones Caribe S.A.S.", "Caribe Hoteles",
                      "900111222", "comercial@caribehoteles.com")

hotel = Hotel("Hotel Caribe", "Cartagena", "Bocagrande Cra 1", 4,
              "reservas@hotelcaribe.com", proveedor)

laura = Pasajero("Laura", "Vergara", "CC", "1036000000", "2000-05-12",
                 "Colombia", True, "3001234567", "laura@correo.com")

daniel = Pasajero("Daniel", "Burbano", "CC", "1036111111", "1999-08-20",
                 "Colombia", False, "3007654321", "angel@correo.com")

r1 = Reserva("HDMDE001", "Medellin", "Cartagena", "2026-10-10",
             "2026-10-14", hotel)

r1.adicionar_pasajero(laura)
r1.adicionar_pasajero(daniel)
r1.confirmar()
print(r1)
print(r1.hotel.proveedor)
