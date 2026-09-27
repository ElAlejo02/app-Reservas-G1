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
