from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from lexico import *
from Analizador_Lexico import *
from TablaAnalisisSintactico import *
from PrimerosYSiguientes import mainPyS
def analizadorSintacticoJava():
    VentanaPrincipal =Toplevel()
    VentanaPrincipal.title("Analizador sintáctico")
    try:
        VentanaPrincipal.state("zoomed")
    except:
        VentanaPrincipal.attributes('-zoomed', True)
    VentanaPrincipal.config(background="#363062")
    encabezado(VentanaPrincipal)
    VentanaPrincipal.mainloop()

def encabezado(VentanaPrincipal):
    font1=("Times New Roman",14)
    font2=("Times New Roman",20)
    archivoLabel=Label(VentanaPrincipal,text="Seleccionar Archivo:",font=font1,width=20,background="#363062",foreground="white")
    archivoLabel.place(x=60,y=30)
    archivoButton=Button(VentanaPrincipal,text="Abrir archivo",width=20,command=lambda:abrirArchivo(VentanaPrincipal),bg="#F99417",font=font1)
    archivoButton.place(x=300,y=20)
    tokenButton=Button(VentanaPrincipal,text="Seleccionar tira de tokens",width=20,bg="#F99417",font=font1,command=lambda:abrirArchivo1(VentanaPrincipal))
    tokenButton.place(x=300,y=100)
    ImprimirResultad0s=Button(VentanaPrincipal,text="Imprimir Resultados",width=20,bg="#F99417",font=font1,command=lambda:imprimirResultados(VentanaPrincipal))
    ImprimirResultad0s.place(x=500,y=60)
    limpiarButton=Button(VentanaPrincipal,text="Limpiar",width=20,bg="#F99417",font=font1,command=lambda:limpiar(VentanaPrincipal))
    limpiarButton.place(x=700,y=60)

def cargarGramatica(Ventana,direccionArchivo):
    global Gramatica
    frameGramatica=Frame(Ventana,width=300,height=600)
    frameGramatica.place(x=60,y=100)
    archivo=open(direccionArchivo,"r",encoding="utf-8")
    Gramatica=[]
    linea=archivo.readline()
    linea=archivo.readline()
    contador=0
    while linea:
        linea=archivo.readline()
        grama=linea
        grama=grama.replace("\n","")
        Gramatica.append(grama) #aqui se guarda la gramatica sin el salto de linea
        mostrarRegla=Label(frameGramatica,text=str(linea),font=("Times New Roman",14),width=20)
        mostrarRegla.grid(row=contador,column=0)
        contador+=1

def abrirArchivo(Ventana):
    global direccionArchivo2
    Ventana.grab_set()
    username=getpass.getuser()
    ruta_proyecto = r"C:\Users\{username}\Documents\ProyectoCompiladores"
    direccionArchivo2= "Pruebas_Archivos_Entrada_JAVA/entradaLR.txt"
    cargarGramatica(Ventana,direccionArchivo2)

def abrirArchivo1(Ventana):
    global tiraTokens
    Ventana.grab_set()
    username=getpass.getuser()
    ruta_proyecto = r"C:\Users\{username}\Documents\ProyectoCompiladores"
    direccionArchivo=filedialog.askopenfilename(initialdir=ruta_proyecto,title="Abrir Archivo",filetypes=(("java","*.java"),))
    tiraTokens = ObtenerTiraTokensExterna(direccionArchivo)
    print("Tira de tokens recibida en el sintáctico:\n", tiraTokens)


