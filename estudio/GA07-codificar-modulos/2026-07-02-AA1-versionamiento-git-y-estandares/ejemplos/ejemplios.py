class Habitacion:
    def __init__(self, numero, capacidad=2):
        self.numero = numero
        self.capacidad = capacidad

    def quien_soy(self):
        print("self es:", self)

    @classmethod
    def quien_es_cls(cls):
        print("cls es:", cls)

hab = Habitacion(301, 4)
hab.quien_soy()           # self es: <__main__.Habitacion object at 0x...>
Habitacion.quien_es_cls() # cls es: <class '__main__.Habitacion'>