from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from lexico import *
from Analizador_Lexico import *
from TablaAnalisisSintacticoRef import *
from PrimerosYSiguientes import mainPyS

import os
import sys

base_path = os.path.abspath(os.path.dirname(__file__))
gramatica_path = os.path.join(base_path, '..', '..', 'pruebas_sintactico/programitas_java', 'entradaLR.txt')

def analizadorSintacticoJava():
    VentanaPrincipal =Toplevel()
    VentanaPrincipal.title("Analizador sintáctico")
    try:
        VentanaPrincipal.state("zoomed")
    except:
        VentanaPrincipal.attributes('-zoomed', True) 
    VentanaPrincipal.config(background="#181818")
    encabezado(VentanaPrincipal)
    VentanaPrincipal.mainloop()

def encabezado(VentanaPrincipal):
    font1=("Times New Roman",14)
    font2=("Times New Roman",20)
    
    archivoLabel=Label(
        VentanaPrincipal,
        text="Seleccionar programa fuente:",
        font=font1,
        width=20,
        background="#282828",
        foreground="#FFFFFF")
    archivoLabel.place(x=60,y=30)
    
    archivoRutaTexto = Text(
        VentanaPrincipal,
        height=1,  # Altura del recuadro en líneas
        width=90,  # Ancho del recuadro en caracteres
        font=font1,
        background="#282828",
        foreground="#FFFFFF",
        state="disabled",  # Inicialmente deshabilitado
        wrap=NONE  # Evita que el texto haga saltos de línea automáticos
    )
    archivoRutaTexto.place(x=530, y=25)
    
    archivoButton=Button(
         VentanaPrincipal,text="Abrir",
        foreground="#FFFFFF",
        width=20,
        bg="#007ACC",
        font=font1,
        command=lambda:abrirArchivo1(VentanaPrincipal, archivoRutaTexto),
        )
    
    archivoButton.place(x=300,y=20)
    tokenButton=Button(
       VentanaPrincipal,
        text="Cargar Gramatica",
        foreground="#FFFFFF",
        width=20,
        command=lambda:abrirArchivo(VentanaPrincipal),
        bg="#007ACC",
        font=font1,
        
        )

    
    tokenButton.place(x=300,y=100)
    ImprimirResultad0s=Button(
        VentanaPrincipal,text="Analizar",
        foreground="#FFFFFF",width=20,bg="#007ACC",
        font=font1,
        command=lambda:imprimirResultados(VentanaPrincipal),
        
        )
    ImprimirResultad0s.place(x=550,y=100)
    limpiarButton=Button(
        VentanaPrincipal,text="Limpiar",
        foreground="#FFFFFF",width=20,bg="#007ACC",
        font=font1,command=lambda:limpiar(VentanaPrincipal),
        )
    limpiarButton.place(x=800,y=100)

def cargarGramatica(Ventana,direccionArchivo):
    global Gramatica
    frameGramatica=Frame(Ventana,width=300,height=600,bg="#1E1E1E")
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
        mostrarRegla=Label(frameGramatica,text=str(linea),
                           font=("Times New Roman",14),
                            width=20, 
                            bg="#252526",  # Fondo oscuro
                            fg="#D4D4D4",  # Texto gris claro
                            )
        mostrarRegla.grid(row=contador,column=0)
        contador+=1

def abrirArchivo(Ventana):
    global direccionArchivo2
    Ventana.grab_set()
    username=getpass.getuser()
    ruta_proyecto = r"C:\Users\{username}\Documents\CompiladorEq5"
    direccionArchivo2= "programitas_java/entradaLR.txt"
    cargarGramatica(Ventana,direccionArchivo2)

