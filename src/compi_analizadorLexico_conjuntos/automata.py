from estado import *
from transicion import *

class Automata:
    def __init__(self):
        self.head = None

    def encontrar_estado_final(self):
        nodo = self.head
        while nodo:
            if nodo.es_estado_final():
                return nodo.obtener_id()
            nodo = nodo.siguiente
        return None

    def buscar_nodo(self, num_estado):
        nodo = self.head
        while nodo:
            if nodo.obtener_id() == num_estado:
                return nodo
            nodo = nodo.siguiente
        return None
