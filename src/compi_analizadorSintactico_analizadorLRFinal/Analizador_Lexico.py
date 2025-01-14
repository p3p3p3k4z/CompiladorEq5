#Respaldo de mi avance

from Cargado_Datos_AL import *
from tkinter import *
import lexico as lx
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import re

#Añadimos la parte grafica
def Analizador_Lexico():
    font1=("Times New Roman",12)
    arrLabels=[]
    lexWindow=Toplevel()
    lexWindow.state("zoomed")
    lexWindow.title("Analizador Lexico")
    lexWindow.config(bg="#363062")
    lineas_entrada = []
    Prog_lista_tokens = []
    Prog_lista_simbolos = []
    Prog_lista_errores = []

    archivoL=Label(lexWindow,text="Selecciona un archivo .java",width=30,font=font1)
    archivoL.place(x=20,y=25)

    archivoButton=Button(lexWindow,text="Abrir archivo",width=20,command=lambda:abrirArchivo(lexWindow,lineas_entrada),bg="#F99417" ,font=font1)
    archivoButton.place(x=350,y=20)

    canvas=Canvas(lexWindow,width=1500,height=900)
    canvas.place(x=0,y=120)

    def on_arrow_key(event):
            if event.keysym == "Left":
                canvas.xview_scroll(-1, "units")
            elif event.keysym == "Right":
                canvas.xview_scroll(1, "units")
            #canvas.config(scrollregion=canvas.bbox("all"))    

    def on_arrow_key_v(event):
         if event.keysym == "Up":
             canvas.yview_scroll(-1, "units")
         elif event.keysym == "Down":
             canvas.yview_scroll(1, "units")
         #canvas.config(scrollregion=canvas.bbox("all"))
    
    scrollbar=ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    scrollbar.set(0.0, 1.0)
    scrollbar.place(x=5, y=50, height=300)

    horizontal_scrollbar = ttk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
    horizontal_scrollbar.set(0.0,1.0)
    horizontal_scrollbar.place(x=0,y=0,width=300)

    tabla=Frame(canvas,width=1470,height=300)
    canvas.create_window((100, 50), window=tabla, anchor=NW)
    canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=horizontal_scrollbar.set)
    
    ttokenButton=Button(lexWindow,text="Tabla Tokens",width=20,command=lambda:MostrarTablaTokens(tabla,canvas,lexWindow,arrLabels,lineas_entrada,Prog_lista_tokens,Prog_lista_simbolos,Prog_lista_errores),bg="#83A2E8" ,font=font1)
    ttokenButton.place(x=350,y=70)
        
    terroresButton=Button(lexWindow,text="Tabla Errores",width=20,command=lambda:MostrarTablaErrores(tabla,canvas,lexWindow,arrLabels,Prog_lista_errores),bg="#83A2E8" ,font=font1)
    terroresButton.place(x=550,y=70)
    
    tsimbolosButton=Button(lexWindow,text="Tabla Símbolos",width=20,command=lambda:MostrarTablaSimbolos(tabla,canvas,lexWindow,arrLabels,Prog_lista_simbolos,Prog_lista_tokens),bg="#83A2E8" ,font=font1)
    tsimbolosButton.place(x=750,y=70)
    

    def on_mousewheel(event):
         canvas.yview_scroll(-1 * (event.delta // 120), "units")
    
    cleanButton=Button(lexWindow,text="Limpiar",font=font1,bg="#F99417",command=lambda:cleanTable(tabla,arrLabels))
    cleanButton.place(x=550,y=20)
    
    cleanAllButton=Button(lexWindow,text="Limpiar todo",font=font1,bg="#F99417",command=lambda:cleanAll(tabla,arrLabels,Prog_lista_tokens,Prog_lista_simbolos,Prog_lista_errores,lineas_entrada))
    cleanAllButton.place(x=750,y=20)
    
    tabla.update_idletasks()
    #canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<KeyPress-Left>", on_arrow_key)
    canvas.bind_all("<KeyPress-Right>", on_arrow_key)
    canvas.bind_all("<KeyPress-Up>", on_arrow_key_v)
    canvas.bind_all("<KeyPress-Down>", on_arrow_key_v)

def cleanTable(tabla,arrLabels):
    for widget in tabla.winfo_children():
        widget.destroy()
    for widget in arrLabels:
        widget.destroy()
    arrLabels.clear()#Limpiar la lista

def cleanAll(tabla,arrLabels,Prog_lista_tokens,Prog_lista_simbolos,Prog_lista_errores,lineas_entrada):
    for widget in tabla.winfo_children():
        widget.destroy()
    for widget in arrLabels:
        widget.destroy()
    arrLabels.clear()#Limpiar la lista
    lineas_entrada.clear()
    Prog_lista_tokens.clear()
    Prog_lista_simbolos.clear()
    Prog_lista_errores.clear()
    
    
def MostrarTablaTokens(tabla,canvas,lexWindow,arrLabels,lines_entry_file,Prog_lista_tokens,Prog_lista_simbolos,Prog_lista_errores):
    font1=("Times New Roman",11)
    columnas_titulos = ['Lexema', 'Token', '# Linea']
    columna=1
    lista_Tokens = []
    listaSimbolos_programa = []
    lista_errores = []
    file_breakdown(lines_entry_file, lista_Tokens, listaSimbolos_programa,lista_errores)   
    Prog_lista_tokens.extend(lista_Tokens)
    Prog_lista_simbolos.extend(listaSimbolos_programa)
    Prog_lista_errores.extend(lista_errores)
    
    for titulo in columnas_titulos:
        col=Label(tabla,text=titulo,width=20,borderwidth=1, relief="solid",font=font1)
        col.grid(row=0,column=columna)
        arrLabels.append(col)
        columna+=1
   
    tabla.update_idletasks()
    #canvas.config(scrollregion=canvas.bbox("all"))
    numElementos=len(lista_Tokens)#Numero de estados
    i = 1
    if numElementos > 0:
        while i <= numElementos:
            nodo  = lista_Tokens[i-1]
            lexema_nodo = nodo.get_lexema()
            token_nodo  = nodo.get_token()
            nlinea_nodo = nodo.get_nlinea()

            celda_lexema = Label(tabla,text=lexema_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_lexema.grid(row=i,column=1)

            celda_token = Label(tabla,text=token_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_token.grid(row=i,column=2)

            celda_nlinea = Label(tabla,text=nlinea_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_nlinea.grid(row=i,column=3)

            i+=1
        #canvas.config(scrollregion=canvas.bbox("all"))
    else:
        lexWindow.grab_set()
        messagebox.showerror("Error","Elige un archivo valido")
        lexWindow.grab_release()

def ObtenerTiraTokensExterna(direccionArchivo):
    lineas_entrada = []
    flag_coment = False
    lineas_aux = []
    try:
        with open(direccionArchivo, 'r') as archivo:
            # Modificar directamente la lista lineas_entrada
            lineas_entrada.clear()  # Limpiar la lista actual
            lineas_entrada.extend(archivo.readlines())  # Extender la lista con las nuevas líneas
            lineas_aux = lineas_entrada
            for n in range(0, len(lineas_entrada)):     # Revisa si hay comentarios y los elimina
                nueva_cad = ""
                if flag_coment == False:                        # Si no hay un comentario multilínea activo...
                    if (re.search(r'(//.*)|(/\*.*?\*/)', lineas_aux[n]) is not None):   # Si es un comentario de línea o multilínea que cierra en la misma línea...
                        lineas_entrada[n] = re.sub(r'(//.*)|(/\*.*?\*/)', '', lineas_aux[n])
                    if (re.search(r'/\*.*', lineas_aux[n]) is not None):           # Si es un comentario multilínea que no cierra en la misma línea...
                        lineas_entrada[n] = re.sub(r'/\*.*', '', lineas_aux[n])
                        flag_coment = True
                else:                                           # Si hay un comentario multilínea activo...
                    if (re.search(r'.*\*/', lineas_aux[n]) is not None):            # Si se encuentra el cierre del comentario multilínea...
                        lineas_entrada[n] = re.sub(r'.*\*/', '', lineas_aux[n])
                        flag_coment = False
                    else:                                                           # Si aún no se cierra el comentario multilínea...
                        lineas_entrada[n] = ''

                while ("\t" in lineas_entrada[n]):
                    lineas_entrada[n] = re.sub(r"\t", " ", lineas_entrada[n])
                    
            print(direccionArchivo)
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        
    lista_Tokens = []
    listaSimbolos_programa = []
    lista_errores = []
    file_breakdown(lineas_entrada, lista_Tokens, listaSimbolos_programa,lista_errores) 
    #Procedemos a convertir la lista de tokens a una cadena
    tiraTokens1 = ""
    for token_aux in lista_Tokens:
        token_aux = token_aux.get_token()
        tiraTokens1 += token_aux + " "

    # Añade el $ al final de la cadena de tokens
    tiraTokens1 += "$"
    #Imprimimos la tira de tokens
    print("Tira de tokens: ", tiraTokens1)
    
    return tiraTokens1
        
    

def MostrarTablaSimbolos(tabla,canvas,lexWindow,arrLabels,Prog_lista_simbolos,Prog_lista_tokens):
    font1=("Times New Roman",11)
    columnas_titulos = ['id', 'valor', 'funcion']
    columna=1
    
        
    detectarFuncion_tSimbolos(Prog_lista_simbolos,Prog_lista_tokens)
    #Hacemos una limpieza de la lista de simolos, para que no haya elementos repetidos.
    Prog_lista_simbolos = eliminar_duplicados(Prog_lista_simbolos)
    
    hacerSeguimientodelValor(Prog_lista_simbolos,Prog_lista_tokens)
    print("Lo que esta saliendo de funcion")
    for sim in Prog_lista_simbolos:
        print(sim)
    
    
    #Se debe eliminar los simbolos después del primero que este asociado a la misma funcion
    contador_id =0 #contador_id es cuantas veces aparece un id asociado al mismo simbolo
    contador_posiciones = 0 #posicion del simbolo a eliminar en la lista
    for simbolo in Prog_lista_simbolos:
        contador_id = 0#contador_id es cuantas veces aparece un id asociado al mismo simbolo
        for s in Prog_lista_simbolos:
            #print("s.get_identificador()",s.get_identificador())
            #print("contador_posciones",contador_posiciones)
            #print("contador_id",contador_id)
            if s.get_identificador() == simbolo.get_identificador() and s.get_funcion() == simbolo.get_funcion():
                contador_id += 1
                if contador_id > 1: #hay mas de un id asociado al mismo simbolo
                    #print("Entro al caso de repeticion contador_id y contador posiciones",contador_id, "",contador_posiciones)
                    Prog_lista_simbolos.pop(contador_posiciones)
                    contador_id = 0
            contador_posiciones += 1
            
        contador_posiciones = 0 #reiniciamos cada que es un nuevo simbolo
    
        
        
    for titulo in columnas_titulos:
        col=Label(tabla,text=titulo,width=20,borderwidth=1, relief="solid",font=font1)
        col.grid(row=0,column=columna)
        arrLabels.append(col)
        columna+=1
   
    tabla.update_idletasks()
    #canvas.config(scrollregion=canvas.bbox("all"))
    numElementos=len(Prog_lista_simbolos)#Numero de estados
    i = 1
    if numElementos > 0:
        while i <= numElementos:
            nodo  = Prog_lista_simbolos[i-1]
            id_nodo = nodo.get_identificador()
            valor_nodo  = nodo.get_valor()
            funcion_nodo = nodo.get_funcion()

            celda_id = Label(tabla,text=id_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_id.grid(row=i,column=1)

            celda_valor = Label(tabla,text=valor_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_valor.grid(row=i,column=2)

            celda_funcion = Label(tabla,text=funcion_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_funcion.grid(row=i,column=3)

            i+=1
        #canvas.config(scrollregion=canvas.bbox("all"))
    else:
        lexWindow.grab_set()
        messagebox.showerror("Error","Elige un archivo valido")
        lexWindow.grab_release()    
 
def MostrarTablaErrores(tabla,canvas,lexWindow,arrLabels,Prog_lista_errores):   
    font1=("Times New Roman",11)
    columnas_titulos = ['simbolo', 'descripcion', 'nlinea']
    columna=1
    
    for titulo in columnas_titulos:
        col=Label(tabla,text=titulo,width=20,borderwidth=1, relief="solid",font=font1)
        col.grid(row=0,column=columna)
        arrLabels.append(col)
        columna+=1
   
    tabla.update_idletasks()
    #canvas.config(scrollregion=canvas.bbox("all"))
    numElementos=len(Prog_lista_errores)#Numero de estados
    i = 1
    if numElementos > 0:
        while i <= numElementos:
            nodo  = Prog_lista_errores[i-1]
            simbolo_nodo = nodo.get_simbolo()
            descripcion_nodo  = nodo.get_descripcion()
            nlinea_nodo = nodo.get_nlinea()

            celda_simbolo = Label(tabla,text=simbolo_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_simbolo.grid(row=i,column=1)

            celda_descripcion = Label(tabla,text=descripcion_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_descripcion.grid(row=i,column=2)
            
            celda_nlinea = Label(tabla,text=nlinea_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_nlinea.grid(row=i,column=3)


            i+=1
        #canvas.config(scrollregion=canvas.bbox("all"))
    else:
        lexWindow.grab_set()
        lexWindow.grab_release()    

def abrirArchivo(lexWindow, lineas_entrada):
    flag_coment = False
    lineas_aux = []
    lexWindow.grab_set()
    direccionArchivo=filedialog.askopenfilename(initialdir=r"C:\Users\Documents\Compiladores",title="Abrir",filetypes=(("java","*.java"),))
    
    try:
        with open(direccionArchivo, 'r') as archivo:
            # Modificar directamente la lista lineas_entrada
            lineas_entrada.clear()  # Limpiar la lista actual
            lineas_entrada.extend(archivo.readlines())  # Extender la lista con las nuevas líneas
            lineas_aux = lineas_entrada
            for n in range(0, len(lineas_entrada)):     # Revisa si hay comentarios y los elimina
                nueva_cad = ""
                if flag_coment == False:                        # Si no hay un comentario multilínea activo...
                    if (re.search(r'(//.*)|(/\*.*?\*/)', lineas_aux[n]) is not None):   # Si es un comentario de línea o multilínea que cierra en la misma línea...
                        lineas_entrada[n] = re.sub(r'(//.*)|(/\*.*?\*/)', '', lineas_aux[n])
                    if (re.search(r'/\*.*', lineas_aux[n]) is not None):           # Si es un comentario multilínea que no cierra en la misma línea...
                        lineas_entrada[n] = re.sub(r'/\*.*', '', lineas_aux[n])
                        flag_coment = True
                else:                                           # Si hay un comentario multilínea activo...
                    if (re.search(r'.*\*/', lineas_aux[n]) is not None):            # Si se encuentra el cierre del comentario multilínea...
                        lineas_entrada[n] = re.sub(r'.*\*/', '', lineas_aux[n])
                        flag_coment = False
                    else:                                                           # Si aún no se cierra el comentario multilínea...
                        lineas_entrada[n] = ''

                while ("\t" in lineas_entrada[n]):
                    lineas_entrada[n] = re.sub(r"\t", " ", lineas_entrada[n])
                    
            print(direccionArchivo)
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
    
    lexWindow.grab_release()









#__________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________

#Clase para la tabla de tokens
class element_TokenTable:
    def __init__(self, lexema, token,nl):
        self.lexema = lexema
        self.token = token
        self.nlinea = nl

    def get_lexema(self):
        return self.lexema

    def get_token(self):
        return self.token
    
    def get_nlinea(self):
        return self.nlinea

    def set_lexema(self, lexema):
        self.lexema = lexema

    def set_token(self, token):
        self.token = token
    
    def set_nlinea(self, nl):
        self.nlinea = nl

    def __str__(self):
        return self.lexema + " " + self.token+ " " + str(self.nlinea)

#clase para la tabla de errores
class element_ErrorTable:  
    def __init__(self, simbolo,descripcion,nlinea):
        self.simbolo = simbolo
        self.descripcion = descripcion 
        self.nlinea = nlinea
    
    def get_simbolo(self):
        return self.simbolo
    
    def get_nlinea(self):
        return self.nlinea
    
    def get_descripcion(self):
        return self.descripcion
    
    def set_nlinea(self, nlinea):
        self.nlinea = nlinea
    
    def set_descripcion(self, descripcion):
        self.descripcion = descripcion
    
    def set_simbolo(self, simbolo):
        self.simbolo = simbolo
        
#clase para la tabla de simbolos
class element_SymbolTable:
    def __init__(self,identificador, v, funcion):
        self.identificador = identificador
        self.valor = v
        self.funcion = funcion
    
    def get_identificador(self):
        return self.identificador
    
    def get_valor(self):
        return self.valor
    
    def get_funcion(self):
        return self.funcion
    
    def set_identificador(self, identificador):
        self.identificador = identificador

    def set_valor(self, v):
        self.valor = v
    
    def set_funcion(self, funcion):
        self.funcion = funcion
    
    def __str__(self):
        return str(self.identificador) + " " + str(self.valor)+ " " + str(self.funcion)

#Función que desgloza el archivo de entrada 
def file_breakdown (lines, tokenList,symbolList_prog,errorList_prog):
    nline = 0
    for line in lines:
        nline+=1
        aux=""
        posNum = ""
        posSimb = ""
        flag_string = False
        flag_found1 = flag_found_id = flag_found_num = flag_found_float=False
        flag_chkLex = False
        flag_comilla_simple = False
        for char in line:

            # Si es espacio, y no es cadena, se activa la bandera para revisar el lexema
            #print("flag_string: ",flag_string)
            if (char == ' ' or char == '\n' ) and flag_string == False: 
                flag_chkLex = True
            else:
                aux+=char

            # Si son comillas, revisar el estado de la bandera de cadena
            #print("aux: ",aux)
            if (char == '"' and flag_string == True) or (flag_string == True and char == "'"): #Se encontro el fin de la cadena
                #print(len(aux), "aux: ", aux)
                #print("flag_comilla:", flag_comilla_simple)
            
                if char == "'" and flag_comilla_simple == True:
                    tokenList.append(element_TokenTable(aux,"literalCar",nline)) #Literal caracter
                else:
                    tokenList.append(element_TokenTable(aux, "varCadena", nline)) #Agregamos a la lista de tokens
                flag_string = False
                aux=""
            elif (char == '"' and flag_string == False) or (char == "'" and flag_string == False): #Es una cadena, se empieza a guardar y se enciende la bandera y asi si esta la bandera encendida esperamos el siguiente
                flag_string = True
                if char == "'":
                    flag_comilla_simple = True

            # Revisa si el caracter actual es un símbolo
            if char in lista_simbolos and flag_string == False: #Es un simbolo
                if (flag_found_float == True):                  # Si ya se ha encontrado un punto antes en el número...
                    tokenList.append(element_TokenTable(posNum, "nfloat", nline))   # Agrega el número decimal de posNum
                    posSimb += char                 # Agrega el símbolo encontrado a simbPos
                    flag_found_float = False
                    posNum = ""
                    aux = ""
                elif (posNum != "" and char != "."):            # Si hay un número entero posible, pero el símbolo no es un punto...
                    tokenList.append(element_TokenTable(posNum, "nint", nline))     # Agrega el número entero de posNum
                    posSimb += char                 # Agrega el símbolo encontrado a simbPos
                    posNum = ""
                    aux = ""
                elif (posNum == "" and aux != char and char != "_"):   # Si no hay número posible, pero aux no está vacío...
                    id_aux = ""
                    for i in range(0, len(aux)-1):
                        id_aux = id_aux + aux[i]    # Crea una cadena sin el último símbolo recién leido
                    flag_found_id = es_id(id_aux, nline, tokenList)
                    if flag_found_id is True:
                        #if (not BuscarSimbolo_ts(aux, symbolList_prog)):    # No existe en la tabla
                        symbolList_prog.append(element_SymbolTable(id_aux, "null", "null"))
                        flag_found_id = False
                    else:
                        errorList_prog.append(element_ErrorTable(id_aux, "ERROR", nline))
                    posSimb += char                 # Agrega el símbolo encontrado a simbPos
                    aux = ""
                elif (posNum == ""):                # Si no hay números posibles almacenados
                    posSimb += char
                    if len(posSimb) == 2:           # Si ya hay dos símbolos almacenados...
                        if posSimb in lista_simbolos:   # Si posSimb es un símbolo válido...
                            tokenList.append(element_TokenTable(posSimb, posSimb, nline))       # Se añade el símbolo de posSimb
                            posSimb = ""                                                        # Y se resetea posSimb
                        else:                           # Si posSimb NO es un símbolo válido...
                            tokenList.append(element_TokenTable(posSimb[0], posSimb[0], nline)) # Se añade solo el primer símbolo de posSimb y
                            posSimb = posSimb[1]                                                # Solo se queda el segundo símbolo en posSimb

                aux = ""
            else:           # Si el caracter leído NO es símbolo...
                if posSimb != "":       # Si hay símbolo guardado...
                    tokenList.append(element_TokenTable(posSimb, posSimb, nline))   # Se agrega el símbolo de posSimb
                    posSimb = ""                                                    # Y se resetea posSimb

            if flag_string == False:        # Si no es cadena, revisa el estado actual de aux y char...
                ##print(len(aux))
                ##print("Evaluacion de número entero")        # Busca si es un entero
                ##print("posNum: ", posNum)
                flag_found_num = es_numero(char) and es_numero(aux) 
                
                if posNum != "" and char == '.': #Evaluamos si posNum es diferente de vacio y existe un punto, porque entonces existe un flotante
                    ##print("Evaluacion de un flotante")
                    flag_found_float = True
                    posNum += char #Agregamos el punto al numero
                    pass
                
                if flag_found_num == True:
                    posNum += char
                    flag_found_num = False
                    pass
                elif flag_found_float == False:
                    if posNum != "" and char in lista_simbolos:     # Si hay un número entero posible
                        tokenList.append(element_TokenTable(posNum, "nint", nline))
                        posNum = ""
                
                if flag_found_float == True and char != '.' and flag_found_num == False:
                    if posNum != "" and char in lista_simbolos:     # Si hay un número flotante posible
                        tokenList.append(element_TokenTable(posNum, "nfloat", nline))
                        flag_found_float = False
                        posNum = ""

                #print("Evaluacion de palabra reservada")    # Busca si es una palabra reservada
                flag_found1 = word_search(aux, nline, tokenList)
                #print("flag_found1: ",flag_found1)
                if (flag_found1 == True):
                    flag_found1 = False
                    aux=""
                elif flag_chkLex == True:       # Si se detecta un espacio, puede haber una palabra por revisar
                    #print("Evaluación de id")   # Busca si es un id
                    flag_found_id = es_id(aux, nline, tokenList)
                    if flag_found_id is True:
                        #if (not BuscarSimbolo_ts(aux, symbolList_prog)):    # No existe en la tabla
                        symbolList_prog.append(element_SymbolTable(aux, "null", "null"))
                        flag_found_id = False
                    elif (len(aux)>0):
                        errorList_prog.append(element_ErrorTable(aux, "ERROR", nline))
                    flag_chkLex = False
                    aux = ""
                pass
        if posSimb != "":
            tokenList.append(element_TokenTable(posSimb, posSimb, nline))
        if posNum != "":
            if "." in posNum:
                tokenList.append(element_TokenTable(posNum, "nfloat", nline))
            else:
                tokenList.append(element_TokenTable(posNum, "nint", nline))
        if aux != "":
            flag_found1 = word_search(aux, nline, tokenList)
            if (flag_found1 == True):
                flag_found1 = False
                aux=""
            else:
                flag_found_id = es_id(aux, nline, tokenList)
                if flag_found_id is True:
                    #if (not BuscarSimbolo_ts(aux, symbolList_prog)):    # No existe en la tabla
                    symbolList_prog.append(element_SymbolTable(aux, "null", "null"))
                    flag_found_id = False
                else:
                    errorList_prog.append(element_ErrorTable(aux, "ERROR", nline))

                    
def contar_llaves(tokens):
    #print("Contando llaves...")
    contador_llaves = []
    maximo_llaves = 0
    contador = 0
    for token in tokens:
        t = token.get_token()
        if t == "{":
            #print("detecto la llave {")
            contador += 1
            if maximo_llaves < contador:
                maximo_llaves = contador
        elif t == "}":
            #print("detecto la llave }")
            contador -= 1
            if contador == 0:
                #print("conta =0")
                contador_llaves.append(maximo_llaves)
                maximo_llaves = 0
            elif contador < 0:
                print("Error: Llave de cierre sin llave de apertura")            
    return contador_llaves
                    
def detectarFuncion_tSimbolos(symbolList_prog, tokenList_prog):
    #print("Detectando funciones...")
    flag_solo_un_id = False
    identificador_principal = None
    for i, token in enumerate(tokenList_prog):
        if token.get_token() == "id" or token.get_token() == "main":
            if token.get_token() == 'main': #Es la función principal
                if not 'main' in [s.get_identificador() for s in symbolList_prog]:
                    symbolList_prog.append(element_SymbolTable(token.get_token(), "null", "Es la función principal"))
                identificador_principal = 'main'
                pass
            
            ##print("token[i-1].get_token():", tokenList_prog[i - 1].get_token())
            ##print("token[i+1].get_token():", tokenList_prog[i + 1].get_token()) 
             #Procedemos a identificar si es una clase
            elif (i > 0 and tokenList_prog[i - 1].get_token() == 'class' and tokenList_prog[i + 1].get_token() =='{') :
                #print("Identificador de clase")
                identificador_clase = tokenList_prog[i].get_lexema() 
                for simbolo in symbolList_prog:
                    if simbolo.get_identificador() == identificador_clase:
                        simbolo.set_funcion("Es una clase")
                pass
                        
            elif (i > 0 and tokenList_prog[i - 1].get_token() in [td for td in lista_tipo_datos] and tokenList_prog[i + 1].get_token() =='(') : #hay un tipo de retorno antes del id así que es una función
                #print("Identificador de función")
                identificador_principal = tokenList_prog[i].get_lexema() 
                for simbolo in symbolList_prog:
                    if simbolo.get_identificador() == identificador_principal:
                        simbolo.set_funcion("Es una función");
                pass
            elif identificador_principal is not None:  #Es un id dentro de una función del nombre contenido por idenficador_principal
                #print("Es un id dentro de una funcion")
                for simbolo in symbolList_prog:
                    if simbolo.get_identificador() == token.get_lexema() and simbolo.get_funcion() == "null":
                        if flag_solo_un_id == False: #Solo puede afectar a un simbolo, un id
                            flag_solo_un_id = True
                            simbolo.set_funcion(identificador_principal)
                flag_solo_un_id = False  

    #for simbolo in symbolList_prog:
        #print(simbolo)
    

def hacerSeguimientodelValor(symbolList_prog,tokenList_prog):
    for i, token in enumerate(tokenList_prog):
            if token.get_token() == 'main': #Es la función principal
                identificador_principal = 'main'
                pass
                        
            elif (i > 0 and tokenList_prog[i - 1].get_token() in [td for td in lista_tipo_datos] and tokenList_prog[i + 1].get_token() =='(') : #hay un tipo de retorno antes del id así que es una función
                #print("Identificador de función")
                identificador_principal = tokenList_prog[i].get_lexema() 
            
        
            elif token.get_lexema() == "=":
                if i > 0 and tokenList_prog[i - 1].get_lexema() in [s.get_identificador() for s in symbolList_prog]:
                    # Encontramos un símbolo seguido por un "=" y hay un token antes de "=" que es un identificador válido
                    identificador = tokenList_prog[i - 1].get_lexema()
                    index_igual = i 

                    while i < len(tokenList_prog) and tokenList_prog[i].get_lexema() != ";":
                        i += 1

                    index_punto_coma = i

                    if index_punto_coma is not None:
                        #print("index_igual:", index_igual)
                        #print("index_punto_coma:", index_punto_coma)
                        valor_token_siguiente = " ".join(token.get_lexema() for token in tokenList_prog[index_igual + 1 : index_punto_coma])

                    for simbolo in symbolList_prog:
                        if simbolo.get_identificador() == identificador and simbolo.get_funcion() == identificador_principal:
                            simbolo.set_valor(valor_token_siguiente)
                            break

    for simbolo in symbolList_prog:
        print(simbolo)



                
def BuscarSimbolo_ts(id, symbolList_prog): #Se verifica que no este en la tabla de simbolos
    for simbolo in symbolList_prog:
        if simbolo.get_identificador() == id:
            return True #Ya existe en la tabla, no se añade
    return False #No existe en la tabla, se añade
                
def eliminar_duplicados(lista):
    nueva_lista = []
    for elemento in lista:
        if not any(e.identificador == elemento.identificador and e.funcion == elemento.funcion for e in nueva_lista):
            nueva_lista.append(elemento)
    return nueva_lista



def word_search(word, nline, tokenList):
    if word in lista_pReservadas: 
        tokenList.append(element_TokenTable(word, word, nline)) #Agregamos a la lista de tokens
        return 1
    return 0
    
def es_numero(cadena):
    try:
        int(cadena) # Intenta convertir la cadena a un entero
        return True
    except ValueError:
        return False # La conversión a entero falló, no es un número
    
def es_nint_re(cadena):
    prueba = re.match(r'[0-9]*(?!\.)', cadena)    # Cualquier repetición de números, pero sin un punto decimal al final
    if prueba is not None:
        return True
    return False

def es_float_re(cadena):
    prueba = re.match(r'[0-9]*\.[0-9]', cadena)   # Dos repeticiones de números, con un punto decimal entre ellas
    if prueba is not None:
        return True
    return False
    
def es_id(cadena, nline, tokenList):
    prueba = re.match('(^[a-zA-Z][a-zA-Z0-9_]*$)|(^[_]+[a-zA-Z0-9]+[a-zA-Z0-9_]*$)', cadena)
    if prueba is not None:
        tokenList.append(element_TokenTable(cadena, "id", nline))
        return True     # Encontró un nombre que empieza por letra, y contiene letras, números, $ ó _
    return False

def es_cad(cadena):
    prueba = re.match('".*"', cadena)
    if prueba is not None:
        return True     # Encontró una frase que está encerrada entre comillas dobles
    return False

def es_car(cadena):
    prueba = re.match("'.'", cadena)
    if prueba is not None:
        return True     # Encuentra un solo caracter entre comillas simples
    return False
    
    
#_____________________________________________________________________________________________________________________________________