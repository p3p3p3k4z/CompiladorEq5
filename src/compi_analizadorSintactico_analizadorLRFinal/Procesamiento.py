from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from Estructura_Automata import *

def Conjuntos():
    font1=("Times New Roman",12)
    arrLabels=[]
    lexWindow=Toplevel()
    lexWindow.state("zoomed")
    lexWindow.title("Algoritmo de Thompson")
    lexWindow.config(bg="#B5FFFF")
    #82EEFD

    archivoL=Label(lexWindow,text="Ingresa una expresion",width=20,bg="#FFB3C6",font=font1)
    archivoL.place(x=20,y=50)

    archivoButton=Button(lexWindow,text="Inspeccionar",width=26,command=lambda:abrirArchivo(alphaEntry,erEntry,lexWindow),bg="#FFB3C6" ,font=font1)
    archivoButton.place(x=210,y=47)

    eregularL=Label(lexWindow,text="Expresión regular:",font=font1,width=20, bg="#FFB3C6")
    eregularL.place(x=20,y=100)

    erEntry=Entry(lexWindow,width=30,font=font1, bg="#FFB3C6")
    erEntry.place(x=210,y=101)

    alphaLabel=Label(lexWindow,text="Alfabeto",font=font1,width=20, bg="#FFB3C6")
    alphaLabel.place(x=20,y=150)

    alphaEntry=Entry(lexWindow,font=font1,width=30, bg="#FFB3C6")
    alphaEntry.place(x=210,y=151)

    canvas=Canvas(lexWindow,width=1500,height=450, bg="#FFB3C6")
    canvas.place(x=0,y=200)

    def on_arrow_key(event):#define un metodo con una accion
            if event.keysym == "Left":#si se preciono la flecha izquierda
                canvas.xview_scroll(-1, "units")#se mueve a la izquierda
            elif event.keysym == "Right":#lo mismo pero con la flecha derecha
                canvas.xview_scroll(1, "units")
            canvas.config(scrollregion=canvas.bbox("all"))#define la region de desplazamiento    

    def on_arrow_key_v(event):
         if event.keysym == "Up":#los mismo pero arriba
             canvas.yview_scroll(-1, "units")
         elif event.keysym == "Down":#abajo
             canvas.yview_scroll(1, "units")
         canvas.config(scrollregion=canvas.bbox("all"))#lo mismo de antes

    tabla=Frame(canvas,width=1470,height=300)
    canvas.create_window((100, 50), window=tabla, anchor=NW)
    #canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=horizontal_scrollbar.set)

    afnButton=Button(lexWindow,text="Obtener AFN",width=15,font=font1,bg="#82EEFD",command=lambda:printTableLexico(alphaEntry.get(),tabla,canvas,lexWindow,arrLabels,erEntry.get()) )
    afnButton.place(x=458,y=97)
    cleanButton=Button(lexWindow,text="Limpiar",font=font1,bg="#82EEFD",command=lambda:cleanTable(tabla,arrLabels,alphaEntry,erEntry))
    cleanButton.place(x=605,y=97)
    tabla.update_idletasks()#actualiza el estado de la tabla
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind_all("<KeyPress-Left>", on_arrow_key)
    canvas.bind_all("<KeyPress-Right>", on_arrow_key)
    canvas.bind_all("<KeyPress-Up>", on_arrow_key_v)
    canvas.bind_all("<KeyPress-Down>", on_arrow_key_v)

