#localiza el ultimo nodo del automata
def encontrarEstadoFinal(estados):
    nodo=estados
    while nodo:
        if nodo.state.getFinalState():
            return nodo.state.getId()
        nodo=nodo.next
    return None

def cerradura_e(elems,head,letra):
    pila=[]
    conjunto=[]
    #edos=nodo.state.getTransitions()#Tiene todas las transiciones de 0
    for i in elems:#Agrega elementos a la pila
        pila.append(i)
    while pila:#Va sacando los numeros de estados de la lista
        elemento=pila.pop()#Obtiene el ultimo estado en la pila
        nodo1=buscarNodo(head,elemento)#Busca si esta el nodo en la
        edos=nodo1.state.getTransitions()#Retorna el arreglo de transiciones
        for transition in edos:#Recorrer todas las transiciones
            char=transition.getSymbol()#Obtiene solo el simbolo de la transicion iterada
            if char==letra:#Compara lambda con el simbolo de la transicion
                pila.append(transition.getState())#Agrega el estado al conjunto generado
                if transition.getState() not in conjunto:
                    conjunto.append(transition.getState())
    conjunto.sort()
    return conjunto #Devuelve una lista

def buscarNodo(head,num_estado):
    nodo=head
    while nodo:
        if num_estado==nodo.state.getId():
            return nodo#Encontro el nodo buscado
        nodo=nodo.next
    return None#No encontró nada

def AFD(listaInicial,abecedario,head):
    letra1=105
    inicial=65#Valor del primer estado A
    pilaEdos=[] 
    pila2=[]
    letraReservada=105#valor de la i
    pilaEdos.append(listaInicial)#Agregar el primer estado A
    conjuntoEdos=[]#trae los nuevos estados
    transicionesEstado=[]#trae una lista de tuplas
    transiciones=[]    
    Concatenar=[]        
    cerraduraAux=[]    
    Edo=[]                               
    conjuntoEdos.append((chr(inicial),listaInicial)) #Agrega el estado A al inicio de la cola
    if abecedario.count('if'):
        abecedario=abecedario.replace("if","")
        bandera=True
    else:
        bandera=False
    if bandera and bandera:#Revisa si se procesa una palabra reservada
        while pilaEdos :#Mientras la cola no se vacie
            estado=pilaEdos.pop(0)
            estado.sort()
            nuevoEdo=getMueveR(estado,head,chr(letra1))#Obtiene e(M(A,i))
            if not existeEstado(nuevoEdo,conjuntoEdos) :#agrega el nuevo estado
                if len(nuevoEdo)!=0:
                    inicial+=1
                    pilaEdos.append(nuevoEdo)
                    pila2.append(nuevoEdo)
                    tuplaAux=(chr(inicial),nuevoEdo)#Modificar
                    conjuntoEdos.append(tuplaAux)       
            #Inserta una tupla de la forma (A,a,B) para transitar de un edo a otro
            transicionesEstado.append((getletra(estado,conjuntoEdos),chr(letra1),getletra(nuevoEdo,conjuntoEdos)))
            cerraduraAux.clear()
            if transicionesEstado not in transiciones:
                transiciones.append(transicionesEstado)
       # #####   ahora  procesamos A(letra-i)
            Edo=[]
            for m in chr(letra1)+"l=":#Este ciclo obtiene los estados a los que se puede ir con i,considerando el conjunto l
                                     #porque i pertenece a letras
                cerraduraAux1= Mueve(estado,head,m)#Manda el caracter
                Edo+=cerraduraAux1
            cerraduraAux1=quitaDuplicados(Edo)
            cerraduraAux2=Mueve(estado,head,chr(letra1))#Obtiene el conjunto A(i)
            for k in cerraduraAux2:#Recorrer #Realiza la resta de conjuntos
                if k  in cerraduraAux1:
                    cerraduraAux1.remove(k)
            nuevoEdo=cerradura_e(cerraduraAux1,head,"λ")
            nuevoEdo+=cerraduraAux1#Unir 
            nuevoEdo.sort()
            if not existeEstado(nuevoEdo,conjuntoEdos) :#agrega el nuevo estado
                if len(nuevoEdo)!=0:
                    inicial+=1 
                    pilaEdos.append(nuevoEdo)
                    pila2.append(nuevoEdo)
                    tuplaAux=(chr(inicial),nuevoEdo)#Modificar
                    conjuntoEdos.append(tuplaAux)  
            Edo.clear()
            transicionesEstado.append((getletra(estado,conjuntoEdos),"letra-"+chr(letra1),getletra(nuevoEdo,conjuntoEdos)))
            if transicionesEstado not in transiciones:
                transiciones.append(transicionesEstado)
            if letra1<106 and letra1>102:#Para que se mueva de i a f
               letra1-=3#pasa a f
            else: 
                letra1=108 
                bandera=False 
    if not pila2:
        pila2.append(listaInicial)
    while pila2 and bandera==False:
        estado=pila2.pop()
          
        for letra in abecedario:#Mandar el alfabeto sin epsilon
            cerraduraAux= Mueve(estado,head,letra)
            #print(cerraduraAux)
            nuevoEdo=cerradura_e(cerraduraAux,head,"λ")
            nuevoEdo+=cerraduraAux#Unir la lista Mueve con la otra lista
            nuevoEdo.sort()
            if not existeEstado(nuevoEdo,conjuntoEdos) :
                if len(nuevoEdo)!=0:
                    inicial+=1
                    pila2.append(nuevoEdo)
                    tuplaAux=(chr(inicial),nuevoEdo)
                    conjuntoEdos.append(tuplaAux)
            if getletra(estado,conjuntoEdos)!='B' or letra!='l':
                transicionesEstado.append( (getletra(estado,conjuntoEdos),letra,getletra(nuevoEdo,conjuntoEdos)) )
            cerraduraAux.clear()
        if transicionesEstado not in transiciones:
            transiciones.append(transicionesEstado)
    conjuntoEdos=[sublista for sublista in conjuntoEdos if sublista]
    transiciones1=quitaDuplicados1(transiciones)
    #print(transiciones1)
    """Se juntan los estados con sus transiciones en una lista de tuplas"""
    final = []
    for auxestado in conjuntoEdos:
        transiciones_estado = [] #Lista para almacenar las transiciones de cada estado
        for auxtrans in transiciones1:
            if auxtrans[0] == auxestado[0]:
                transiciones_estado.append(auxtrans)
        auxestado_con_transiciones = auxestado + (transiciones_estado,)
        final.append(auxestado_con_transiciones)
    return final #Devuelve una lista de tuplas

