from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import getpass
from coleccion_canonica import *
from primerosYsiguiente import *
from tabla_canonica import * #DE AQUI RECIBIMOS COINCIDENCIAS
import os

coincidencias_dict = {}  # Definir el diccionario global
bandera_coincidencia = 0
coincidencias = []

def conversorCoincidencia(bandera_coincidencia):  # Se agrega el parámetro
    global coincidencias_dict  # Usar la variable global coincidencias_dict
    
    # Obtener las coincidencias desde la función maint
    coincidencias = maint(bandera_coincidencia)

    # Verificar si coincidencias es una lista de cadenas
    if not isinstance(coincidencias, list):
        print("Error: la función maint no está devolviendo una lista de coincidencias.")
        return
    
    # Imprimir las coincidencias para ver si todo está correcto
    print("Lista de coincidencias final:")
    print(coincidencias)

    # Convertir las coincidencias a un diccionario global
    for coincidencia in coincidencias:
        # Separar la línea por los dos puntos
        if ": " in coincidencia:
            estado, transicion = coincidencia.split(": ", 1)
            
            # Verificar que la clave tenga el formato esperado
            if estado.startswith("I") and estado[1:].isdigit():
                # Filtro adicional para evitar coincidencias no deseadas
                if estado in ['I2', 'I3', 'I5', 'I9', 'I10', 'I11']:  # Filtrar solo las claves conocidas
                    coincidencias_dict[estado.strip()] = transicion.strip()  # Usamos las claves originales
                else:
                    print(f"Advertencia: la clave '{estado}' no está en la lista de claves permitidas.")
            else:
                print(f"Advertencia: la clave '{estado}' no tiene el formato esperado.")
        else:
            print(f"Advertencia: la coincidencia '{coincidencia}' no tiene el formato esperado.")
    
    # Asegurarse de que el diccionario esté ordenado correctamente por las claves numéricas
    coincidencias_dict = dict(sorted(coincidencias_dict.items(), key=lambda item: int(item[0][1:])))
    
    # Ahora tienes un diccionario con las coincidencias
    print("Diccionario de coincidencias ordenado numéricamente:")
    print(coincidencias_dict)

    return coincidencias_dict



class reglaProduccion:
    def __init__(self, b):
        self.base = b
        self.produccion = []
    def getBase(self):
        return self.base
    def getProduccion(self):
        return self.produccion
    def setBase(self, b):
        self.base = b
    def addProduccion(self, p):
        self.produccion.append(p)
    def __str__(self):
        cadena = self.base + " -> " 
        for p in self.produccion:
            cadena += str(p) + " "
        return cadena

def InterfazTablaAS():
    font1=("Times New Roman",14)
    VentanaPrincipal =Toplevel()
    VentanaPrincipal.title("Algoritmo de la colección canónica")
    
    try:
        VentanaPrincipal.attributes("-zoomed", True)
    except:
       VentanaPrincipal.geometry(f"{lexWindow.winfo_screenwidth()}x{lexWindow.winfo_screenheight()}+0+0")
    
    VentanaPrincipal.config(background="#F9C0AB")
    font2=("Times New Roman",20)
    archivoLabel=Label(VentanaPrincipal,text="Seleccionar Archivo:",font=font1,width=20,background="#A8CD89",foreground="white")
    archivoLabel.place(x=60,y=30)
    frameGramatica=Frame(VentanaPrincipal,width=400,height=300)
    frameGramatica.place(x=20,y=100)
    frameTablaAS=Frame(VentanaPrincipal,width=1010,height=600)
    frameTablaAS.place(x=350,y=100)
    frameSiguientes=Frame(VentanaPrincipal,width=400,height=300)#Aqui va el frame de siguientes
    frameSiguientes.place(x=20,y=400)#Aqui va el frame de siguientes
    archivoButton=Button(VentanaPrincipal,text="Abrir archivo",width=20,command=lambda:abrirArchivo(VentanaPrincipal,frameGramatica,frameSiguientes),bg="#F4E0AF",font=font1)
    archivoButton.place(x=300,y=20)
    
    conversorCoincidencia(bandera_coincidencia)
    
    #ESTA ES LA QUE HICE Y LA DEL PROBLEMA XDDDDD
    ImprimirResultad0s = Button(
    VentanaPrincipal, 
    text="Imprimir tabla", 
    width=20, 
    bg="#F4E0AF", 
    font=font1, 
    command=lambda: ImprimirTablaAS(frameTablaAS, coincidencias)
    )
    
    ImprimirResultad0s.place(x=300,y=60)
    limpiarButton=Button(VentanaPrincipal,text="Limpiar",width=20,bg="#F4E0AF",font=font1,command=lambda:limpiar(frameTablaAS,frameGramatica,frameSiguientes))
    limpiarButton.place(x=700,y=60)
    
    VentanaPrincipal.mainloop()

