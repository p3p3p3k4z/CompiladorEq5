from tkinter import filedialog
import getpass

def cargarDireccion():
    username = getpass.getuser()
    ruta_proyecto = r"C:\Users\{username}\Documents\ProyectoCompiladores"
    direccionArchivo = filedialog.askopenfilename(initialdir=ruta_proyecto, title="Abrir Archivo",
                                                  filetypes=(("texto", "*.txt"),))
    return direccionArchivo

def listaCadena(lista):#Recibe una lista y la convierte en una cadena
    cadena=""
    if lista!=[]:
        for i in lista :
            cadena+=i+" "
    return cadena

def cargarDatos(direccionArchivo):
    archivoGramatica = open(direccionArchivo, encoding="utf-8")#abre un archivo utilizando utf-8 que permite
    #leer ñ, tildes y caracteres especiales
    noTerminales = archivoGramatica.readline().split()#lee la primera linea del archivo
    terminales = archivoGramatica.readline().split()#lee la segunda linea del archivo
    return noTerminales, terminales#devuelve ambas listas

def getReglasProduccion(direccionArchivo):
    reglasProduccion = []
    archivoGramatica = open(direccionArchivo, encoding="utf-8")
    archivoGramatica.readline()
    archivoGramatica.readline()#Se salta las 2 primeras lineas
    texto = "hola"#para que entre al while
    while texto != "":
        texto = archivoGramatica.readline()#lee la siguiente linea del archivo
        quitarSalto = texto.replace("\n","")#elimina el salto de linea al final de la cadena
        #divide la cadena en dos partes, antes de -> seran los no terminales y los despues
        #seras los producidos ejemplo A -> a b resultado:[["A", "a b"]
        quitarSalto=quitarSalto.split("->")
        #verifica que la linea no este vacia y verifica que la regla que acabamos de leer no este
        #en reglasProduccion para evitar que se repitan
        if quitarSalto!=[""] and quitarSalto not in reglasProduccion:
            #divide la lista en una lista de simbolos
            aux=quitarSalto[1].split(" ")
            #se crea una tupla con el no terminal y los simbolos
            regla=(quitarSalto[0],aux)
            #se agregan a la lista
            reglasProduccion.append(regla)
    archivoGramatica.close()#cerramos el archivo
    #regres la lista de expresiones procesadas
    return reglasProduccion

def obtenerReglaDerecha(noTerminal,reglasProduccion):#Recibe un no terminal y las reglas de produccion.regresa todas las reglas de produccion que tengan ese no terminal en la parte derecha
    coincidencias=[]
    for regla in reglasProduccion:
        #guardamos en aux la lista de signos del lado derecho
        aux=regla[1]
        #verificamos si el no terminal se encuentra en la lista de simbolos del lado derecho
        #y verificamos que no se repita
        if noTerminal in aux and regla not in coincidencias:
            #agregamos a la lista
            coincidencias.append(regla)
    #si no se encontraron reglas donde el no terminal aparezca del lado derecho
    if coincidencias==[]:
        return "None"
    return coincidencias

def getBeta(regla,noTerminal):#recibe un no terminal y la parte [1] de la tupla de la regla de produccion,es decir, la pura regla sin el no terminal que la produce
    #verificamos que el no terminal aparezca en el lado derecho de las reglas
    if noTerminal in regla:
        #obtenemos el indice del no terminal
        indice=regla.index(noTerminal)
        #toma todos los elementos en la cadena despues del indice
        nuevaCadena=regla[indice+1:]
        #si la cadena no esta vacia regresas la nueva cadena
        #si esta vacia regresas λ
        if nuevaCadena!=[]:
            return nuevaCadena
        return "λ"
    #falso en caso de que no este el no terminal en la parte derecha de la regla
    return False

def obtenerRegla(noTerminal,reglasProduccion):#buscamos si un no terminal dado aparece del lado izquierdo
    coincidencias=[]
    for regla in reglasProduccion:
        #guardamos en aux el no terminal
        aux=regla[0]
        #verficamos si el no terminal es el que buscamos
        #y si no esta en la lista ya
        if aux[0]==noTerminal and regla not in coincidencias:
            #en cuyo caso la agregamos
            coincidencias.append(regla)
    #retornamos la coincidencias
    return coincidencias       

def obtenerSoloProduccion(reglasProduccion):#aqui solo agregamos las partes derechas a una lista
    parteDerecha=[]
    for regla in reglasProduccion:
        parteDerecha.append(regla[1])
    return parteDerecha

def quitar_duplicados(lista):#Elimina duplicados o simbolos que se repiten
    lista2 = []
    for i in lista:
        if i not in lista2:
            lista2.append(i)
    return lista2

