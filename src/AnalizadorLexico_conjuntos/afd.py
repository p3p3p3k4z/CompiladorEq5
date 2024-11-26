from automata import *
from utilidades import *

class AFD:
    def __init__(self, lista_inicial, abecedario, head):
        self.lista_inicial = lista_inicial
        self.abecedario = abecedario
        self.head = head
        self.conjunto_estados = []
        self.transiciones = []

    def construir_afd(self):
        letra1 = 105
        inicial = 65  # Valor ASCII para 'A'
        pila_edos = [self.lista_inicial]
        conjunto_estados = [(chr(inicial), self.lista_inicial)]
        transiciones_estado = []

        while pila_edos:
            estado = pila_edos.pop(0)
            estado.sort()
            nuevo_edo = self.get_mueve_r(estado, chr(letra1))

            if not self.existe_estado(nuevo_edo, conjunto_estados):
                if len(nuevo_edo) != 0:
                    inicial += 1
                    pila_edos.append(nuevo_edo)
                    conjunto_estados.append((chr(inicial), nuevo_edo))

            transiciones_estado.append(
                (self.get_letra(estado, conjunto_estados), chr(letra1), self.get_letra(nuevo_edo, conjunto_estados))
            )

            if transiciones_estado not in self.transiciones:
                self.transiciones.append(transiciones_estado)

        final = self.formatear_resultado(conjunto_estados)
        return final

    def formatear_resultado(self, conjunto_estados):
        final = []
        for aux_estado in conjunto_estados:
            transiciones_estado = [
                trans for trans in self.transiciones if trans[0] == aux_estado[0]
            ]
            aux_estado_con_transiciones = aux_estado + (transiciones_estado,)
            final.append(aux_estado_con_transiciones)
        return final

    def get_mueve_r(self, estado, letra):
        cerradura_aux = []
        for simbolo in letra + "l":
            aux1 = self.mueve(estado, simbolo)
            cerradura_aux += aux1
        edo = self.cerradura_e(cerradura_aux, "λ")
        resultado = unir_listas(edo, cerradura_aux)
        return resultado

    def cerradura_e(self, elems, letra):
        pila = elems[:]
        conjunto = []
        while pila:
            elemento = pila.pop()
            nodo = self.buscar_nodo(elemento)
            for transicion in nodo.obtener_transiciones():
                if transicion.obtener_simbolo() == letra:
                    estado_destino = transicion.obtener_estado_destino()
                    pila.append(estado_destino)
                    if estado_destino not in conjunto:
                        conjunto.append(estado_destino)
        conjunto.sort()
        return conjunto

    def mueve(self, elems, letra):
        pila = elems[:]
        conjunto = []
        while pila:
            elemento = pila.pop()
            nodo = self.buscar_nodo(elemento)
            for transicion in nodo.obtener_transiciones():
                if transicion.obtener_simbolo() == letra:
                    estado_destino = transicion.obtener_estado_destino()
                    if estado_destino not in conjunto:
                        conjunto.append(estado_destino)
        conjunto.sort()
        return conjunto

    def existe_estado(self, estado, lista_tuplas):
        for tupla in lista_tuplas:
            if estado == tupla[1]:
                return tupla[0]
        return None

    def get_letra(self, estado, lista_tuplas):
        for tupla in lista_tuplas:
            if estado == tupla[1]:
                return tupla[0]
        return '-'
