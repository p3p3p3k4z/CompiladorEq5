import re
from coleccion_canonica import main as main
import PyS  # Importa el módulo PyS

def leer_reglas(ruta_archivo):
    """
    Lee las reglas de un archivo y las guarda como 'variable: producción :rX'.
    """
    reglas = []
    contador = 1  # Contador para el índice de las reglas

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        
        # Filtrar las reglas después de '->'
        for linea in lineas:
            linea = linea.strip()
            if '->' in linea:
                # Dividir en variable y producción
                variable, produccion = linea.split('->')
                variable = variable.strip()
                produccion = produccion.strip()
                
                # Reemplazar cualquier versión extraña de λ (por ejemplo, 'Î»') por 'λ'
                produccion = produccion.replace('Î»', 'λ').replace('λ', 'λ')
                
                # Guardar la regla en el formato 'variable: producción :rX'
                regla = f"{variable}: {produccion} :r{contador}"
                reglas.append(regla)
                contador += 1
    
    #print("\nReglas leídas del archivo (formato 'variable: producción :rX'):")
    #for regla in reglas:
     #   print(f"Regla: {regla}")
    
    return reglas

def ejecutar_coleccion_canonica(ruta_archivo):
    """
    Ejecuta el programa de colección canónica utilizando un archivo predefinido.
    """
    # Llamamos a la función main del módulo coleccion_canonica
    lista_estados = main(ruta_archivo)
    
    # Extraer solo los estados que comienzan con 'I'
    estados_extraidos = extraer_estados(lista_estados)
    
    # Filtrar los estados que contienen el fragmento con '•' al final
    estados_con_punto = filtrar_estados_con_punto(estados_extraidos)
    
    return estados_con_punto

def extraer_estados(lista_estados):
    """
    Extrae los estados de una lista de estados, que están en el formato:
    Estado: ['I10', [['L', [',', 'id', 'L', '•']]]]
    """
    estados_encontrados = []
    
    # Iteramos sobre cada estado en la lista
    for estado in lista_estados:
        # Convertimos cada estado en una cadena para aplicar la búsqueda de los patrones
        estado_str = str(estado)
        
        # Expresión regular para encontrar estados que comienzan con 'I' y tienen el formato adecuado
        patron_estado = r"Estado: \['I\d+', .*\]"
        
        # Buscar las coincidencias
        estados_encontrados.extend(re.findall(patron_estado, estado_str))
    
    return estados_encontrados

def filtrar_estados_con_punto(estados):
    """
    Filtra las sublistas que contienen '•' como único elemento o como el último elemento de cualquier sublista en un estado.
    """
    estados_con_punto = {}

    for estado in estados:
        # Convertir el estado a cadena para facilitar el análisis
        estado_str = str(estado)
        
        # Buscar el identificador del estado
        estado_id_match = re.search(r"I\d+", estado_str)
        if not estado_id_match:
            continue
        estado_id = estado_id_match.group(0)
        
        # Inicializar una lista para almacenar las sublistas válidas
        sublistas_con_punto = []
        
        # Expresión regular para capturar transiciones completas
        patron_transiciones = r"\['[A-Za-z]', \[(.*?)\]\]"
        
        # Buscar todas las transiciones en el estado
        transiciones = re.findall(patron_transiciones, estado_str)
        
        for transicion in transiciones:
            # Dividir los elementos de la lista interna de la transición
            elementos = eval(f"[{transicion}]")
            # Verificar si el último elemento es '•'
            if elementos and elementos[-1] == '•':
                # Aquí incluimos la lista completa de la transición con el '•'
                sublistas_con_punto.append([elementos])  # Envolvemos el fragmento completo en una lista
        
        # Si se encontraron sublistas válidas, asociarlas con el identificador del estado
        if sublistas_con_punto:
            estados_con_punto[estado_id] = sublistas_con_punto
    
    return estados_con_punto

def formatear_estados(estados_con_punto):
    """
    Crea una nueva lista con el formato solicitado (por ejemplo, I3:float, I4:int, etc.).
    """
    nueva_lista = {}

    for estado_id, transiciones in estados_con_punto.items():
        for transicion in transiciones:
            # Tomamos el primer (y único) elemento de la lista de la transición
            transicion_lista = transicion[0]
            
            # Si la transición tiene solo el marcador '•', la reemplazamos por 'λ'
            if len(transicion_lista) == 1 and transicion_lista[0] == '•':
                transicion_formateada = 'λ'
            else:
                # Eliminamos el '•' al final, si está presente
                if transicion_lista[-1] == '•':
                    transicion_lista = transicion_lista[:-1]  # Elimina el último elemento
                
                # Unimos los elementos de la transición con espacios
                transicion_formateada = ' '.join(transicion_lista)
            
            # Asegurarnos de que el símbolo 'λ' sea consistente
            transicion_formateada = transicion_formateada.replace('Î»', 'λ').replace('λ', 'λ')
            
            # Añadimos el estado con su transición formateada
            nueva_lista[estado_id] = transicion_formateada
    
    #print("\nNueva lista con las transiciones formateadas:")
    #for estado_id, transicion in nueva_lista.items():
        #print(f"{estado_id}:{transicion}")
    
    return nueva_lista

