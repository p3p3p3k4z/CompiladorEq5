from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from logica import *

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
    frameTablaAS=Frame(VentanaPrincipal,width=1510,height=600)
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