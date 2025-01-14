#Este archivo solo contiene la parte de la interfaz del programa
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from PrimerosYSiguientes import *

def interfazPyS():
    ventana=Toplevel()
    ventana.grab_set()
    ventana.title("Primeros y siguientes")
    ventana.state("zoomed")
    ventana.config(bg="#363062")
    encabezado(ventana)

def encabezado(ventana):
    font1=("Times New Roman",18)
    gramaticaLabel=Label(ventana,text="Seleccionar gramática",bg="#363062",fg="white",font=font1,width=20)
    gramaticaLabel.place(x=50,y=50)
    gramaticaButton=Button(ventana,text="Cargar",bg="#F99417",width=10,font=font1,command=lambda:cargarGramatica(ventana))
    gramaticaButton.place(x=350,y=50)

    imprimirLabel=Label(ventana,text="Imprimir resultados",bg="#363062",fg="white",width=20,font=font1)
    imprimirLabel.place(x=50,y=150)
    imprimirButton=Button(ventana,text="Imprimir",bg="#F99417",font=font1,width=10,command=lambda:ImprimirResultados(ventana))
    imprimirButton.place(x=350,y=150)

    limpiarButton=Button(ventana,text="Limpiar",bg="#F99417",font=font1,width=10,command=lambda:limpiar(ventana))
    limpiarButton.place(x=600,y=150)

def cargarGramatica(ventana):
    global direccionArchivo
    direccionArchivo=cargarDireccion()
    frameGramatica=Frame(ventana,width=400,height=500)
    frameGramatica.place(x=50,y=300)
    listaReglas=Listbox(frameGramatica,width=50,height=30,font=("Times New Roman",16))
    listaReglas.place(x=0,y=0)
    try:
        archivoGramatica=open(direccionArchivo,encoding="utf-8")
        linea="hola"
        listaReglas.insert(END,"Gramática")
        listaReglas.insert(END,"")
        while linea!="":
            linea=archivoGramatica.readline()
            listaReglas.insert(END,linea)
    except:
        messagebox.showerror("Error","No se ha cargado una gramática")

def ImprimirResultados(ventana):
    try:
        datos=mainPyS(direccionArchivo)
        #print(datos)
        framePrimeros=Frame(ventana,width=400,height=200)
        framePrimeros.place(x=600,y=300)
        frameSiguientes=Frame(ventana,width=400,height=200)
        frameSiguientes.place(x=600,y=600)
        listaPrimeros=Listbox(framePrimeros,width=50,height=30,font=("Times New Roman",16))
        listaPrimeros.place(x=0,y=0)

        listaSiguientes=Listbox(frameSiguientes,width=50,height=30,font=("Times New Roman",16))
        listaSiguientes.place(x=0,y=0)

        listaPrimeros.insert(END,"Primeros")
        listaPrimeros.insert(END,"")
        listaSiguientes.insert(END,"Siguientes")
        listaSiguientes.insert(END,"")
        for i in datos:
            listaPrimeros.insert(END,i[0]+"=    "+str(listaCadena(i[1])))
            listaSiguientes.insert(END,i[0]+"=    "+str(listaCadena(i[2])))
    except:
        messagebox.showerror("Error","No se ha cargado una gramática")
def limpiar(ventana):
    global direccionArchivo

    for widget in ventana.winfo_children():
        widget.destroy()
    direccionArchivo=""
    encabezado(ventana)



direccionArchivo=""