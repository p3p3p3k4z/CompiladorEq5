from tkinter import *
import lexico as lx
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from Thompson1 import *

def Conjuntos():
    font1=("Times New Roman",12)
    arrLabels=[]
    lexWindow=Toplevel()
    lexWindow.state("zoomed")
    lexWindow.title("Construccion de Conjuntos")
    lexWindow.config(bg="#363062")

    archivoL=Label(lexWindow,text="Selecciona una expresión regular",width=30,font=font1)
    archivoL.place(x=20,y=30)

    archivoButton=Button(lexWindow,text="Abrir archivo",width=20,command=lambda:abrirArchivo(alphaEntry,erEntry,lexWindow),bg="#F99417" ,font=font1)
    archivoButton.place(x=350,y=20)

    eregularL=Label(lexWindow,text="Expresión regular seleccionada",font=font1,width=30)
    eregularL.place(x=20,y=100)

    erEntry=Entry(lexWindow,width=30,font=font1)
    erEntry.place(x=350,y=100)

    alphaLabel=Label(lexWindow,text="Alfabeto",font=font1,width=30)
    alphaLabel.place(x=650,y=100)

    alphaEntry=Entry(lexWindow,font=font1,width=30)
    alphaEntry.place(x=950,y=100)

    canvas=Canvas(lexWindow,width=1500,height=450)
    canvas.place(x=0,y=200)

    def on_arrow_key(event):
            if event.keysym == "Left":
                canvas.xview_scroll(-1, "units")
            elif event.keysym == "Right":
                canvas.xview_scroll(1, "units")
            canvas.config(scrollregion=canvas.bbox("all"))    

    def on_arrow_key_v(event):
         if event.keysym == "Up":
             canvas.yview_scroll(-1, "units")
         elif event.keysym == "Down":
             canvas.yview_scroll(1, "units")
         canvas.config(scrollregion=canvas.bbox("all"))
    
    scrollbar=ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    scrollbar.set(0.0, 1.0)
    scrollbar.place(x=5, y=50, height=300)

    horizontal_scrollbar = ttk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
    horizontal_scrollbar.set(0.0,1.0)
    horizontal_scrollbar.place(x=0,y=0,width=300)

    tabla=Frame(canvas,width=1470,height=300)
    canvas.create_window((100, 50), window=tabla, anchor=NW)
    canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=horizontal_scrollbar.set)

    def on_mousewheel(event):
         canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    afnButton=Button(lexWindow,text="Obtener AFN",width=15,font=font1,bg="#F99417",command=lambda:printTable(alphaEntry.get(),tabla,canvas,lexWindow,arrLabels,erEntry.get()) )
    afnButton.place(x=150,y=150)
    cleanButton=Button(lexWindow,text="Limpiar",font=font1,bg="#F99417",command=lambda:cleanTable(tabla,arrLabels,alphaEntry,erEntry))
    cleanButton.place(x=350,y=150)
    tabla.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<KeyPress-Left>", on_arrow_key)
    canvas.bind_all("<KeyPress-Right>", on_arrow_key)
    canvas.bind_all("<KeyPress-Up>", on_arrow_key_v)
    canvas.bind_all("<KeyPress-Down>", on_arrow_key_v)


def printTable(alfabeto,tabla,canvas,lexWindow,arrLabels,er):
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
    direccionArchivo=filedialog.askopenfilename(initialdir=r"C:\Users\Documents\Compiladores",title="Abrir",filetypes=(("texto","*.txt"),))
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