def imprimirResultados(Ventana):
    global tiraTokens
    global direccionArchivo2
    global Gramatica
    ventanaResultados=Toplevel()
    ventanaResultados.title("Resultados")
    try:
        ventanaResultados.state("zoomed")
    except:
        ventanaResultados.attributes('-zoomed', True)
    ventanaResultados.grab_set()
    frameResultados=Frame(ventanaResultados,width=300,height=600)
    frameResultados.place(x=60,y=100)
    ventana2=Toplevel()
    frame2=Frame(ventana2,width=300,height=600)
    #Esto es lo que hay que arreglar
    datos,reglas=ImprimirResultados2(ventana2,frame2,direccionArchivo2)
    ventana2.destroy()
    setDireccionArchivo(direccionArchivo2,reglas)
    variable,simbolos,estados=ImprimirTablaAS(ventanaResultados,frameResultados)#variable es un diccionario con clave el numero de estado y la columna y contenido un label con el contenido de la tabla
    for var in variable:
        contenido=variable[var]
        cont=contenido.cget("text")
        print("clave:",var,"contenido:",cont)
    #print("simbolos:",simbolos)
    #print("estados:",estados)
    tira=tiraTokens.split(" ")
    print("tiraTokens:",tira)
    tuplasimbolos=()
    arreglosimbolos=[]
    j=0
    for i in simbolos:
        j=j+1
        tuplasimbolos=(i,j)
        arreglosimbolos.append(tuplasimbolos)
    tuplaGrama=()
    arreGramatica=[]
    Gramatica=list(filter(lambda x: x is not None and x != "", Gramatica)) #aqui se quitan los elementos vacios de la lista
    for grama in Gramatica:
        grama=grama.split("->")
        tuplaGrama=(grama[0],grama[1])
        arreGramatica.append(tuplaGrama)
    print("Gramatica:",arreGramatica)
    print("simbolos:",arreglosimbolos)
    print("funcion")
    TablaLr(variable,arreglosimbolos,tira,arreGramatica,Ventana)
    ventanaResultados.grab_release()

    
def TablaLr(variable,simbolos,tira,arreGramatica,Ventana):
    Ventana.grab_set()
    tabla=Frame(Ventana,width=900,height=600)
    tabla.place(x=300,y=150)
    contadorFila=0
    pila=[]
    accion=[]
    pila.append(0)
    font1=("Times New Roman",14)
    labelTextPila=Label(tabla,text="Pila",width=20,font=font1,borderwidth=2,relief="solid")
    labelTextPila.grid(row=contadorFila,column=0)
    labelTextTira=Label(tabla,text="Entrada",width=30,font=font1,borderwidth=2,relief="solid")
    labelTextTira.grid(row=contadorFila,column=1)
    labelTextSalida=Label(tabla,text="Salida",width=40,font=font1,borderwidth=2,relief="solid")
    labelTextSalida.grid(row=contadorFila,column=2,columnspan=2)
    contadorFila+=1
    while((len(tira)>0) & (accion!='Aceptacion') & (accion!='')):
        a=tira[0]
        sacarTira=tira[0]
        labelPila=Label(tabla,text=pilaCadena(pila),width=20,font=font1,borderwidth=2,relief="solid")
        labelPila.grid(row=contadorFila,column=0) 
        labelTira=Label(tabla,text=pilaCadena(tira),width=30,font=font1,borderwidth=2,relief="solid")
        labelTira.grid(row=contadorFila,column=1)
        simboloTira=buscarSimbolo(simbolos,sacarTira)
        print("simbolo en la tira:",simboloTira)
        estado=pila.pop()
        pila.append(estado)
        entero=int(estado)
        entero=entero+2
        print("estado en el que vamos:",entero)
        accion=buscarAccion(variable,entero,simboloTira)
        if(accion != None):
            if(accion[0]=='d'):
                tira.pop(0)
                print("salida:",accion) #imprimimos la accion de desplazamiento o reduccion
                labelSalida=Label(tabla,text=pilaCadena(accion),width=20,font=font1,borderwidth=2,relief="solid")
                labelSalida.grid(row=contadorFila,column=2)
                labelRegla=Label(tabla,text=" ",width=20,font=font1,borderwidth=2,relief="solid")
                labelRegla.grid(row=contadorFila,column=3)
                pila.append(a)
                estadoAgregar=int(accion[1])
                pila.append(estadoAgregar)
                print("contenido de la pila:",pila)
                print("tira de tokens despues del desplazamiento:",tira)
            elif(accion[0]=='0'or accion[0]=='1' or accion[0]=='2' or accion[0]=='3' or accion[0]=='4' or accion[0]=='5' or accion[0]=='6' or accion[0]=='7' or accion[0]=='8' or accion[0]=='9'):
                tira.pop(0)
                print("salida:",accion) #imprimimos la accion de desplazamiento o reduccion
                labelSalida=Label(tabla,text=pilaCadena(accion),width=20,font=font1,borderwidth=2,relief="solid")
                labelSalida.grid(row=contadorFila,column=2)
                labelRegla=Label(tabla,text=" ",width=20,font=font1,borderwidth=2,relief="solid")
                labelRegla.grid(row=contadorFila,column=3)
                pila.append(a)
                estadoAgregar=int(accion[0])
                pila.append(estadoAgregar)
                print("contenido de la pila:",pila)
                print("tira de tokens despues del desplazamiento:",tira)
            elif(accion[0]=='r'):  #reducir A→β
                print("es una reduccion")
                pos=int(accion[1])
                regla=arreGramatica[pos-1]
                labelSalida=Label(tabla,text=pilaCadena(accion),width=20,font=font1,borderwidth=2,relief="solid")
                labelSalida.grid(row=contadorFila,column=2)
                #imprimir la producción A→β
                print("Regla:",regla)
                labelRegla=Label(tabla,text=str(regla[0])+"->"+str(regla[1]),width=20,font=font1,borderwidth=2,relief="solid")
                labelRegla.grid(row=contadorFila,column=3)
                tama=len(regla[1].split(' ')) #calculamos el tamaño de β
                tama=tama*2 
                for k in range(0,tama):
                    pila.pop()  #pop 2*|β| símbolos
                print("contenido de la pila despues de eliminar:",pila)
                pila.append(regla[0])   #push A
                print("contenido de la pila despues de agregar A:",pila)
                simbIra=buscarSimbolo(simbolos,pila[len(pila)-1]) 
                #s=Ir_a[j,A]
                s=buscarAccion(variable,pila[len(pila)-2]+2,simbIra) 
                #push s
                pila.append(s)
                print("contenido de la pila despues de agregar s:",pila)
                print("tira de tokens despues de la reduccion:",tira)  
            elif(accion=='Aceptacion'):
                print("Aceptado")
                labelRegla=Label(tabla,text="Aceptacion",width=20,font=font1,borderwidth=2,relief="solid")
                labelRegla.grid(row=contadorFila,column=2)
                label2=Label(tabla,text=" ",width=20,font=font1,borderwidth=2,relief="solid")
                label2.grid(row=contadorFila,column=3)
            elif(accion==''):
                print("Error de sintaxis")
                break
        else:
            print("Error de sintaxis")
            esperaba=[]
            esperaba=buscarSeEsperaba(entero,variable,simbolos)
            print("se esperaba: ",esperaba)
            labelError=Label(tabla,text="se esperaba: "+pilaError(esperaba),width=20,font=font1,borderwidth=2,relief="solid")
            labelError.grid(row=contadorFila,column=2)
            label2=Label(tabla,text=" ",width=20,font=font1,borderwidth=2,relief="solid")
            label2.grid(row=contadorFila,column=3)
            break
        contadorFila+=1
                