def  printTableLexico(alfabeto,tabla,canvas,lexWindow,arrLabels,er):
    #alfabeto: Un conjunto de símbolos que forman el alfabeto del autómata.
    #tabla: La referencia a la tabla donde se mostrarán las transiciones.
    #canvas: Un área de desplazamiento para la tabla.
    #lexWindow: La ventana principal de la interfaz.
    #arrLabels: Una lista para almacenar etiquetas de la tabla.
    #er: Una expresión regular que se evaluará.
    expresion_reg = er
    expresion_reg = expresion_postfija(expresion_reg)#convierte la expresion regular a notacion postfija
    #print(expresion_reg)#mostramos la notacion postfija
    Automata=evaluar_expresion_postfija(expresion_reg)#la evaluamos
    font1=("Times New Roman",11)
    estados=alfabeto
    columna=1
    encabezadoL=Label(tabla,text="Estado",font=font1,borderwidth=1, relief="solid",width=20)
    encabezadoL.grid(row=0,column=0)#coloca el el label en la tabla utilizando un metodo de cuadriculas
    abecedario=[]
    for letra in estados:
        ColumnaL=Label(tabla,text=str(letra),width=20,borderwidth=1, relief="solid",font=font1)
        ColumnaL.grid(row=0,column=columna)#lo mismo de antes pero en una columna diferente
        arrLabels.append(ColumnaL)
        abecedario.append(letra)
        columna+=1
    abecedario.append("λ")
    lambdaL=Label(tabla,text="ε",font=font1,borderwidth=1, relief="solid",width=20)
    lambdaL.grid(row=0,column=columna)
    arrLabels.append(encabezadoL)
    arrLabels.append(lambdaL)
    tabla.update_idletasks()#actualiza la interfaz
    canvas.config(scrollregion=canvas.bbox("all"))#barra de desplazamiento, tal vez borrar
    numEstados=len(estados)#Numero de estados
    if numEstados:#verifica que haya estados
        i=1
        nodo=Automata.head#nodo apunta al estado del primer nodo
        while nodo:#mientras nodo no sea vacio va a iterar
            l=0
            num_estado=nodo.state.getId()#obtiene el id del estado
            if num_estado == 0:
                #Si es un estado inicial le agregamos una i
                celda=Label(tabla,text=str(num_estado)+" i",width=20,borderwidth=1, relief="solid",font=font1)
            if nodo.state.getFinalState():
                #si es un estado final le agregamos una f
                celda=Label(tabla,text=str(num_estado)+ " f",width=20,borderwidth=1, relief="solid",font=font1)
            if not nodo.state.getFinalState() and num_estado != 0:
                #si no es estado final solamente se muestra su numero
                celda=Label(tabla,text=str(num_estado),width=20,borderwidth=1, relief="solid",font=font1)
            
            celda.grid(row=i,column=l)#lo coloca en la tabla
            l+=1#aumenta el numero de las culomnas
            edos=nodo.state.getTransitions()#pide la lista de transiciones
            for transition in edos :
                l=1#Reestablecer columnas
                caracter=transition.getSymbol()#obtiene el simbolo asociado a la transicion actual
                #print(edo_sig)
                for aux in abecedario:#Para poner guiones
                    if aux==caracter:
                        #si existe coincidencia entre el simbolo del abecedario y la transicion
                        celda_sym=Label(tabla,text=str(nodo.state),width=20,borderwidth=1, relief="solid",font=font1)
                        celda_sym.grid(row=i,column=l)
                    else:
                        #si no hay transicion se coloca guion
                        celda_sym=Label(tabla,text="-",width=20,borderwidth=1, relief="solid",font=font1)
                        celda_sym.grid(row=i,column=l)
                    l+=1
            i+=1#se incrementa el  contador de filas
            nodo=nodo.next#avanza al siguiente nodo
        num_letras=len(abecedario)#numero de de simbolos en abecedario
        m=1#columnas
        i=i-1
        while m<=num_letras:#rellena lo demas con guiones
            celda_sym=Label(tabla,text="-",width=20,borderwidth=1, relief="solid",font=font1)
            celda_sym.grid(row=i,column=m)
            m+=1
        canvas.config(scrollregion=canvas.bbox("all"))#ajusta para incluir todos los elemntos de la tabla
    else:
        lexWindow.grab_set()#muestra error
        messagebox.showerror("Error","introduce un alfabeto")
        lexWindow.grab_release()