def abrirArchivo(Ventana, frameGramatica, frameSiguientes):
    global direccionArchivo, bandera_coincidencia  # Se declara global para poder modificarla
    fuente = ("Times New Roman", 15)
    Ventana.grab_set()
    
    # Abre y almacena la dirección del archivo
    direccionArchivo = cargarDireccion()
    
    # Obtener el nombre del archivo sin la ruta
    nombreArchivo = os.path.basename(direccionArchivo)
    
    # Asignar el valor de la bandera según el archivo
    if nombreArchivo == "Gramatica1.txt":
        bandera_coincidencia = 1
    elif nombreArchivo == "gramatica2.txt":
        bandera_coincidencia = 2
    elif nombreArchivo == "gramatica3.txt":
        bandera_coincidencia = 3
    elif nombreArchivo == "gramatica4.txt":
        bandera_coincidencia = 4
    elif nombreArchivo == "gramatica5.txt":
        bandera_coincidencia = 5
    else:
        bandera_coincidencia = 1  # Si el archivo no es ninguno de los anteriores
        print("archivo no cargado correctamente o fallo!!!!!")
    
    # Mostrar la bandera en la consola para verificar
    print(f"Bandera para {nombreArchivo}: {bandera_coincidencia}")
    # Crear la lista de gramática
    listaGramatica = Listbox(frameGramatica)
    listaGramatica.pack()
    
    archivoGramatica = open(direccionArchivo, encoding="utf-8")
    simboloInicial = archivoGramatica.readline().split()
    
    Inicial = simboloInicial[0]
    listaGramatica.insert(END, "-----Gramática extendida-----")
    listaGramatica.insert(END, Inicial + "'" + "->" + Inicial + "$")
    listaGramatica.config(font=fuente, width=30, height=12)
    archivoGramatica.readline()  # Leer los terminales
    
    texto = "hola"
    while texto != "":
        texto = archivoGramatica.readline()
        listaGramatica.insert(END, texto)
    
    archivoGramatica.close()
    
    # Llamar a la función para imprimir los resultados
    ImprimirResultados2(Ventana, frameSiguientes, direccionArchivo)
    
    Ventana.grab_release()

def limpiar(frameTablaAS,frameGramatica,frameSiguientes):
    global ruta
    for widget in frameTablaAS.winfo_children():
        widget.destroy()
    for widget in frameGramatica.winfo_children():
        widget.destroy()
    for widget in frameSiguientes.winfo_children():
        widget.destroy()        
    ruta=""

def ImprimirResultados2(Ventana,FrameResultados,direccionArchivo):
    global reglasProduccionTemp
    Ventana.grab_set()
    fuente=("Times New Roman",15)
    lista=Listbox(FrameResultados)
    lista.config(width=30,height=12,font=fuente)
    lista.pack()
    reglasProduccionTemp,listaNoTerminales,listaTerminales=CargadoGramatica2(direccionArchivo)
    #print("reglasProduccionTemp: ", reglasProduccionTemp)
    #print("listaNoTerminales: ", listaNoTerminales)
    #print("listaTerminales: ", listaTerminales)
    lista.insert(END,"-----Siguientes:------")
    datos=mainPyS(direccionArchivo)
    for s in datos:
        cadena=listaCadena(s[2])
        aux=s[0]+" -> "+cadena
        lista.insert(END,aux)
    Ventana.grab_release()
    return datos,reglasProduccionTemp


