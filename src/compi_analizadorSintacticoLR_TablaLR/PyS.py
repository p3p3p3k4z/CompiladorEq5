from tkinter import filedialog
import getpass
import sys
import os

# Mantener las funciones sin cambios, pero eliminamos la ejecución directa al final
def cargarDireccion():    
    ruta_proyecto = r"../../Gramaticas"
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
    archivoGramatica = open(direccionArchivo, encoding="utf-8")
    noTerminales = archivoGramatica.readline().split()#Falta implementar lo de los no terminales primos A'
    terminales = archivoGramatica.readline().split()
    return noTerminales, terminales

def getReglasProduccion(direccionArchivo):
    reglasProduccion = []
    archivoGramatica = open(direccionArchivo, encoding="utf-8")
    archivoGramatica.readline()
    archivoGramatica.readline()#Se salta las 2 primeras lineas
    texto = "hola"#para que entre al while
    while texto != "":
        texto = archivoGramatica.readline()
        quitarSalto = texto.replace("\n","")
        quitarSalto=quitarSalto.split("->")
        if quitarSalto!=[""] and quitarSalto not in reglasProduccion:
            aux=quitarSalto[1].split(" ")
            regla=(quitarSalto[0],aux)
            reglasProduccion.append(regla)#Tupla con el no terminal y la regla que produce
    archivoGramatica.close()
    return reglasProduccion

def obtenerReglaDerecha(noTerminal,reglasProduccion):#Recibe un no terminal y las reglas de produccion.regresa todas las reglas de produccion que tengan ese no terminal en la parte derecha
    coincidencias=[]
    for regla in reglasProduccion:
        aux=regla[1]
        if noTerminal in aux and regla not in coincidencias:
            coincidencias.append(regla)
    if coincidencias==[]:
        return "None"
    return coincidencias

def getBeta(regla,noTerminal):#recibe un no terminal y la parte [1] de la tupla de la regla de produccion,es decir, la pura regla sin el no terminal que la produce
    if noTerminal in regla:#El no terminal esta en la regla
        indice=regla.index(noTerminal)#Obtener indice del no terminal en la regla
        nuevaCadena=regla[indice+1:]#Obtener la cadena que esta despues del no terminal
        #if indice+1<len(regla):
        #    return regla[indice+1]
        if nuevaCadena!=[]:
            return nuevaCadena
        return "λ"
    return False

def obtenerRegla(noTerminal,reglasProduccion):#Recibe un no terminal y las reglas de produccion.regresa todas las reglas de produccion que tengan ese no terminal en la parte derecha
    coincidencias=[]
    for regla in reglasProduccion:
        aux=regla[0]
        if aux[0]==noTerminal and regla not in coincidencias:
            coincidencias.append(regla)
    return coincidencias       

def obtenerSoloProduccion(reglasProduccion):
    parteDerecha=[]
    for regla in reglasProduccion:
        parteDerecha.append(regla[1])
    return parteDerecha

def quitar_duplicados(lista):
    lista2 = []
    for i in lista:
        if i not in lista2:
            lista2.append(i)
    return lista2

def getPrimeros(noTerminales,terminales,reglasProduccion,simbolo):
    flag=False
    if simbolo in terminales  or simbolo=="λ" :#Si es terminal o lambda
        return [simbolo]
    else:#Es un no terminal
        reglas=obtenerRegla(simbolo,reglasProduccion)
        reglas=obtenerSoloProduccion(reglas)
        primeros=[]
        for regla in reglas:
            for caracter in regla :
                if caracter==simbolo:#Es el mismo no terminal
                    break#ir a la siguiente iteracion
                else:
                    aux=getPrimeros(noTerminales,terminales,reglasProduccion,caracter)
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
    flag=False
    primeros=[]
    siguientes=[]
    reglas=obtenerReglaDerecha(simbolo,reglasProduccion)#Obtiene solo la parte derecha de la regla donde aparece el no terminal
    if simbolo==noTerminales[0] and "$" not in siguientes:#Se añade $ a los siguientes del primer no terminal
        siguientes.append("$")
    if reglas!="None":#Si el no terminal tiene reglas en donde aparezca en la parte derecha,si no devuelve $ como siguiente
        for regla in reglas:#Recorre todas las reglas de produccion donde aparece el no terminal a la derecha
            beta=getBeta(regla[1],simbolo)#Obtiene el siguiente caracter del no terminal en la regla de produccion 
            for i in beta:   
                primeros.extend(getPrimeros(noTerminales,terminales,reglasProduccion,i))
                primeros=quitar_duplicados(primeros)
                if "λ" not in primeros:#regla 3 de primeros,continuar solo si  hay lambda en los primeros
                    break
            siguientes.extend(primeros)#Agregar los primeros obtenidos a los siguientes del no terminal
            siguientes=quitar_duplicados(siguientes)#Para eliminar datos duplicados
            if "λ" in primeros:#No puede haber lambda en los siguientes de un no terminal
                siguientes.remove("λ")
            lista=[simbolo,siguientes]#Lista con el no terminal y sus siguientes
            for i in lista_siguientes:#Si ya se agrego el no terminal y sus siguientes a la lista de siguientes solo se agregan los nuevos siguientes,en caso de encontrar mas
                if i[0]==simbolo :
                    i[1].extend(siguientes)
                    i[1]=quitar_duplicados(i[1])
                    flag=True
                    break
            if flag==False:#Si no se ha agregado el no terminal y sus siguientes a la lista de siguientes
                lista_siguientes.append(lista)
            if "λ" in primeros:#Si se obtuvo lambda en los primeros de algun simbolo.Caso 3
                if regla[0]!=simbolo :#Por si no es un caso A->aA,si no salta a la sig regla
                    var1,var2=verificarSiguientes(regla[0],lista_siguientes)#devuelve boolean,lista de siguientes
                    if var1==False:#Si no se han calculado los siguientes
                        aux=getSiguientes(noTerminales,terminales,reglasProduccion,regla[0],lista_siguientes)#Regla[0] es el inicio de la regla
                        siguientes.extend(aux)
                        siguientes=quitar_duplicados(siguientes)
                    else:#Si ya se calcularon los siguientes
                        siguientes.extend(var2)
                        if "λ" in siguientes:
                            siguientes.remove("λ")
                        siguientes=quitar_duplicados(siguientes)
            primeros.clear()#Hay que limpiar los primeros despues de cada regla
    return siguientes

def verificarSiguientes(simbolo,listaSiguientes):#Verifica si el simbolo ya esta en la lista de siguientes
    for i in listaSiguientes:
        if i[0]==simbolo:
            return True,i[1]
    return False,None

def mainPyS(direccionArchivo=None):  # Agregar la posibilidad de recibir la dirección como parámetro
    if not direccionArchivo:  # Si no se proporciona, usar el cuadro de diálogo
        direccionArchivo = cargarDireccion()
    lista_siguientes = []
    datos = []
    noTerminales, terminales = cargarDatos(direccionArchivo)
    reglasProduccion = getReglasProduccion(direccionArchivo)
    primeros = getPrimeros(noTerminales, terminales, reglasProduccion, noTerminales[0])

    for var in noTerminales:
        primeros = getPrimeros(noTerminales, terminales, reglasProduccion, var)
        siguientes = getSiguientes(noTerminales, terminales, reglasProduccion, var, lista_siguientes)
        tupla = (var, primeros, siguientes)
        datos.append(tupla)
    return datos

# Hacer que el script pueda ser ejecutado directamente o importado
if __name__ == "__main__":
    print(mainPyS())

# Run the function
#print(mainPyS())