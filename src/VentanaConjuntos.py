from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from VentanaThompson import * #reutilizacion de elemntos
from analizadorLexico_conjuntos import *

def Conjuntos_afn():
    font1=("Times New Roman",12)
    arrLabels=[]
    lexWindow=Toplevel()
    
    try:
        lexWindow.attributes("-zoomed", True)
    except:
        lexWindow.geometry(f"{lexWindow.winfo_screenwidth()}x{lexWindow.winfo_screenheight()}+0+0")
    
    lexWindow.title("Automata finito determinista")
    lexWindow.config(bg="#B5FFFF")
    #82EEFD  #B5FFFF

    archivoL=Label(lexWindow,text="Ingresa una expresion",width=20,bg="#2f2c79",fg="white",font=font1)
    archivoL.place(x=20,y=50)

    archivoButton=Button(lexWindow,text="Inspeccionar",width=26,command=lambda:(abrirArchivo(alphaEntry,erEntry,lexWindow),habilitar_botones()),bg="#2f2c79",fg="white" ,font=font1)
    archivoButton.place(x=210,y=47)

    eregularL=Label(lexWindow,text="Expresión regular:",font=font1,width=20, bg="#2f2c79",fg="white")
    eregularL.place(x=20,y=100)

    erEntry=Entry(lexWindow,width=30,font=font1,bg="#2f2c79",fg="white")
    erEntry.place(x=210,y=101)

    alphaLabel=Label(lexWindow,text="Alfabeto",font=font1,width=20, bg="#2f2c79",fg="white")
    alphaLabel.place(x=20,y=150)

    alphaEntry=Entry(lexWindow,font=font1,width=30, bg="#2f2c79",fg="white")
    alphaEntry.place(x=210,y=151)

    canvas=Canvas(lexWindow,width=1500,height=450, bg="#2f2c79")
    canvas.place(x=0,y=200)
#CAMBIO: se agrego dos funciones def habilitar_botones(): y def deshabilitar_botones(): #####################
    def habilitar_botones():
        afnButton.config(state=NORMAL)
        cleanButton.config(state=NORMAL)

    def deshabilitar_botones():
        afnButton.config(state=DISABLED)
        cleanButton.config(state=DISABLED)

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

#CAMBIO: tabla=Frame(canvas,width=1470,height=300,bg="#2f2c79") ###########################
    tabla=Frame(canvas,width=1470,height=300,bg="#2f2c79")
    canvas.create_window((100, 50), window=tabla, anchor=NW)
    #canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=horizontal_scrollbar.set)

    def on_mousewheel(event):
         canvas.yview_scroll(-1 * (event.delta // 120), "units")
    ##################################################
    #CAMBIO: Se agrego state="disabled"
    afnButton=Button(lexWindow,text="Obtener AFD",width=15,font=font1,bg="#2f2c79",state="disabled",fg="white",command=lambda:printTableConjuntos(alphaEntry.get(),tabla,canvas,lexWindow,arrLabels,erEntry.get()) )
    afnButton.place(x=458,y=97)
    #########################################
    #CAMBIO: se agrego state="disabled" y command=lambda:(cleanTable(tabla,arrLabels,alphaEntry,erEntry),deshabilitar_botones())
    cleanButton=Button(lexWindow,text="Limpiar",font=font1,bg="#2f2c79",state="disabled",fg="white",command=lambda:(cleanTable(tabla,arrLabels,alphaEntry,erEntry),deshabilitar_botones()))
    cleanButton.place(x=605,y=97)
    tabla.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind("<MouseWheel>", on_mousewheel)#posible eliminacion
    canvas.bind_all("<KeyPress-Left>", on_arrow_key)
    canvas.bind_all("<KeyPress-Right>", on_arrow_key)
    canvas.bind_all("<KeyPress-Up>", on_arrow_key_v)
    canvas.bind_all("<KeyPress-Down>", on_arrow_key_v)

def  printTableLexico(alfabeto,tabla,canvas,lexWindow,arrLabels,er):
    expresion_reg = er
    expresion_reg = expresion_postfija(expresion_reg)
    print(expresion_reg)
    Automata=evaluar_expresion_postfija(expresion_reg)
    font1=("Times New Roman",11)
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

def  printTableLexico(alfabeto,tabla,canvas,lexWindow,arrLabels,er):
    expresion_reg = er
    expresion_reg = expresion_postfija(expresion_reg)
    print(expresion_reg)
    Automata=evaluar_expresion_postfija(expresion_reg)
    font1=("Times New Roman",11)
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
    direccionArchivo=filedialog.askopenfilename(initialdir=r"Pruebas_expresiones_reg/",title="Abrir",filetypes=(("texto","*.txt"),))
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