def comparar_transiciones_con_siguientes(nueva_lista, reglas, datos_pys):
    """
    Compara las transiciones contenidas en 'nueva_lista' con las producciones almacenadas en 'reglas'.
    Al encontrar una coincidencia, asigna solo el valor de r y agrega los elementos de 'siguientes' 
    asociados al 'no_terminal' correspondiente.
    """
    print("\nComparando las transiciones con las reglas del archivo y agregando 'siguientes'...")
    coincidencias = {}  # Almacenar coincidencias con r y los siguientes

    for estado_id, transicion in nueva_lista.items():
        for regla in reglas:
            # Dividir regla en variable, producción y r
            match = re.match(r"(.*?):\s(.*?)\s:r(\d+)", regla)
            if not match:
                continue
            variable, produccion, r = match.groups()
            
            if transicion == produccion:
                # Buscar los 'siguientes' correspondientes al 'variable' en datos_pys
                siguientes = set()  # Usar un conjunto para evitar duplicados
                for no_terminal, primeros, sigs in datos_pys:
                    if no_terminal == variable:
                        siguientes.update(sigs)
                
                # Convertir los siguientes a una cadena ordenada y unida por espacios
                siguientes_str = " ".join(sorted(siguientes))
                
                # Almacenar la coincidencia con el formato deseado
                coincidencias[estado_id] = f"r{r} :{siguientes_str}"
    
    return coincidencias

def maint(opcion):
    coincidencias_lista = []
    
    # Establecer la ruta del archivo según la opción
    if opcion == 1:
        ruta_archivo = r"Gramatica1.txt"
    elif opcion == 2:
        ruta_archivo = r"gramatica2.txt"
    elif opcion == 3:
        ruta_archivo = r"gramatica3.txt"
    elif opcion == 4:
        ruta_archivo = r"gramatica4.txt"
    elif opcion == 5:
        ruta_archivo = r"gramatica5.txt"
    else:
        print("Opción no válida. Usando ruta por defecto.")
        ruta_archivo = r"gramatica2.txt"  # Ruta por defecto en caso de opción no válida
    
    # Ejecutar PyS para obtener los primeros y siguientes
    print("\n=== Ejecutando PyS ===")
    datos_pys = PyS.mainPyS(ruta_archivo)  # Llamamos al módulo PyS con la misma ruta del archivo
    
    # Mostrar los resultados de PyS
    print("\nResultados de PyS (Primeros y Siguientes):")
    for no_terminal, primeros, siguientes in datos_pys:
        print(f"No Terminal: {no_terminal}")
        print(f"Primeros: {primeros}")
        print(f"Siguientes: {siguientes}")
        print("-" * 40)
    
    # Ejecutar la colección canónica
    print("\n=== Ejecutando colección canónica ===")
    lista_estados = ejecutar_coleccion_canonica(ruta_archivo)
    
    # Crear la nueva lista con el formato solicitado
    nueva_lista = formatear_estados(lista_estados)
    
    # Leer las reglas del archivo
    reglas = leer_reglas(ruta_archivo)
    
    # Comparar las transiciones con las reglas y agregar los 'siguientes'
    coincidencias = comparar_transiciones_con_siguientes(nueva_lista, reglas, datos_pys)
    
    # Imprimir coincidencias finales
    print("\nCoincidencias encontradas (estado: r):")
    for estado_id, r in coincidencias.items():
        coincidencia_formateada = f"{estado_id}: {r}"  # Formatear el resultado
        coincidencias_lista.append(coincidencia_formateada)  # Agregar a la lista
    
    # Verificación de la lista de coincidencias
    print("\nLista de coincidencias final:")
    for item in coincidencias_lista:
        print(item)
    
    return coincidencias_lista

    #ESTA FUNCION DEBE DE RETORNAR COINCIDENCIAS PARA SER MANDADO AL CODIGO DE CRISTIAN

if __name__ == "__main__":
    maint(1)