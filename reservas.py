
class Proveedor:
    def __init__(self, razon_social, nombre_comercial, numero_documento, correo):
        self.razon_social = razon_social
        self.nombre_comercial = nombre_comercial
        self.numero_documento = numero_documento
        self.correo = correo
    
    def __str__(self):
        return f"{self.nombre_comercial}"

class Hotel:
    def __init__(self, nombre, ciudad, direccion, categoria, correo, proveedor):
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
    def __init__(self, nombre, apellido, tipo_documento_identidad, numero_documento_identidad, fecha_nacimiento, pais, es_titular, celular, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_documento_identidad = tipo_documento_identidad
        self.numero_documento_identidad = numero_documento_identidad
        self.fecha_nacimiento = fecha_nacimiento
        self.pais = pais
        self.es_titular = es_titular
        self.celular = celular
        self.correo = correo
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} "

class Reserva:
    def __init__(self, codigo, origen, destino, check_in, check_out, hotel,
                 cantidad_habitaciones, cantidad_adultos, cantidad_ninos, titular):
        self.codigo_reserva = self.codigo_reserva
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

    def __str__(self):
        return f"{self.codigo_reserva} | {self.destino} | {self.titular} | {self.cantidad_pasajeros} | estado: {self.estado}"
    
    def cantidad_pasajeros(self):
        return self.cantidad_adultos + self.cantidad_ninos
    
    def confirmar(self):
        if self.estado == "Cancelada":
            print(f"La reserva {self.codigo_reserva} no se puede confirmar porque está Cancelada")
            return
        self.estado = "Confirmada"
    
    def cancelar(self):
        self.estado = "Cancelada"
        return self.estado
    
class Usuario:
    def __init__(self, nombre_usuario, contrasena, correo, rol):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.correo = correo
        self.rol = rol
    
    def __str__(self):
        return f"{self.nombre_usuario}"

r1 = Reserva("HDMDE001", "Medellin", "Cartagena", "2026-10-10", "2026-10-14",
             "Hotel Caribe", 1, 2, 1, "Laura Vergara")