# Función que elimina duplicados de una lista
def quitaDuplicados(conjunto):
    nuevaLista=[]
    for i in conjunto:
        if i not in nuevaLista:
            nuevaLista.append(i)
    return nuevaLista

# Funciones auxiliares para manejo de estados
def quitaDuplicados1(conjunto):
    nuevaLista=[]
    aux1=conjunto[0]
    for i in aux1:
        if i not in nuevaLista and i[2]!='-':
            nuevaLista.append(i)
    return nuevaLista


def getMueveR(estado,head,letra):
    cerraduraAux=[]
    Aux1=[]
    for m in letra+"l":#Este ciclo obtiene los estados a los que se puede ir con i,considerando el conjunto l
                                    #porque i pertenece a letras
        Aux1=Mueve(estado,head,m)#Manda el caracter
        cerraduraAux+=Aux1

    Edo=cerradura_e(cerraduraAux,head,"λ")#Obtiene la primer parte
    resultado=unirListas(Edo,cerraduraAux)
    resultado.sort()
    return resultado

def existeEstado(estado,listaTuplas):
    for j in listaTuplas:
        if estado==j[1]:
            return j[0]
        if len(estado)==0:
            return False
    return None

def unirListas(lista1,lista2):
    for i in lista2:
        if i not in lista1:
            lista1.append(i)
    lista1.sort()
    return lista1

def getletra(estado,listaTuplas):
    for j in listaTuplas:
        if estado==j[1]:
            return j[0]
    return '-'

# Funciones auxiliares para manejo de estados
def Mueve(elems,head,letra):#Esta funcion realiza el Mueve
    pila=[]
    conjunto=[]
    for i in elems:
        pila.append(i)
    while pila:
        elemento=pila.pop()#Obtener
        nodo1=buscarNodo(head,elemento)
        edos=nodo1.state.getTransitions()
        for transition in edos:#Recorrer todas las transiciones
            char=transition.getSymbol()
            if char==letra:
                #pila.append(transition.getState())
                if transition.getState() not in conjunto:
                    conjunto.append(transition.getState())

    #cerraduratemp=cerradura_e(conjunto,head,letra)
    cerradura=[]
    for j in conjunto:
        cerradura.append(j)
    cerradura.sort()
    return cerradura #Devuelve una lista