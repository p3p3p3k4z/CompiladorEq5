from transicion import *

class Estado:
    def __init__(self, id, es_final=False):
        self.id = id
        self.es_final = es_final
        self.transiciones = []

    def agregar_transicion(self, simbolo, estado_destino):
        self.transiciones.append(Transicion(simbolo, estado_destino))

    def obtener_transiciones(self):
        return self.transiciones

    def es_estado_final(self):
        return self.es_final

    def obtener_id(self):
        return self.id
