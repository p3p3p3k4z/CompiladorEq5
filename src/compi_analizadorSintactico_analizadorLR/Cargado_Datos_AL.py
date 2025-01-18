import os

# Función para cargar un archivo
def cargar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as file:
            return [linea.strip('\n') for linea in file.readlines()]
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {ruta_archivo}: {e}")
        return []

# Inicialización de listas
lista_pReservadas = []
lista_simbolos = []
lista_tipo_datos = []

# Construir rutas absolutas para los archivos
ruta_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'necesario')
ruta_palabras_reservadas = os.path.join(ruta_data, 'palabras_reservadas.txt')
ruta_simbolos = os.path.join(ruta_data, 'simbolos.txt')
ruta_tipos_dato = os.path.join(ruta_data, 'tipos_dato.txt')

# Cargar los archivos
lista_pReservadas = cargar_archivo(ruta_palabras_reservadas)
lista_simbolos = cargar_archivo(ruta_simbolos)
lista_tipo_datos = cargar_archivo(ruta_tipos_dato)

# Depuración: imprimir resultados
#print("Palabras reservadas:", lista_pReservadas)
#print("Símbolos:", lista_simbolos)
#print("Tipos de datos:", lista_tipo_datos)