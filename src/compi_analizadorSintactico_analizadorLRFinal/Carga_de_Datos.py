# Función para cargar los datos de la carpeta Data que 
def cargar_palabras_reservadas(lineas):
    for linea in lineas:
        lista_pReservadas.append(linea.strip('\n'))
        
def cargar_simbolos(lineas):
    for linea in lineas:
        lista_simbolos.append(linea.strip('\n'))

def cargar_tipo_datos(lineas):
    for linea in lineas:
        lista_tipo_datos.append(linea.strip('\n'))
    
    

# Leer el archivo de entrada
archivo_cargado = 'D:\Sistemas\Proyect_Comp_Java\Proyecto_compilador\Datos\Palabras_Reservadas.txt'
with open(archivo_cargado, 'r') as file:
    lineas = file.readlines()
    
lista_pReservadas = []
cargar_palabras_reservadas(lineas)

archivo_cargado = 'D:\Sistemas\Proyect_Comp_Java\Proyecto_compilador\Datos\simbolos.txt'
with open(archivo_cargado, 'r') as file:
    lineas = file.readlines()
    
lista_simbolos = []
cargar_simbolos(lineas)

archivo_cargado = 'D:\Sistemas\Proyect_Comp_Java\Proyecto_compilador\Datos\Tipos_de_Datos.txt'
with open(archivo_cargado, 'r') as file:
    lineas = file.readlines()
    
lista_tipo_datos = []
cargar_tipo_datos(lineas)

#unimos la lista de tipos de datos al de palabras reservadas
lista_pReservadas = lista_pReservadas + lista_tipo_datos

for pReservada in lista_pReservadas:
    print(pReservada)