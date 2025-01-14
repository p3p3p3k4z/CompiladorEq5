from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import getpass
from tkinter import ttk 
from coleccionCanonica import *



def InterfazCanonica():
    font1=("Times New Roman",14)
    VentanaPrincipal =Toplevel()
    VentanaPrincipal.title("Algoritmo de la colección canónica")
    VentanaPrincipal.state("zoomed")
    VentanaPrincipal.config(background="#363062")
    font2=("Times New Roman",20)
    archivoLabel=Label(VentanaPrincipal,text="Seleccionar Archivo:",font=font1,width=20,background="#363062",foreground="white")
    archivoLabel.place(x=60,y=30)
    frameGramatica=Frame(VentanaPrincipal,width=400,height=600)
    frameGramatica.place(x=20,y=100)
    framePrimeros=Frame(VentanaPrincipal,width=1010,height=600)
    framePrimeros.place(x=450,y=100)
    archivoButton=Button(VentanaPrincipal,text="Abrir archivo",width=20,command=lambda:abrirArchivo(VentanaPrincipal,frameGramatica),bg="#F99417",font=font1)
    archivoButton.place(x=300,y=20)
    ImprimirResultad0s=Button(VentanaPrincipal,text="Imprimir Resultados",width=20,bg="#F99417",font=font1,command=lambda:ImprimirCanonicos(VentanaPrincipal,framePrimeros))
    ImprimirResultad0s.place(x=300,y=60)
    limpiarButton=Button(VentanaPrincipal,text="Limpiar",width=20,bg="#F99417",font=font1,command=lambda:limpiar(framePrimeros,frameGramatica))
    limpiarButton.place(x=700,y=60)

    

def abrirArchivo(Ventana,frameGramatica):
    global direccionArchivo
    fuente=("Times New Roman",15)
    Ventana.grab_set()
    username=getpass.getuser()
    ruta_proyecto = r"C:\Users\{username}\Documents\ProyectoCompiladores"
    direccionArchivo=filedialog.askopenfilename(initialdir=ruta_proyecto,title="Abrir Archivo",filetypes=(("texto","*.txt"),))
    listaGramatica=Listbox(frameGramatica)
    listaGramatica.pack()
    archivoGramatica=open(direccionArchivo,encoding="utf-8")

    simboloInicial=archivoGramatica.readline().split()
    #print(simboloInicial)
    Inicial=simboloInicial[0]
    listaGramatica.insert(END,"-----Gramática extendida-----")
    listaGramatica.insert(END,Inicial+"'"+"->"+Inicial+"$")
    listaGramatica.config(font=fuente ,width=30,height=26  )
    archivoGramatica.readline()#leer los terminales
    texto="hola"
    while texto!="":
        texto=archivoGramatica.readline()
        listaGramatica.insert(END,texto)
    
    archivoGramatica.close()
    Ventana.grab_release()


def ImprimirCanonicos(Ventana,Frame):
    global ruta
    global direccionArchivo
    Ventana.grab_set()
    if direccionArchivo!="": 
        ruta=direccionArchivo
        #print("ruta==",ruta)
   
        fuente=("Times New Roman",12)
        listaCanonicos=Listbox(Frame)
        listaCanonicos.config(width=120,height=30,font=fuente)
        listaCanonicos.pack()
        listaCanonicos.insert(END,"----Colección canónica----")
        ResultadosCanonica=main(ruta)
        flag=0
        #print("tipo de resultado",type(ResultadosCanonica[0]))
        for elemento in ResultadosCanonica:#elemento es un objeto de la clase tablaColeccionCanonica
            #print(elemento)
            if flag==0:
                listaCanonicos.insert(END,"Cerradura= "+str(elemento.getEnviadoACerradura()))
                listaCanonicos.insert(END,"Estado="+str(elemento.getEstado()))    
                listaCanonicos.insert(END,"    ")
                flag=1
            else:
                if elemento.getSimboloIr_A()=="-":
                    continue
                else:
                    listaCanonicos.insert(END,"ir a("+str(elemento.getEstadoIr_A())+","+str(elemento.getSimboloIr_A())+")=Cerradura"+str(elemento.getEnviadoACerradura()))

                    if len(elemento.getEstado())==0:
                        listaCanonicos.insert(END,"Aceptación")
                    else:
                        listaCanonicos.insert(END,"Estado="+str(elemento.getEstado()))
                listaCanonicos.insert(END,"    ")

            
            #listaCanonicos.insert(END,elemento)
            

    else:
        messagebox.showerror("Error","Selecciona un archivo antes")
    Ventana.grab_release()
def limpiar(framePrimeros,frameGramatica):
    global ruta
    for widget in framePrimeros.winfo_children():
        widget.destroy()
    for widget in frameGramatica.winfo_children():
        widget.destroy()
    
    ruta=""

ruta=""
direccionArchivo=""
