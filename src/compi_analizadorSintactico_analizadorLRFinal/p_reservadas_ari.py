import re
archivo_codigo = '/home/ari/Escritorio/Lexico/prueba2'
archivo_palabras_reservadas = '/home/ari/Escritorio/Lexico/palabras_reservadas'

# Leer las palabras reservadas desde txt
archivo='/home/ari/Escritorio/Lexico/palabras_reservadas'
def cargar_palabras_reservadas(archivo):
    with open(archivo, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Expresión regular
def crear_patron(palabras_reservadas):
    return r'\b(' + '|'.join(palabras_reservadas) + r')\b'

def encontrar_palabras_reservadas(archivo_codigo, archivo_palabras_reservadas):
    # Cargar las palabras reservadas
    palabras_reservadas = cargar_palabras_reservadas(archivo_palabras_reservadas)
    
    # Crear la expresión regular
    patron_palabras_reservadas = crear_patron(palabras_reservadas)
    
    # Leer el código C desde el txt
    with open(archivo_codigo, 'r') as file:
        codigo = file.read()
    
    # Encontrar todas las palabras reservadas en el código
    coincidencias = re.findall(patron_palabras_reservadas, codigo)
    
    # Eliminar palabras duplicadas y retornar como lista
    coincidencias_unicas = set(coincidencias)
    return list(coincidencias_unicas)

archivo_codigo = '/home/ari/Escritorio/Lexico/prueba2'
archivo_palabras_reservadas = '/home/ari/Escritorio/Lexico/palabras_reservadas'
palabras_reservadas_encontradas = encontrar_palabras_reservadas(archivo_codigo, archivo_palabras_reservadas)
print("Palabras reservadas encontradas:", palabras_reservadas_encontradas)