def printTableConjuntos(alfabeto,tabla,canvas,lexWindow,arrLabels,er):
    columna=1
    abecedario=[]
    font1=("Times New Roman",15)
    numEstados=len(alfabeto)#Numero de estados
    if numEstados:#Verificar que exista un alfabeto
        """Obtener el AFN"""
        expresion_reg = expresion_postfija(er)#Obtener la expresión postfija
        Automata=evaluar_expresion_postfija(expresion_reg)#Obtener el autómata
        
        """Obtener el AFD"""
        cerradura=[]
        cerradura.append(0)
        cerradura=cerradura_e(cerradura,Automata.head,"λ")
        cerradura.append(0)
        #print(cerradura)
        NuevosEstados=AFD(cerradura,alfabeto,Automata.head)
        print(NuevosEstados)

        """Imprime los labels fantasma, el alfabeto y la palabra Estado"""
        label_fantasma=Label(tabla,text="     ",width=10).grid(row=0,column=0)#Imprime una columna vacía
        fila=1 #Fila de la tabla
        columna=1#Columna de la tabla

        """Verifica si el alfabeto contiene la palabra reservada digito o letra"""
        bandera_letra = False
        if 'l' in alfabeto and 'd' in alfabeto:#Si el alfabeto contiene las palabras reservadas
            alfabeto_aux = alfabeto.replace('l',"")
            alfabeto_aux = alfabeto.replace('d',"")
            if len(alfabeto_aux) > 0:#Si el alfabeto no esta vacío despues de quitarle las palabras reservadas letra y digito
                bandera_letra = True
        elif 'l' in alfabeto:#Si el alfabeto contiene la palabra reservada letra
            alfabeto_aux = alfabeto.replace('l',"")
            if len(alfabeto_aux) > 0:#Si el alfabeto no esta vacío despues de quitarle las palabra reservada letra
                bandera_letra = True
        """
        elif 'd' in alfabeto:#Si el alfabeto contiene la palabra reservada digito
            alfabeto_aux = alfabeto.replace('d',"")
            if len(alfabeto_aux) > 0:#Si el alfabeto no esta vacío despues de quitarle la palabra reservada digito
                bandera_letra = True
        """
                
        """Imprime el alfabeto"""
        idSimbolos = 1
        dictSimbolos = {}
        for letra in alfabeto:
            label_fantasma=Label(tabla,text="     ",width=10).grid(row=0,column=columna)#Imprime una columna vacía
            
            """Remplaza l por letra y d por digito"""
            letra_aux = letra
            if letra == 'l':
                letra_aux="letra"
            elif letra == 'd':
                letra_aux="digito"
            ColumnaL=Label(tabla,text=letra_aux,width=15,borderwidth=1, relief="solid",font=font1)
            ColumnaL.grid(row=fila,column=columna)#Imprime el label
            arrLabels.append(ColumnaL)#Agrega el label a un arreglo para poder modificarlo
            abecedario.append(letra)#Agrega la letra al abecedario
            dictSimbolos[idSimbolos]=letra#Agrega el simbolo al diccionario

            """Agrega los simbolos 'letra-caracter'"""
            if letra != 'l' and letra != 'd' and bandera_letra == True:
                columna += 1
                idSimbolos += 1#Aumenta el id de los simbolos
                letra_aux2 = "letra-"+letra_aux
                ColumnaL=Label(tabla,text=letra_aux2,width=15,borderwidth=1, relief="solid",font=font1)
                ColumnaL.grid(row=fila,column=columna)#Imprime el label
                arrLabels.append(ColumnaL)#Agrega el label a un arreglo para poder modificarlo
                abecedario.append(letra)#Agrega la letra al abecedario
                dictSimbolos[idSimbolos]=letra_aux2

            columna+=1#Aumenta la columna
            idSimbolos += 1
        encabezadoL=Label(tabla,text="Estado",font=font1,borderwidth=1, relief="solid",width=10)#Imprime Estado en la primera columna y la primera fila
        encabezadoL.grid(row=fila,column=0)
        arrLabels.append(encabezadoL)#Agrega el label a un arreglo para poder modificarlo
        abecedario.append("λ")#Agrega el lambda al abecedario
        
        """"Imprime los estados y las transiciones"""
        EstadoFinal = encontrarEstadoFinal(Automata.head)#Obtiene el estado final
        #print(EstadoFinal)
        fila=2
        tamañoLista=len(NuevosEstados)
        nodo=NuevosEstados
        #print(dictSimbolos)
        for i in range(tamañoLista):#i es el indice de la lista
            columna=0

            """Verifica si el estado es inicial o final"""
            estados_no_renombrados = nodo[i][1]#Obtiene la lista de estados no renombrado
            #print(estados_no_renombrados)
            for auxxx in estados_no_renombrados:#Recorre la lista de estados no renombrados
                #print(auxxx)
                if auxxx == 0:
                    celda=Label(tabla,text=nodo[i][0]+" i",width=10,borderwidth=1, relief="solid",font=font1)#Imprime el estado
                    break
                elif auxxx == EstadoFinal:
                    celda=Label(tabla,text=nodo[i][0]+" f",width=10,borderwidth=1, relief="solid",font=font1)#Imprime el estado
                else:
                    celda=Label(tabla,text=nodo[i][0],width=10,borderwidth=1, relief="solid",font=font1)#Imprime el estado

            #celda=Label(tabla,text=nodo[i][0]+"",width=10,borderwidth=1, relief="solid",font=font1)#Imprime el estado
            celda.grid(row=fila,column=columna)
            columna=1
            
            """Imprime las transiciones"""
            for j in range(len(dictSimbolos)):
                simbolo = dictSimbolos[columna]#Obtiene el simbolo de la columna
                transicionesDentro = nodo[i][2]#Obtiene la lista de transiciones
                for transicion in transicionesDentro:#Recorre la lista de transiciones
                    if transicion[1] == simbolo:#Si el simbolo de la transicion es igual al simbolo de la columna
                        celda_sym=Label(tabla,text=transicion[2],width=15,borderwidth=1, relief="solid",font=font1)#Imprime el estado de transición
                        celda_sym.grid(row=fila,column=columna)
                        break#Termina el ciclo
                    else:
                        celda_sym=Label(tabla,text="-",width=15,borderwidth=1, relief="solid",font=font1)#Imprime el estado de transición
                        celda_sym.grid(row=fila,column=columna)
                columna+=1
            fila+=1

        """Actualiza la tabla"""
        tabla.update_idletasks()#Actualizar la tabla
        canvas.config(scrollregion=canvas.bbox("all"))#Actualizar el canvas
    else:#Si no existe un alfabeto, muestra un error
        lexWindow.grab_set()
        messagebox.showerror("Error","introduce un alfabeto")
        lexWindow.grab_release()

