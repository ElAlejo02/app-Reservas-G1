class Proveedor:
    def __init__(self, razon_social, nombre_comercial, 
                 numero_documento, correo):
        self.razon_social = razon_social
        self.nombre_comercial = nombre_comercial
        self.numero_documento = numero_documento
        self.correo = correo
    
    def __str__(self):
        return f"{self.nombre_comercial}"