def ImprimirTablaAS(FrameResultados, coincidencias):
    global direccionArchivo
    datos = mainPyS(direccionArchivo)  # Obtiene los primeros y siguientes
    archivo = open(direccionArchivo, encoding="utf-8")
    noTerminales = archivo.readline().split()
    terminales = archivo.readline().split()
    archivo.close()
    
    canvasR = Canvas(FrameResultados, width=1100, height=900)
    canvasR.pack()
    frameR = Frame(canvasR)
    canvasR.create_window(0, 0, window=frameR, anchor="nw")
    canvasR.update_idletasks()

    # Crear encabezados
    Encabezado = Label(frameR, text="Estado", width=10, background="#FFF7D1", foreground="black")
    Encabezado.grid(row=1, column=0, padx=1, pady=1)
    counter = 1

    # Diccionario de terminales
    dictionaryTokens = {}
    for i in terminales:
        Encabezado = Label(frameR, text=str(i), width=10, background="#FFF7D1", foreground="black")
        Encabezado.grid(row=1, column=counter, padx=1, pady=1)
        dictionaryTokens[i] = counter
        counter += 1
    dictionaryTokens["$"] = counter
    Encabezado = Label(frameR, text="$", width=10, background="#FFF7D1", foreground="black")
    Encabezado.grid(row=1, column=counter, padx=1, pady=1)

    # Imprimir estados y llenar la tabla con datos de `coincidencias`
    fila = 2
    #ACA MODIFIQUE ;-;
    conversorCoincidencia(bandera_coincidencia)
    for estado_id, transicion in coincidencias_dict.items():
        # Obtener el número del estado y las acciones
        estado_num = int(estado_id[1:])  # Quitar el prefijo "I"
        accion, simbolos = transicion.split(" :")

        # Imprimir el estado en la columna de estados
        EstadoLabel = Label(frameR, text=f"I{estado_num}", width=10, background="#FFF7D1", foreground="black")
        EstadoLabel.grid(row=fila, column=0, padx=1, pady=1)

        # Imprimir las acciones en las columnas de terminales
        for simbolo in simbolos.split():
            if simbolo in dictionaryTokens:
                columna = dictionaryTokens[simbolo]
                AccionLabel = Label(frameR, text=accion, width=10, background="#80C4E9", foreground="white")
                AccionLabel.grid(row=fila, column=columna, padx=1, pady=1)

        fila += 1
           
                       

def ObtenerNumeroDeProduccion(i, reglasProduccion,cadena):
    index = 1
    #print("produA:", i)
    produ = str(i[1])
    produ = produ.replace("•","")#Reemplazar el punto
    #Reemplazar primer elemento y ultimo
    produ = produ.removeprefix("[")
    produ = produ.removesuffix("]")

    produ = produ.replace("'","")#Se quita la comilla
    produ = ' '.join(produ.split(', '))#Se quita la coma y el espacio
    produ = str(i[0])+" -> "+produ#Se concatena el no terminal con la produccion
    if produ == str(i[0])+" -> ":#Si la produccion es vacia
        produ = str(i[0])+" -> lamda "
    #print("produS:", produ)
    for regla in reglasProduccion:
        if str(regla) == produ:
            #print("regla:",regla)
            #print(produ+"       r"+str(index)+cadena)
            return index
        index += 1

#Nueva funcion para enlazar el analizador sintactico LR con la tabla de analisis sintactico
def setDireccionArchivo(direccion,reglaProduccion):
    global direccionArchivo
    global reglasProduccionTemp #Variable global para guardar las reglas de produccion
    reglasProduccionTemp = reglaProduccion
    direccionArchivo = direccion


def CargadoGramatica2(direccionArchivo):
    listaNoTerminales = []
    listaTerminales = []
    reglasProduccion = []
    with open(direccionArchivo, 'r', encoding="utf-8") as file:
        lineas = file.readlines()
    index = 0
    for linea in lineas:
        if index == 0:
            #Desglocamos la linea para obtener los no terminales
            linea = linea.replace("\n","")
            listaNoTerminales = linea.split(" ")
            #print(listaNoTerminales)
        if index == 1:
            #Desglocamos la linea para obtener los terminales
            linea = linea.replace("\n","")
            listaTerminales = linea.split(" ")
            #print(listaTerminales)
        if index > 1:
            #procesamos las reglas
            base = linea.split("->")[0].strip() #Se retorna el primer elemento
            produccion = linea.split("->")[1].strip() #Se retorna lo que produce
            produccion = produccion.replace("λ","lamda")
            #print("produccion: ", produccion)
            
            #produccion = produccion.replace("lamda","λ")
            produccion = produccion.split(" ")
            reglasProduccion.append(reglaProduccion(base))
            for p in produccion:
                reglasProduccion[index-2].addProduccion(p.strip('\n'))
        index += 1
    
    return reglasProduccion, listaNoTerminales, listaTerminales

ruta=""
direccionArchivo=""

#InterfazTablaAS()