def encontrarEstadoFinal(estados):
    nodo=estados
    while nodo:#mientras nodo no sea none
        if nodo.state.getFinalState():
            return nodo.state.getId()#si es final regresamos el id del estado
        nodo=nodo.next#de lo contrario pasamos al siguiente
    return None#si ninguno es final regresamo none

def cerradura_e(elems,head,letra):
    pila=[]#lista para recorrer los estados
    conjunto=[]#lista para estado alcanzables con epsilon
    for i in elems:#
        pila.append(i)#agregamos los estados a la pila
    while pila:#mientras haya elementos en la pila seguimos iterando
        elemento=pila.pop()#saca un elemento de la pila
        nodo1=buscarNodo(head,elemento)#llama a la funcion
        edos=nodo1.state.getTransitions()#obtiene las transiciones del estado actual
        for transition in edos:#recorremos esas transiciones
            char=transition.getSymbol()#obtiene el simbolo de la transicion actual
            if char==letra:#varifica si char es igual a epsilon
                pila.append(transition.getState())#agrega el estado alcanzado con la transicion
                if transition.getState() not in conjunto:#verifica si el estado alcanzado no esta aun en el conjunto de estados
                    conjunto.append(transition.getState())#agrega el estado al conjunto
    conjunto.sort()#ordena la lista
    return conjunto #Devuelve una lista de estados con epsilon

def buscarNodo(head,num_estado):
    nodo=head#lo inicializamos con el primer nodo de la lista
    while nodo:#mientras nodo no sea none
        if num_estado==nodo.state.getId():#si el id del estado actual es igual al del estado buscado
            return nodo#regresa el nodo encontrado
        nodo=nodo.next#de lo contrario pasa al siguiente nodo
    return None#regresa none en caso de no encontrar nada

