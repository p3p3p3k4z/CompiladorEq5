from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import getpass
from coleccion_canonica import *
from primerosYsiguiente import *
#FINALLLLLL
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
        VentanaPrincipal.state("zoomed")
    except:
        VentanaPrincipal.attributes('-zoomed', True)
        
    VentanaPrincipal.config(background="#F9C0AB")
    font2=("Times New Roman",20)
    archivoLabel=Label(VentanaPrincipal,text="Seleccionar Archivo:",font=font1,width=20,background="#A8CD89",foreground="white")
    archivoLabel.place(x=60,y=30)
    frameGramatica=Frame(VentanaPrincipal,width=400,height=300)
    frameGramatica.place(x=20,y=100)
    frameTablaAS=Frame(VentanaPrincipal,width=1210,height=600)
    frameTablaAS.place(x=350,y=100)
    frameSiguientes=Frame(VentanaPrincipal,width=400,height=300)#Aqui va el frame de siguientes
    frameSiguientes.place(x=20,y=400)#Aqui va el frame de siguientes
    archivoButton=Button(VentanaPrincipal,text="Abrir archivo",width=20,command=lambda:abrirArchivo(VentanaPrincipal,frameGramatica,frameSiguientes),bg="#F4E0AF",font=font1)
    archivoButton.place(x=300,y=20)
    ImprimirResultad0s=Button(VentanaPrincipal,text="Imprimir tabla ",width=20,bg="#F4E0AF",font=font1,command=lambda:ImprimirTablaAS(frameTablaAS))
    ImprimirResultad0s.place(x=300,y=60)
    limpiarButton=Button(VentanaPrincipal,text="Limpiar",width=20,bg="#F4E0AF",font=font1,command=lambda:limpiar(frameTablaAS,frameGramatica,frameSiguientes))
    limpiarButton.place(x=700,y=60)
    
    VentanaPrincipal.mainloop()

def abrirArchivo(Ventana,frameGramatica,frameSiguientes):
    global direccionArchivo
    fuente=("Times New Roman",15)
    Ventana.grab_set()
    direccionArchivo=cargarDireccion()#Abre y almacenamos la direccion del archivo
    listaGramatica=Listbox(frameGramatica)
    listaGramatica.pack()
    archivoGramatica=open(direccionArchivo,encoding="utf-8")
    simboloInicial=archivoGramatica.readline().split()
    #print(simboloInicial)
    Inicial=simboloInicial[0]
    listaGramatica.insert(END,"-----Gramática extendida-----")
    listaGramatica.insert(END,Inicial+"'"+"->"+Inicial+"$")
    listaGramatica.config(font=fuente ,width=30,height=12  )
    archivoGramatica.readline()#leer los terminales
    texto="hola"
    while texto!="":
        texto=archivoGramatica.readline()
        listaGramatica.insert(END,texto)
    archivoGramatica.close()
    ImprimirResultados2(Ventana,frameSiguientes,direccionArchivo)
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
    #print("datos",datos)
    #print("reglas",reglasProduccionTemp)
    return datos,reglasProduccionTemp

def on_key( event,canvas):
       if event.char == "a":
           canvas.xview_scroll(-1, "units")
       elif event.char == "d":
           canvas.xview_scroll(1, "units")
       elif event.char == "w":
           canvas.yview_scroll(-1, "units")
       elif event.char == "s":
           canvas.yview_scroll(1, "units")
           
