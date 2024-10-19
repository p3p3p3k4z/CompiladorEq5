from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from Estructura_Automata import *

#Genera la ventana emergente para el algoritmo de Thompson
def Conjuntos():
    font1=("Times New Roman",12)
    arrLabels=[]
    lexWindow=Toplevel()
    
    try:
        lexWindow.attributes("-zoomed", True)
    except:
        lexWindow.geometry(f"{lexWindow.winfo_screenwidth()}x{lexWindow.winfo_screenheight()}+0+0")
        
    lexWindow.title("Algoritmo de Thompson")
    lexWindow.config(bg="#B5FFFF")
    #82EEFD

#Crea el listado de opciones 
    archivoL=Label(lexWindow,text="Ingresa una expresion",width=20,bg="#FFB3C6",font=font1)
    archivoL.place(x=20,y=50)

#boton para seleccionar el archivo 
    archivoButton=Button(lexWindow,text="Inspeccionar",width=26,command=lambda:abrirArchivo(alphaEntry,erEntry,lexWindow),bg="#FFB3C6" ,font=font1)
    archivoButton.place(x=210,y=47)

#muestra la expresion regular contenida en el archivo seleccionado 
    eregularL=Label(lexWindow,text="Expresión regular:",font=font1,width=20, bg="#FFB3C6")
    eregularL.place(x=20,y=100)

    erEntry=Entry(lexWindow,width=30,font=font1, bg="#FFB3C6")
    erEntry.place(x=210,y=101)

    alphaLabel=Label(lexWindow,text="Alfabeto",font=font1,width=20, bg="#FFB3C6")
    alphaLabel.place(x=20,y=150)
#muestra el alfabeto contenido en el archivo seleccionado
    alphaEntry=Entry(lexWindow,font=font1,width=30, bg="#FFB3C6")
    alphaEntry.place(x=210,y=151)

#Define el espacio de la tabla 
    canvas=Canvas(lexWindow,width=1500,height=450, bg="#FFB3C6")
    canvas.place(x=0,y=200)

#Habilita el scroll 
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
    
    #scrollbar=ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    #scrollbar.set(0.0, 1.0)
    #scrollbar.place(x=5, y=50, height=300)

    #horizontal_scrollbar = ttk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
    #horizontal_scrollbar.set(0.0,1.0)
    #horizontal_scrollbar.place(x=0,y=0,width=300)

#crea el espacio para la tabla 
    tabla=Frame(canvas,width=1470,height=300)
    canvas.create_window((100, 50), window=tabla, anchor=NW)
    #canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=horizontal_scrollbar.set)

    def on_mousewheel(event):
         canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    afnButton=Button(lexWindow,text="Obtener AFN",width=15,font=font1,bg="#82EEFD",command=lambda:printTable(alphaEntry.get(),tabla,canvas,lexWindow,arrLabels,erEntry.get()) )
    afnButton.place(x=458,y=97)
    cleanButton=Button(lexWindow,text="Limpiar",font=font1,bg="#82EEFD",command=lambda:cleanTable(tabla,arrLabels,alphaEntry,erEntry))
    cleanButton.place(x=605,y=97)
    tabla.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind("<MouseWheel>", on_mousewheel)#posible eliminacion
    canvas.bind_all("<KeyPress-Left>", on_arrow_key)
    canvas.bind_all("<KeyPress-Right>", on_arrow_key)
    canvas.bind_all("<KeyPress-Up>", on_arrow_key_v)
    canvas.bind_all("<KeyPress-Down>", on_arrow_key_v)

#funcion que genera la escritura de la tabla 
def  printTable(alfabeto,tabla,canvas,lexWindow,arrLabels,er):
    expresion_reg = er
    exp_postfija = expresion_postfija(expresion_reg)
    print(f"la expresion regular convertida a postfija es: {exp_postfija}")
    Automata=evaluar_expresion_postfija(exp_postfija)
    font1=("Display",11)
    estados=alfabeto
    columna=1
    encabezadoL=Label(tabla,text="Estado",font=font1,borderwidth=1, relief="solid",width=20)
    encabezadoL.grid(row=0,column=0)
    abecedario=[]
    for letra in estados:
        ColumnaL=Label(tabla,text=str(letra),width=20,borderwidth=1, relief="solid",font=font1)
        ColumnaL.grid(row=0,column=columna)
        arrLabels.append(ColumnaL)
        abecedario.append(letra)
        columna+=1
    abecedario.append("λ")
    lambdaL=Label(tabla,text="ε",font=font1,borderwidth=1, relief="solid",width=20)
    lambdaL.grid(row=0,column=columna)
    arrLabels.append(encabezadoL)
    arrLabels.append(lambdaL)
    tabla.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    numEstados=len(estados)#Numero de estados
    if numEstados:
        #elementos=[(1,2,3,5,4),(4,5,6),(7,8,9),(10,11,12),(13,14,15),(16,17,18),(19,20,21),(19,20,21),(19,20,21),(19,20,21),(19,20,21),(19,20,21),(19,20,21),(19,20,21),(19,20,21),(10,20,30),(10,20,70),(10,20,30),(10,20,30),(10,20,30),(1,2,3)]
        #i=1
        #for j in elementos:
        #    tupla=j
        #    l=0
        #    for k in tupla:
        #        celda=Label(tabla,text=str(k),width=20,borderwidth=1, relief="solid",font=font1)
        #        celda.grid(row=i,column=l)
        #        tabla.update_idletasks()
        #        l+=1
        #    i+=1
        i=1
        nodo=Automata.head
        while nodo:
            l=0
            num_estado=nodo.state.getId()
            if num_estado == 0:
                #print("entro al edo inicial")
                celda=Label(tabla,text=str(num_estado)+" i",width=20,borderwidth=1, relief="solid",font=font1)
            if nodo.state.getFinalState():
                celda=Label(tabla,text=str(num_estado)+ " f",width=20,borderwidth=1, relief="solid",font=font1)
            if not nodo.state.getFinalState() and num_estado != 0:
                celda=Label(tabla,text=str(num_estado),width=20,borderwidth=1, relief="solid",font=font1)
            celda.grid(row=i,column=l)
            l+=1
            edos=nodo.state.getTransitions()
            #print(edos)
            for transition in edos :
                l=1#Reestablecer columnas
                caracter=transition.getSymbol()
                #print(edo_sig)
                for aux in abecedario:#Para poner guiones
                    #print()
                    if aux==caracter:
                        #celda_sym=Label(tabla,text=str( transition.getState()+","+str),width=20,borderwidth=1, relief="solid",font=font1)
                        celda_sym=Label(tabla,text=str(nodo.state),width=20,borderwidth=1, relief="solid",font=font1)
                        celda_sym.grid(row=i,column=l)
                    else:
                        celda_sym=Label(tabla,text="-",width=20,borderwidth=1, relief="solid",font=font1)
                        celda_sym.grid(row=i,column=l)
                    l+=1
            i+=1
            nodo=nodo.next
        num_letras=len(abecedario)
        m=1
        i=i-1
        while m<=num_letras:
            celda_sym=Label(tabla,text="-",width=20,borderwidth=1, relief="solid",font=font1)
            celda_sym.grid(row=i,column=m)
            m+=1
        canvas.config(scrollregion=canvas.bbox("all"))
    else:
        lexWindow.grab_set()
        messagebox.showerror("Error","introduce un alfabeto")
        lexWindow.grab_release()

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
    direccionArchivo=filedialog.askopenfilename(initialdir=r"Proyecto_compilador\Pruebas_expresiones_reg",title="Abrir",filetypes=(("texto","*.txt"),))
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