def getPrimeros(noTerminales,terminales,reglasProduccion,simbolo):
    flag=False#bandera que nos ayudara despues
    if simbolo in terminales  or simbolo=="λ" :#Si es terminal o lambda
        #regresa una lista que solo contiene simbolo
        return [simbolo]
    else:#Si es un no terminal
        #busca el simbolo en el lado izquierdo
        reglas=obtenerRegla(simbolo,reglasProduccion)
        #extrae la parte derecha de las reglas encontradas, es decir los simbolos que pueden derivar 
        reglas=obtenerSoloProduccion(reglas)
        primeros=[]
        for regla in reglas:
            for caracter in regla :
                if caracter==simbolo:#Es el mismo no terminal
                    break#ir a la siguiente iteracion ejemplo: S -> S a no podemos procesar S y pasamos a "a"
                else:
                    #en caso contrario hacemos una recursividad
                    aux=getPrimeros(noTerminales,terminales,reglasProduccion,caracter)
                    #añadimos los resultados a la lista de primeros
                    primeros.extend(aux)
                    if "λ" not in aux:#No se encontro lambda en los primeros del simbolo
                        flag=False
                        break#salta a la sig regla
                    else:
                        flag=True
                    #flag=True#Continuar si lambda esta en los primeros 
        if flag==False and "λ" in primeros:#Si no se encontro lambda en los primeros de algun simbolo.Caso 3
            primeros.remove("λ")
        primeros=quitar_duplicados(primeros)
        return primeros  #Retorna una lista con los primeros del simbolo dado 


def getSiguientes(noTerminales,terminales,reglasProduccion,simbolo,lista_siguientes):
    flag=False#una bandera que nos ayudara despues
    primeros=[]
    siguientes=[]
    #obtenemos todas las reglas donde simbolos es parte de la cadena derivada
    reglas=obtenerReglaDerecha(simbolo,reglasProduccion)
    #si el simbolo es el primer no terminal de la gramatica agregamos el $ a la lista
    if simbolo==noTerminales[0] and "$" not in siguientes:
        siguientes.append("$")
        #si simbolo aparece del lado derecho de la lista de produccion
    if reglas!="None":
        for regla in reglas:
            #llamamos a beta para obtener lo que sigue despues del simbolo
            beta=getBeta(regla[1],simbolo) 
            for i in beta:
                #obtemos los primeros de de cada elemento de beta
                primeros.extend(getPrimeros(noTerminales,terminales,reglasProduccion,i))
                primeros=quitar_duplicados(primeros)
                #si no se encuentra λ en primeros se termina el procesamiento de esa regla
                if "λ" not in primeros:
                    break
                #despues de procesar la regla agregamos los primeros a siguientes y removemos λ
            siguientes.extend(primeros)
            siguientes=quitar_duplicados(siguientes)
            if "λ" in primeros:
                siguientes.remove("λ")
                
            lista=[simbolo,siguientes]
            #si ya calculo los siguientes de un simbolo agregamos los demas elementos
            #en caso de que no se agrega un nuevo elemento con simbolo y su conjunto siguientes
            for i in lista_siguientes:
                if i[0]==simbolo :
                    i[1].extend(siguientes)
                    i[1]=quitar_duplicados(i[1])
                    flag=True
                    break
            if flag==False:
                lista_siguientes.append(lista)
            if "λ" in primeros:
                #si hay λ significa que simbolo puede derivar a un no terminal, entonces calculamos los
                #siguiente que aparecen antes de simbolo
                if regla[0]!=simbolo :
                    #var1 indica si ya fueeron calculados los siguientes de el no terminal y var2
                    #es el conjunto de siguientes en caso de que var1 sea true
                    var1,var2=verificarSiguientes(regla[0],lista_siguientes)
                    if var1==False:
                        #si no se han calculado, se calculan los siguientes para el no terminal
                        aux=getSiguientes(noTerminales,terminales,reglasProduccion,regla[0],lista_siguientes)
                        siguientes.extend(aux)
                        siguientes=quitar_duplicados(siguientes)
                    else:
                        #si ya fueron calculados se añaden los siguientes almacenas en var2
                        # a la lista de siguientes de simbolo
                        siguientes.extend(var2)
                        if "λ" in siguientes:
                            siguientes.remove("λ")
                        siguientes=quitar_duplicados(siguientes)
            #se limpia la lista de primeros para la siguiente ejecucion
            primeros.clear()
    #regresa la lista de siguientes
    return siguientes
#verificamos si ya se calcularon los siguientes
def verificarSiguientes(simbolo,listaSiguientes):
    for i in listaSiguientes:
        if i[0]==simbolo:
            return True,i[1]
    return False,None

def mainPyS(ruta):#Por ahora solo la framatica 6 falla
    lista_siguientes=[]
    datos=[]
    noTerminales, terminales = cargarDatos(ruta)
    reglasProduccion = getReglasProduccion(ruta)
    primeros=getPrimeros(noTerminales,terminales,reglasProduccion,noTerminales[0])

    for var in noTerminales:
        primeros = getPrimeros(noTerminales,terminales,reglasProduccion,var  )
        siguientes=getSiguientes(noTerminales,terminales,reglasProduccion,var,lista_siguientes)
        print(f"Los primeros de {var} son: {primeros}")
        print(f"Los siguientes de {var} son: {siguientes}\n")
        #tupla=(("siguientes de: " + str(var)),siguientes)
        tupla = (var,primeros,siguientes)
        datos.append(tupla)
    return datos
    #return "algo" + str(datos)+ " "

#print(mainPyS("gramatica1.txt"))