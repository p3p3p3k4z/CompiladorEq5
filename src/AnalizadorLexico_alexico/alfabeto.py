import re

class Alfabeto:
    def __init__(self, incluir_mayusculas=True, incluir_minusculas=True, incluir_digitos=True):
        # Inicializamos el conjunto del alfabeto y las configuraciones
        self.alfabeto = set()
        self.incluir_mayusculas = incluir_mayusculas
        self.incluir_minusculas = incluir_minusculas
        self.incluir_digitos = incluir_digitos

    def agregar_alfabeto_estandar(self):
        # Agrega letras mayúsculas y minúsculas al alfabeto si está habilitado
        if self.incluir_mayusculas:
            self.alfabeto.update(chr(i) for i in range(65, 91))
        if self.incluir_minusculas:
            self.alfabeto.update(chr(i) for i in range(97, 123))
        
    def agregar_digitos(self):
        # Agrega dígitos al alfabeto si está habilitado
        if self.incluir_digitos:
            self.alfabeto.update(str(i) for i in range(10))

    # Función para generar el alfabeto a partir de las líneas del archivo
    def generar_alfabeto(lineas):
        alfabeto = set()
        for linea in lineas:
            # Buscamos las líneas que comienzan con "alfabetoX:"
            match = re.match(r'^alfabeto(\d+): (.+)$', linea)
            if match:
                numero_alfabeto = match.group(1)
                contenido = match.group(2)
                # Si contiene "letras", agregamos todas las letras del alfabeto
                if contenido == 'letras':
                    alfabeto.update('l')
                   #alfabeto.update(set(chr(i) for i in range(65, 91)))
                   #alfabeto.update(set(chr(i) for i in range(97, 123)))
                # Si contiene "digitos", agregamos los dígitos del 0 al 9
                elif contenido == 'digitos':
                    #alfabeto.update(set(str(i) for i in range(10)))
                    alfabeto.update('d')
                # De lo contrario, agregamos las letras únicas
                else:
                    alfabeto.update(set(contenido))
        return sorted(alfabeto)
    
    def obtener_alfabeto_como_cadena(self):
        # Retorna el alfabeto generado como una cadena
        return ''.join(sorted(self.alfabeto))
    
    def agregar_caracter(self, caracter):
        # Método para agregar caracteres individuales
        self.alfabeto.add(caracter)

    def eliminar_caracter(self, caracter):
        # Método para eliminar caracteres individuales
        self.alfabeto.discard(caracter)

    def reiniciar_alfabeto(self):
        # Reinicia el alfabeto a vacío
        self.alfabeto.clear()
'''
# Ejemplo de uso:
lineas = [
    "alfabeto1: letras",
    "alfabeto2: digitos",
    "alfabeto3: abcxyz"
]

generador = AlfabetoGenerator(incluir_mayusculas=True, incluir_minusculas=False)
alfabeto = generador.generar_alfabeto(lineas)
print("Alfabeto como lista ordenada:", alfabeto)
print("Alfabeto como cadena:", generador.obtener_alfabeto_como_cadena())

# Agregando y eliminando caracteres
generador.agregar_caracter('@')
print("Alfabeto después de agregar '@':", generador.obtener_alfabeto_como_cadena())
generador.eliminar_caracter('@')
print("Alfabeto después de eliminar '@':", generador.obtener_alfabeto_como_cadena())
'''
