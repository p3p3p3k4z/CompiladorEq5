from Ir_a_Algoritmo import *
from cerradura import *
class TablaColeccionCanonica:
    def __init__(self):
        self.estado = []
        self.SimboloIr_A = '-'
        self.estadoIr_A = '-'
        self.EnviadoACerradura = []
           
    def getEstado(self):
        return self.estado
        
    def getSimboloIr_A(self):
        return self.SimboloIr_A
    
    def getEstadoIr_A(self):
        return self.estadoIr_A
    
    def getEnviadoACerradura(self):
        return self.EnviadoACerradura
    
    def setEstado(self, estado):
        self.estado = estado
    
    def setSimboloIr_A(self, SimboloIr_A):
        self.SimboloIr_A = SimboloIr_A
    
    def setEstadoIr_A(self, estadoIr_A):
        self.estadoIr_A = estadoIr_A
    
    def setEnviadoACerradura(self, EnviadoACerradura):
        if self.EnviadoACerradura is None:
            self.EnviadoACerradura = EnviadoACerradura
        else:
            self.EnviadoACerradura.extend(EnviadoACerradura)
    
    def __str__(self):
        if self.estadoIr_A == '-' or self.estadoIr_A == '':
            cadena = "\ncerradura (" + str(self.EnviadoACerradura) + ")\n\nEstado: " + str(self.estado) + "\n\n"
        else:    
            cadena = "\nIr_a(" + str(self.estadoIr_A) + "," + str(self.SimboloIr_A) + ") =  " + str(self.EnviadoACerradura) + "\n\nEstado: " + str(self.estado) + "\n\n"
        return cadena

    def clear(self):
        self.estado = []
        self.SimboloIr_A = '-'
        self.estadoIr_A = '-'
        self.EnviadoACerradura = []

def calcularReglasP(archivo,listaNoTerminales,ruta):
    listaProducciones=[]
    cadena = []
    lineas = archivo.readlines()   
    archivo2=open(str(ruta),encoding="utf-8")
    archivo2.readline()
    archivo2.readline()
    for l in lineas:
        cadena=[]
        reglaP = archivo2.readline().split("->")
        reglaP[1] = reglaP[1].replace("\n", "")
        indice = 0
        cad=reglaP[1]
        while indice < len(cad):
            aux=""
            if cad[indice] == ' ':
                indice+=1
            if indice < len(cad):
                caracter = cad[indice]  
                if caracter.isupper() == True:
                    cadena.append(caracter)
                    indice += 1
                elif caracter.isalpha() == False:
                    cadena.append(caracter)
                    indice += 1
                else:
                    while caracter.islower() == True and indice < len(cad):
                        caracter = cad[indice]
                        aux+=caracter
                        indice += 1
                    cadena.append(aux)
        producciones = (reglaP[0], cadena)
        listaProducciones.append(producciones)


    for i, elemento in enumerate(listaProducciones):
        for j, elemento2 in enumerate(elemento[1]):
            listaProducciones[i][1][j] = elemento2.replace(" ", "")
    return listaProducciones

def agregarPunto(listaProducciones):
    listaProduccionesAux = []
    for produccion in listaProducciones:
        if produccion[1] == ['λ']:
            produccion = (produccion[0],['•'])
        else:
            produccion = (produccion[0], ['•'] + produccion[1])
        listaProduccionesAux.append(produccion)
    return listaProduccionesAux

def convertirLista(Conjunto):
    for i, elemento in enumerate(Conjunto):
        Conjunto[i] = list(elemento)


def buscarEstado(lista_estados_conjuntos, conjunto_ir_a):
    for index, elemento_lista_conjuntos in enumerate(lista_estados_conjuntos):
        if conjunto_ir_a == elemento_lista_conjuntos[1]:
            return index
    return -1
def quitarLambda(ConjuntoC):
    for i,elem in enumerate(ConjuntoC):
        for j, produccion in enumerate(elem):
            if produccion[j] == 'λ':
                ConjuntoC[i][j].remove('λ')

