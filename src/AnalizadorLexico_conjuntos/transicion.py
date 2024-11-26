class Transicion:
    def __init__(self, simbolo, estado_destino):
        self.simbolo = simbolo
        self.estado_destino = estado_destino

    def obtener_simbolo(self):
        return self.simbolo

    def obtener_estado_destino(self):
        return self.estado_destino
