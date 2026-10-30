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