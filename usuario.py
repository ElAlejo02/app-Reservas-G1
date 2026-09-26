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
