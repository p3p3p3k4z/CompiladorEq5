import os
import sys

base_path = os.path.abspath(os.path.dirname(__file__))

def cargar_datos(lineas):
    """Processes lines from a file and strips newline characters."""
    return [linea.strip('\n') for linea in lineas]

def cargar_archivo(ruta_relativa):
    """Loads a file and returns its lines."""
    archivo_cargado = os.path.join(base_path, ruta_relativa)
    if not os.path.exists(archivo_cargado):
        print(f"Error: File not found: {archivo_cargado}")
        sys.exit(1)
    try:
        with open(archivo_cargado, 'r') as file:
            return file.readlines()
    except IOError as e:
        print(f"Error reading file {archivo_cargado}: {e}")
        sys.exit(1)

# Load data from files
lineas_pReservadas = cargar_archivo('../../pruebas_sintactico/necesario/palabras_reservadas.txt')
lineas_simbolos = cargar_archivo('../../pruebas_sintactico/necesario/simbolos.txt')
lineas_tipos_dato = cargar_archivo('../../pruebas_sintactico/necesario/tipos_dato.txt')

# Process data
lista_pReservadas = cargar_datos(lineas_pReservadas)
lista_simbolos = cargar_datos(lineas_simbolos)
lista_tipo_datos = cargar_datos(lineas_tipos_dato)

# Combine lists
lista_pReservadas += lista_tipo_datos

# Debugging
# Debug the base path
print(f"Base path: {base_path}")

# Attempt to construct and load the file
archivo_cargado = os.path.join(base_path, '..', '..', 'pruebas_sintactico/necesario', 'palabras_reservadas.txt')
print(f"Attempting to load file from: {archivo_cargado}")

# Check if file exists
if not os.path.exists(archivo_cargado):
    print(f"Error: File not found: {archivo_cargado}")
    sys.exit(1)

# Read the file
try:
    with open(archivo_cargado, 'r') as file:
        lineas = file.readlines()
except IOError as e:
    print(f"Error reading file {archivo_cargado}: {e}")
    sys.exit(1)