def pilaError(esperaba):
    cont=0
    k=""
    for i in esperaba:
        k+=str(i)
        if(cont<len(esperaba)-1):
            k+=" o "
        cont+=1
    return str(k)
   
def pilaCadena(pila):
    k=""
    for i in pila:
        k+=str(i)
        k+=" "
    return str(k)
            
def buscarSeEsperaba(estado,variable,simbolos):
    esperaba=[]
    for simbolo in simbolos:
        clave=(estado,simbolo[1])
        if(clave in variable):
            contenido=variable[clave]
            cont=contenido.cget("text")
            if(cont[0]=='d' or cont[0]=='r'):
                esperaba.append(simbolo[0])
    return esperaba       
        
def buscarAccion(variable,estado,posTira):  #esta es una funcion que busca la accion en la tabla de analisis sintactico
    for var in variable:
        clave=(estado,posTira)
        if(var==clave):
            contenido=variable[var]
            cont=contenido.cget("text")
            return cont
    return None 
    
def buscarSimbolo(simbolos,tira): #esta es una funcion que busca el simbolo en la tira de tokens pero asocia el simbolo con el numero de columna
    print("tira:",tira)
    for simbolo in simbolos:
        if(simbolo[0]==tira):
            return simbolo[1]
    return None

def limpiar(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
    direccionArchivo=""
    encabezado(ventana)
    

direccionArchivo2=""
tiraTokens=""

#analizadorSintacticoJava()
    