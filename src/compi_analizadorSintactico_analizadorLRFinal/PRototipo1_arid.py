import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox

def MostrarTablaTokens(tabla,canvas,lexWindow,arrLabels,archivo_entradas,Prog_lista_tokens,Prog_lista_simbolos,Prog_lista_errores):
    font1=("Times New Roman",11)#definicion de la fuente
    columnas_titulos = ['Lexema', 'Token', '# Linea']#lista con los titulos
    columna=1#se establece la posicion de la columna para la tabla
    lista_Tokens = []#inicializamos las listas
    listaSimbolos_programa = []
    lista_errores = []
    Desgloce_archivo(archivo_entradas, lista_Tokens, listaSimbolos_programa,lista_errores)
    #añade los resultados obtenidos a sus respectivas listas
    Prog_lista_tokens.extend(lista_Tokens)
    Prog_lista_simbolos.extend(listaSimbolos_programa)
    Prog_lista_errores.extend(lista_errores)
    
    for titulo in columnas_titulos:#mostramos los elemtos de titulos en la tabla
        col=Label(tabla,text=titulo,width=20,borderwidth=1, relief="solid",font=font1)
        col.grid(row=0,column=columna)#coloca los elementos en la tabla
        arrLabels.append(col)#guardamos los label para llevar un control
        columna+=1
   
    tabla.update_idletasks()
    numElementos=len(lista_Tokens)#Numero de estados
    i = 1
    if numElementos > 0:#verificamos que haya tokens
        while i <= numElementos:#recorremos los estados
            nodo = lista_Tokens[i-1]#se obtiene informacion del nodo actual
            lexema_nodo = nodo.get_lexema()  # Obtiene el lexema del nodo
            token_nodo = nodo.get_token()    # Obtiene el tipo de token
            nlinea_nodo = nodo.get_nlinea()  # Obtiene el número de línea donde se encuentra el token


            celda_lexema = Label(tabla,text=lexema_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_lexema.grid(row=i,column=1)#mostramos los elementos en la tabla

            celda_token = Label(tabla,text=token_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_token.grid(row=i,column=2)

            celda_nlinea = Label(tabla,text=nlinea_nodo,width=20,borderwidth=1, relief="solid",font=font1)
            celda_nlinea.grid(row=i,column=3)

            i+=1

    else:
        lexWindow.grab_set()#bloquea la interfaz
        messagebox.showerror("Error","Elige un archivo valido")
        lexWindow.grab_release()#libera la interfaz
direccionArchivo= '/home/ari/Escritorio/Proyecto_compilador/ARICITA/codigos_c/ejem1'

def ObtenerTiraTokensExterna(direccionArchivo):
    lineas_entrada = []
    bandera_comentario = False
    contadorL = 0
    
    try:
        with open(direccionArchivo, 'r') as archivo:
            lineas_entrada = archivo.readlines() #Aqui podemos leer todas las lineas del archivo convirtiendolas en una lista con sus saltos de linea

            for n in range(len(lineas_entrada)):
                lineaA = lineas_entrada[n].strip('\n')
                #con strip podemos borrar lo que no queremos de nuestra lista ,en este caso los saltos de linea 

                if not bandera_comentario: #es decir si es null o 0
                    if "//" in lineaA: #validamos si existe // en nuestra lista del archivo
                        lineaA = lineaA.split("//")[0].strip()
                        #aqui se toma la parte antes de encontrar // el [0] valida que se tome esta y el strip elimina los posibles espacios en blanco
                    if "/*" in lineaA:
                        lineaA = lineaA.split("/*")[0].strip() 
                        #lo mismo del anterior pero para comentarios de bloque
                        bandera_comentario=True #con esto ya indicamos que se iniciara un comentario de bloque
                else: #en caso que ya estemos en un comentario de bloque entonces
                    if "*/" in lineaA:
                        lineaA = lineaA.split("*/",1)[1].strip()
                        #Aqui indicamos que se dividira en dos la cadena una antes de */ y otra despues
                        # en este caso es [1] para ahora tomar la parte despues de */ y obviar lo que estaba antes
                        bandera_comentario= False #ya apagamos la bandera para indicar que ya no estamos en un comentario
                    else:
                        lineaA = '' #si no es el final dejamos como si no tuviera nada
                
                lineas_entrada[n] = re.sub(r"\t", " ", lineaA)
                #remplazamos olas tabulacikones por espacios en blanco en nuestro nueva lista sin comentarios
                #y esto sera nuestro nueva linea de entreda
                if lineas_entrada[n].strip():
                    #verifica q quitando los espacios en blanco no este vacia
                    contadorL += 1

            print(direccionArchivo)
    except Exception as e:
        print("Error al abrir el archivo: {e}")
    

    list_tokens=[]
    list_simbolos=[]
    list_errores=[]
    Desgloce_archivo(lineas_entrada,list_tokens,list_simbolos,list_errores)
    
    tiraTokens1 = " ".join(token.get_token() for token in list_token) + " $"
    #aqui nuestra tira de tokens se hace con join juntando tldos los tokens encontrados iguales en listtoken separandolos por espacios y al final agrega un  $

    print ("Tira de tokens:\n" , tiraTokens1)
    print ("Lineas totales:", contadorL)
    return tiraTokens1



# Clase para tokens con tipo de dato y valor
class token_tipo_val:
    def __init__(self, tipo, val):
        self.tipo = tipo
        self.val = val

    def get_tipo(self):
        return self.tipo

    def get_val(self):
        return self.val
    
    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_val(self, val):
        self.val = val

    def __str__(self):
        return self.tipo + ".val = " + str(self.val)
    
# Obtener tira de tokens con objetos token_tipo_val(tipo:token, val:lexema)
def ObtenerTiraTokensExternaObj(direccionArchivo):
    lineas_entrada = []
    Bandera_comentario = False
    lineas_aux = []
    try:
        with open(direccionArchivo, 'r') as archivo:
            # Modificar directamente la lista lineas_entrada
            lineas_entrada.clear()  # Limpiar la lista actual
            lineas_entrada.extend(archivo.readlines())  # Extender la lista con las nuevas líneas
            lineas_aux = lineas_entrada
            for n in range(0, len(lineas_entrada)):     # Revisa si hay comentarios y los elimina
                nueva_cad = ""
                if Bandera_comentario == False:                        # Si no hay un comentario multilínea activo...
                    if (re.search(r'(//.*)|(/\*.*?\*/)', lineas_aux[n]) is not None):   # Si es un comentario de línea o multilínea que cierra en la misma línea...
                        lineas_entrada[n] = re.sub(r'(//.*)|(/\*.*?\*/)', '', lineas_aux[n])
                    if (re.search(r'/\*.*', lineas_aux[n]) is not None):           # Si es un comentario multilínea que no cierra en la misma línea...
                        lineas_entrada[n] = re.sub(r'/\*.*', '', lineas_aux[n])
                        Bandera_comentario = True
                else:                                           # Si hay un comentario multilínea activo...
                    if (re.search(r'.*\*/', lineas_aux[n]) is not None):            # Si se encuentra el cierre del comentario multilínea...
                        lineas_entrada[n] = re.sub(r'.*\*/', '', lineas_aux[n])
                        Bandera_comentario = False
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
    #Procedemos a convertir la lista de tokens a una lista de objetos
    tiraTokens1 = []
    for token_aux in lista_Tokens:
        objTokenAux = token_tipo_val(token_aux.get_token(), token_aux.get_lexema())
        tiraTokens1.append(objTokenAux)

    # Añade el $ al final de la cadena de tokens
    tiraTokens1.append(token_tipo_val("$", "$"))
    #Imprimimos la tira de tokens
    print("Tira de tokens: ", tiraTokens1)
    
    return tiraTokens1