def abrirArchivo1(Ventana, archivoRutaTexto): 
    global tiraTokens
    Ventana.grab_set()
    
    # Definir la ruta inicial del proyecto (asegúrate de que 'gramatica_path' esté definida)
    ruta_proyecto = gramatica_path  
    direccionArchivo = filedialog.askopenfilename(
        initialdir=ruta_proyecto,
        title="Abrir Archivo",
        filetypes=(("Archivos Java", "*.java"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    
    if direccionArchivo:
        # Mostrar solo la ruta del archivo en el cuadro de texto
        archivoRutaTexto.config(state="normal")  # Habilitar edición temporalmente
        archivoRutaTexto.delete(1.0, END)  # Limpiar cualquier texto previo
        archivoRutaTexto.insert(END, direccionArchivo)  # Insertar la ruta del archivo seleccionado
        archivoRutaTexto.config(state="disabled")  # Volver a deshabilitar

        # Procesar el archivo seleccionado
        tiraTokens = ObtenerTiraTokensExterna(direccionArchivo)

        # Sustituir operadores y símbolos compuestos por dos caracteres
        reemplazos = {
            "<": "menorque", ">": "mayorque", "==": "igualigual",
            ">=": "mayorigual", "<=": "menorigual", "!=": "diferente",
            "&&": "and", "||": "or", "++": "masmas", "--": "menosmenos",
            "+=": "masigual", "-=": "menosigual", "*=": "porigual",
            "/=": "entredosigual", "%=": "modigual", "-": "resta",
            "String": "string"
        }

        for key, value in reemplazos.items():
            tiraTokens = tiraTokens.replace(key, value)

        # Opcional: Puedes imprimir la tira de tokens para depuración
        print("Tira de tokens procesada:", tiraTokens)

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
    frameResultados=Frame(ventanaResultados,width=600,height=600)
    frameResultados.place(x=60,y=100)
    ventana2=Toplevel()
    frame2=Frame(ventana2,width=300,height=600)
    
    #Esto es lo que hay que arreglar
    datos,reglas=ImprimirResultados2(ventana2,frame2,direccionArchivo2)
    ventana2.destroy()
    setDireccionArchivo(direccionArchivo2,reglas)
    variable,simbolos,estados=ImprimirTablaASZ(ventanaResultados,frameResultados)#variable es un diccionario con clave el numero de estado y la columna y contenido un label con el contenido de la tabla
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
    tabla.config(background="#F6C794")
    canvas=Canvas(Ventana,width=1100,height=900)
    canvas.place(x=300,y=150)

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
    canvas.bind_all("<KeyPress-Left>", on_arrow_key)
    canvas.bind_all("<KeyPress-Right>", on_arrow_key)
    canvas.bind_all("<KeyPress-Up>", on_arrow_key_v)
    canvas.bind_all("<KeyPress-Down>", on_arrow_key_v)
    contadorFila=0
    pila=[]
    accion=[]
    pila.append(0)
    font1=("Times New Roman",14)
    labelTextPila=Label(tabla,text="Pila",background="#3CB35A",width=40,font=font1,borderwidth=2,relief="solid")
    labelTextPila.grid(row=contadorFila,column=0)
    labelTextTira=Label(tabla,text="Entrada",width=60,background="#3CB35A",font=font1,borderwidth=2,relief="solid")
    labelTextTira.grid(row=contadorFila,column=1)
    labelTextSalida=Label(tabla,text="Salida",width=40,background="#3CB35A",font=font1,borderwidth=2,relief="solid")
    labelTextSalida.grid(row=contadorFila,column=2,columnspan=2)
    contadorFila+=1
    while((len(tira)>0) & (accion!='Aceptacion') & (accion!='')):
        a=tira[0]
        sacarTira=tira[0]
        labelPila=Label(tabla,text=pilaCadena(pila),width=40,font=font1,borderwidth=2,relief="solid")
        labelPila.grid(row=contadorFila,column=0) 
        labelTira=Label(tabla,text=pilaCadena(tira),width=60,font=font1,borderwidth=2,relief="solid")
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
                estadoAgregar=int(accion[1:])
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
                estadoAgregar=int(accion)
                pila.append(estadoAgregar)
                print("contenido de la pila:",pila)
                print("tira de tokens despues del desplazamiento:",tira)
            elif(accion[0]=='r'):  #reducir A→β
                print("es una reduccion")
                pos=int(accion[1:])
                regla=arreGramatica[pos-1]
                labelSalida=Label(tabla,text=pilaCadena(accion),width=20,font=font1,borderwidth=2,relief="solid")
                labelSalida.grid(row=contadorFila,column=2)
                #imprimir la producción A→β
                print("Regla:",regla)
                labelRegla=Label(tabla,text=str(regla[0])+"->"+str(regla[1]),width=20,font=font1,borderwidth=2,relief="solid")
                labelRegla.grid(row=contadorFila,column=3)
                tama=len(regla[1].split(' ')) #calculamos el tamaño de β
                reglasinL=regla[1].split(' ')
                if(reglasinL[0]=='λ'):
                    tama=0
                else:
                    tama=tama*2 
                print("tamaño de beta:",tama)
                print("ctm")
                for k in range(0,tama):
                    pila.pop()  #pop 2*|β| símbolos
                print("contenido de la pila despues de eliminar:",pila)
                pila.append(regla[0])   #push A
                print("contenido de la pila despues de agregar A:",pila)
                simbIra=buscarSimbolo(simbolos,pila[len(pila)-1])
                #s=Ir_a[j,A]
                es=int(pila[len(pila)-2])+2
                print(es)
                s=buscarAccion(variable,es,simbIra)
                #push s
                print(s)
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
tiraTokens=gramatica_path
#analizadorSintacticoJava()