def ImprimirTablaAS(FrameResultados):
    global direccionArchivo
    datos=mainPyS(direccionArchivo)#Obtiene los primeros y siguientes
    archivo=open(direccionArchivo,encoding="utf-8")
    noTerminales=archivo.readline().split()
    terminales=archivo.readline().split()
    canvasR=Canvas(FrameResultados,width=1100,height=900)
    canvasR.pack()
    frameR=Frame(canvasR)
    canvasR.create_window(0,0,window=frameR,anchor="nw")
    canvasR.update_idletasks()
    canvasR.bind_all("<KeyPress>",  lambda event:on_key  (event,canvasR) )
    canvasR.bind_all("<KeyPress>", lambda event:on_key  (event,canvasR) )
    canvasR.bind_all("<KeyPress>",    lambda event:on_key(event,canvasR) )
    canvasR.bind_all("<KeyPress>",  lambda event:on_key(event,canvasR) )


    Encabezado=Label(frameR,text="Estado",width=10,background="#FFF7D1",foreground="black")
    Encabezado.grid(row=1,column=0,padx=1,pady=1)
    counter=1
    #Diccionario de terminales
    dictionaryTokens={} 
    for i in terminales:#imprime el encabezado de los terminales
        Encabezado=Label(frameR,text=str(i),width=10,background="#FFF7D1",foreground="black")
        Encabezado.grid(row=1,column=counter,padx=1,pady=1)
        dictionaryTokens[i]=counter
        counter+=1
    dictionaryTokens["$"]=counter#agregamos el $ al diccionario de tokens
    Encabezado=Label(frameR,text="$",width=10,background="#FFF7D1",foreground="black")
    Encabezado.grid(row=1,column=counter,padx=1,pady=1)
    counter1=counter+1
    labelAccion=Label(frameR,text="              Accion                ",background="#FFF7D1",foreground="black")
    labelAccion.grid(row=0,column=1,padx=1,pady=1,columnspan=counter)

    #Diccionario de no terminales
    dictionaryNoTerminales={}
    for i in noTerminales:
        counter+=1
        dictionaryNoTerminales[i]=counter
        Encabezado=Label(frameR,text=str(i),width=10,background="#FFF7D1",foreground="black")
        Encabezado.grid(row=1,column=counter,padx=1,pady=1)

    labelAccion=Label(frameR,text="                    Ir A                  ",background="#FFF7D1",foreground="black")#imprime el encabezado de ir a
    labelAccion.grid(row=0,column=counter1,padx=1,pady=1,columnspan=counter)

    ResultadosCanonica=main(direccionArchivo)
    
    #Estados
    fila=2
    arrayEstados=[]
    dictionaryEstados={}
    for j in ResultadosCanonica:
        if j.getEstado() not in arrayEstados and len(j.getEstado())==2:
            aux=j.getEstado()
            arrayEstados.append(aux[0])
            dictionaryEstados[aux[0]]=fila
            EstadoLabel=Label(frameR,text=str(aux[0]),width=10,background="#FFF7D1",foreground="black")
            EstadoLabel.grid(row=fila,column=0,padx=1,pady=1)
            fila+=1
    #print ("array=",arrayEstados)

    #print("diccionarioT=",dictionaryTokens)
    #print ("diccionarioE=",dictionaryEstados)
    #print("diccionarioN=",dictionaryNoTerminales)
    #print("estados:",arrayEstados)
    
    #Desplazamientos
    labels_diccionario = {}
    for j in ResultadosCanonica:#Recorre la lista de objetos tablaColeccionCanonica
        #print(j.getEstadoIr_A(),j.getSimboloIr_A(),j.getEstado()) aca se encontro el errror de que se concateno un espacio en blanco
        if j.getSimboloIr_A() in terminales:#si el simbolo es un terminal
            if len(j.getEstado()[0])!=1:#si el estado es un conjunto
                    fila = dictionaryEstados[j.getEstadoIr_A()]#obtenemos la fila del estado
                    columnaDeToken = dictionaryTokens[j.getSimboloIr_A()]#obtenemos la columna del token
                    DesplazamientoLabel=Label(frameR,text="d"+str(j.getEstado()[0].replace("I","")),width=10,background="#80C4E9",foreground="white")
                    DesplazamientoLabel.grid(row=fila,column=columnaDeToken,padx=1,pady=1)
                    labels_diccionario[fila,columnaDeToken] = DesplazamientoLabel

            else:#si el estado es un solo elemento
                    fila = dictionaryEstados[j.getEstadoIr_A()]#obtenemos la fila del estado
                    columnaDeToken = dictionaryTokens[j.getSimboloIr_A()]#obtenemos la columna del token
                    DesplazamientoLabel=Label(frameR,text="d"+j.getEstado().replace("I",""),width=10,background="#80C4E9",foreground="white")
                    DesplazamientoLabel.grid(row=fila,column=columnaDeToken,padx=1,pady=1)
                    #print("j",j.getEstado())
                    labels_diccionario[fila,columnaDeToken] = DesplazamientoLabel

    #Aceptacion
    for j in ResultadosCanonica:#Recorre la lista de objetos tablaColeccionCanonica
        if j.getSimboloIr_A() == "$":#si el simbolo es un $
            fila = dictionaryEstados[j.getEstadoIr_A()]#obtenemos la fila del estado
            columnaDeToken = dictionaryTokens["$"]#obtenemos la columna del token
            DesplazamientoLabel=Label(frameR,text="Aceptacion",width=10,background="#FFBF61",foreground="white")
            DesplazamientoLabel.grid(row=fila,column=columnaDeToken,padx=1,pady=1)
            labels_diccionario[fila,columnaDeToken] = DesplazamientoLabel
            
    #Reducciones
    auxiliar = []#Para quitar duplicados de getEnviadoACerradura()
    for j in ResultadosCanonica:#Recorre la lista de objetos tablaColeccionCanonica
        #print(j.getEnviadoACerradura())
        if type(j.getEnviadoACerradura()) is list:#Ignora el primer elemento, el cual es una tupla
            if j.getEnviadoACerradura() != auxiliar:#Si la lista no es igual a la anterior
                auxiliar = j.getEnviadoACerradura()#Se iguala la lista anterior a la actual
                for i in j.getEnviadoACerradura():#Recorre la lista de enviados a cerradura
                    longitudProduccion=len(i[1])#Obtenemos la longitud de la produccion
                    if i[1][longitudProduccion-1] == "•":#Si el ultimo elemento de la produccion es un punto
                        for s in datos:#Recorremos la lista de siguientes que vienen en una lista de tuplas ('no terminal',[primeros],[siguientes])
                            if s[0] == i[0]:#Si el no terminal de la produccion es igual al no terminal de la lista de siguientes
                                cadena = "   S("+str(s[0])+")={"+str(listaCadena(s[2])    )+"}"
                                numeroProduccion = ObtenerNumeroDeProduccion(i,reglasProduccionTemp,cadena)
                                if len(j.getEstado()[0])!=1:#si el estado es un conjunto
                                    fila = dictionaryEstados[j.getEstado()[0]]#obtenemos la fila del estado
                                else:
                                    fila = dictionaryEstados[j.getEstado()]
                                #print("fila: ", fila)
                                for siguiente in s[2]:#Recorremos la lista de siguientes
                                    columnaDeToken = dictionaryTokens[siguiente]#obtenemos la columna del token
                                    if labels_diccionario.get((fila,columnaDeToken)) is None:
                                        LabelReduccion=Label(frameR,text="r"+str(numeroProduccion),width=10,background="#176B87",foreground="white")
                                        LabelReduccion.grid(row=fila,column=columnaDeToken,padx=1,pady=1)
                                        labels_diccionario[fila,columnaDeToken] = LabelReduccion
                                    else:
                                        if labels_diccionario.get((fila,columnaDeToken))["text"] != "r"+str(numeroProduccion):
                                            cadenaaa = labels_diccionario.get((fila,columnaDeToken))["text"]
                                            LabelReduccion=Label(frameR,text=cadenaaa+"/r"+str(numeroProduccion),width=10,background="#B31312",foreground="white")
                                            LabelReduccion.grid(row=fila,column=columnaDeToken,padx=1,pady=1)
                                            #labels_diccionario[fila,columnaDeToken] = LabelReduccion
    

    #Ir a
    for j in ResultadosCanonica:#Recorre la lista de objetos tablaColeccionCanonica:
        if j.getSimboloIr_A() in noTerminales:#si el simbolo es un no terminal
            if len(j.getEstado()[0])!=1:#si el estado es un conjunto:
                fila = dictionaryEstados[j.getEstadoIr_A()]#obtenemos la fila del estado
                cadenaAux = j.getEstado()[0]
                cadenaAux = cadenaAux.replace("I","")
            else:
                fila = dictionaryEstados[j.getEstadoIr_A()]
                cadenaAux = j.getEstado()
                cadenaAux = cadenaAux.replace("I","")
            columnaNoTerminal = dictionaryNoTerminales[j.getSimboloIr_A()]
            #print(j.getEstadoIr_A(),j.getSimboloIr_A(),j.getEstado())
            IrALabel=Label(frameR,text=cadenaAux,width=10,background="#80C4E9",foreground="white")
            IrALabel.grid(row=fila,column=columnaNoTerminal,padx=1,pady=1)
            labels_diccionario[fila,columnaNoTerminal] = IrALabel
    terminales.append("$")
    terminales=terminales+noTerminales
    print("array",arrayEstados)
    print("terminales",terminales)
    print("diccionario", labels_diccionario)
    return labels_diccionario,terminales,arrayEstados

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