def AFD(listaInicial,abecedario,head):
    #una funcion con tres parametros donde el primero representa un conjunto de estados iniciales
    #el segundo es una cadena que representa el estado de los automatas y el tecero es el nodo inicial
    letra1=105#valor ascci "i"
    inicial=65#Valor ascci "A"
    pilaEdos=[] 
    pila2=[]
    letraReservada=105#valor ascci "i"
    pilaEdos.append(listaInicial)#Agregar el primer estado A
    conjuntoEdos=[]#trae los nuevos estados
    transicionesEstado=[]#trae una lista de tuplas
    transiciones=[]    
    Concatenar=[]        
    cerraduraAux=[]    
    Edo=[]                               
    conjuntoEdos.append((chr(inicial),listaInicial)) #creamos una tupla con "A" y el conjunto de estados
    if abecedario.count('if'):#comprueba si abecedario tiene "if"
        abecedario=abecedario.replace("if","")#en caso de que si elimina "if" de la cadena
        bandera=True#establecemos una bandera donde dice que es verdadero
    else:
        bandera=False#en caso de que no establecemos la bandera con distinto valor
    if bandera and bandera:#Revisa si se procesa una palabra reservada
        while pilaEdos :#mientras haya elementos en la pila
            estado=pilaEdos.pop(0)#extrae el primer nodo de la pila
            estado.sort()#ordena los estados
            nuevoEdo=getMueveR(estado,head,chr(letra1))#Obtiene e(M(A,i))
            if not existeEstado(nuevoEdo,conjuntoEdos) :#comprueba si el nuevo estado ya esta en conjuntos
                #si no esta y nuevoEdo no esta vacio lo agrega
                if len(nuevoEdo)!=0:
                    inicial+=1
                    pilaEdos.append(nuevoEdo)
                    pila2.append(nuevoEdo)
                    tuplaAux=(chr(inicial),nuevoEdo)#Crea una tupla
                    conjuntoEdos.append(tuplaAux)#la añade a la lista       
            #Inserta una tupla de la forma (A,a,B) para transitar de un edo a otro
            transicionesEstado.append((getletra(estado,conjuntoEdos),chr(letra1),getletra(nuevoEdo,conjuntoEdos)))
            cerraduraAux.clear()
            if transicionesEstado not in transiciones:#si las transiciones aun no estan registradas se añaden
                transiciones.append(transicionesEstado)
       #ahora  procesamos A(letra-i)
            Edo=[]
            for m in chr(letra1)+"l=":#Este ciclo obtiene los estados a los que se puede ir con i,considerando el conjunto l
                cerraduraAux1= Mueve(estado,head,m)#Manda el caracter
                Edo+=cerraduraAux1
            cerraduraAux1=quitaDuplicados(Edo)#se eliminan los estados
            cerraduraAux2=Mueve(estado,head,chr(letra1))#Obtiene el conjunto de estado que se alcanzan con "i"
            for k in cerraduraAux2:
                if k  in cerraduraAux1:
                    cerraduraAux1.remove(k)#aliminamos cualquier estado de esta lista que este en cerraduraAux2
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

def quitaDuplicados(conjunto):
    nuevaLista=[]
    for i in conjunto:
        if i not in nuevaLista:
            nuevaLista.append(i)
    return nuevaLista

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

def cleanTable(tabla,arrLabels,alphaEntry,erEntry):
    for widget in tabla.winfo_children():
        widget.destroy()
    for widget in arrLabels:
        widget.destroy()
    arrLabels.clear()#Limpiar la lista
    alphaEntry.delete(0,END)
    erEntry.delete(0,END)

def abrirArchivo(alphaEntry,erEntry,lexWindow):
    lexWindow.grab_set()
    alphaEntry.delete(0,END)
    erEntry.delete(0,END)
    direccionArchivo=filedialog.askopenfilename(initialdir=r"D:\Sistemas\Proyect_Comp_Java\Proyecto_compilador\Pruebas_expresiones_reg",title="Abrir",filetypes=(("texto","*.txt"),))
    archivo=open(direccionArchivo)
    alfabeto=archivo.readline()
    expresionRegular =archivo.readline()
    expresionRegular = expresionRegular.replace('digitos','d')
    expresionRegular = expresionRegular.replace('letras','l')
    alfabeto = alfabeto.strip()
    alfabeto = alfabeto.replace('letras','l')
    #Si tiene la palabra reservada digito, letra sustituye y hay que encender la bandera para identificar
    indice_dig = alfabeto.find("digitos")
    if indice_dig != -1:
        alfabeto = alfabeto.replace('digitos','d')
        bandera_transformacion_digitos = 1
    
    indice_alfa = alfabeto.find("letras")
    if indice_alfa != -1:
        alfabeto = alfabeto.replace('digitos','d')
        bandera_transformacion_alfabeto = 1
    print(alfabeto)
    print(expresionRegular)
    alphaEntry.insert(0,alfabeto)
    erEntry.insert(0,expresionRegular)
    lexWindow.grab_release()