def coleccionCanonica(ConjuntoC, reglasProduccion, lista_estados_conjuntos, enumeracion_estados):
    listaCanonica = []
    
    while ConjuntoC:
        conjunto_actual = ConjuntoC.pop(0)
        caracteresEvaluados = []
        
        conjunto_ir_a = []
        for reglas in conjunto_actual[1]:
            regla = reglas[1]
            bandera_se_encontro_estado = -1
            bandera_no_se_ha_calculado_transicion = -1
            for i in range(len(regla)): 
                

                if regla[0] == '•' and len(regla) == 1:
                    nuevo_elemento_canonica = TablaColeccionCanonica()
                    nuevo_elemento_canonica.setEnviadoACerradura([reglas])
                    nuevo_elemento_canonica.setEstado(conjunto_actual[0])
                    listaCanonica.append(nuevo_elemento_canonica)
            
                    
                if regla[len(regla)-1] == '•' :
                    conjunto_ir_a = None
                    
                elif regla[i] == '•' and regla[i+1] != None:
                    if regla[i+1] not in caracteresEvaluados:
                        nuevo_elemento_canonica = TablaColeccionCanonica()
                        nuevo_elemento_canonica.setEstadoIr_A(conjunto_actual[0])
                        nuevo_elemento_canonica.setSimboloIr_A(regla[i+1])

                        simbolo_evaluar_ir_a = regla[i+1]
                        caracteresEvaluados.append(regla[i+1])
                        
                        conjunto_ir_a = Ir_a(conjunto_actual, simbolo_evaluar_ir_a, reglasProduccion, nuevo_elemento_canonica)
                        if conjunto_ir_a != None:
                            quitarLambda(conjunto_ir_a)
                        bandera_se_encontro_estado = -1
                        bandera_no_se_ha_calculado_transicion = 1
                        bandera_se_encontro_estado = buscarEstado(lista_estados_conjuntos, conjunto_ir_a)

    
            if bandera_se_encontro_estado == -1 and bandera_no_se_ha_calculado_transicion == 1:
                if (conjunto_ir_a != None and conjunto_ir_a != "Aceptacion"):
                    enumeracion_estados += 1
                    nuevo_estado = ['I' + str(enumeracion_estados), conjunto_ir_a]
                    nuevo_elemento_canonica.setEstado(nuevo_estado)
                    listaCanonica.append(nuevo_elemento_canonica)
                    lista_estados_conjuntos.append(nuevo_estado)
                    ConjuntoC.append(nuevo_estado)
                    
                if (conjunto_ir_a == "Aceptacion"):
                    listaCanonica.append(nuevo_elemento_canonica)
            if bandera_se_encontro_estado != -1 and bandera_no_se_ha_calculado_transicion == 1:
                    nuevo_elemento_canonica.setEstado('I'+str(bandera_se_encontro_estado))
                    listaCanonica.append(nuevo_elemento_canonica)
                    bandera_se_encontro_estado = -1
 
    return listaCanonica           
            
def main(ruta):
    archivoGramatica=open(ruta,encoding="utf-8")
    noTerminales=archivoGramatica.readline().split()
    terminales=archivoGramatica.readline().split()
    simboloInicial = noTerminales[0]
    noTerminales=[]
    terminales=[]
    primerosArray=[]
    reglasProduccion=[]
    reglasProduccion=calcularReglasP(archivoGramatica,noTerminales,ruta)




    elemento_gramatica_aumentada = [simboloInicial + "'", [simboloInicial,"$"]]
    elemento_gramatica_aumentada_aux = [simboloInicial + "'", [simboloInicial,"$"]] 
    elemento_gramatica_aumentada_aux[1].insert(0, '•')    
    ConjuntoC = cerradura(['I0',[elemento_gramatica_aumentada_aux]],reglasProduccion)
    
    quitarLambda(ConjuntoC)
    reglasProduccion.insert(0,elemento_gramatica_aumentada)
    gramatica_aumentada = agregarPunto(reglasProduccion)
    
    lista_posociones_reglas = []

    for i, regla in enumerate(gramatica_aumentada):
        for j, elemento in enumerate(ConjuntoC):
            if elemento == list(regla): 
                lista_posociones_reglas.append(i)
    
    aux = []
    for posicion in lista_posociones_reglas:
        aux.append(gramatica_aumentada[posicion]) 

    i = 0  
    aux_I = [   'I'+ str(i)  , aux      ] 

    ConjuntoC.clear()
    ConjuntoC.append(aux_I)

    for index, elemento in enumerate(ConjuntoC):
        ConjuntoC[index] = list(elemento)

        for e_index, e in enumerate(elemento[1]):
            ConjuntoC[index][1][e_index] = list(e)

    lista_estados_conjuntos = []
    lista_estados_conjuntos.append(aux_I)

    for index, elemento in enumerate(ConjuntoC):
        ConjuntoC[index] = list(elemento)

        for e_index, e in enumerate(elemento[1]):
            ConjuntoC[index][1][e_index] = list(e)

    ResultadosCanonica = coleccionCanonica(ConjuntoC, reglasProduccion, lista_estados_conjuntos,i)

    Estado_Inicial = TablaColeccionCanonica()
    Estado_Inicial.setEstado(lista_estados_conjuntos[0])
    Estado_Inicial.setEnviadoACerradura(gramatica_aumentada[0])
    ResultadosCanonica.insert(0,Estado_Inicial)

    print("\n\nResultadosCanonica: _______________________________________________________________________________________ ")
    for elemento in ResultadosCanonica:
        print(elemento)
    return ResultadosCanonica

#main("./gramatica1.txt")