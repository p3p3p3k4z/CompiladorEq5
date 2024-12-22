import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_presentacion_alexico'))
sys.path.append(lib_path)
lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_presentacion_sintactico'))
sys.path.append(lib_path2)
lib_path3 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Coleccion_canonica'))
sys.path.append(lib_path3)
lib_path4 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintacticoLR_TablaLR'))
sys.path.append(lib_path4)
lib_path5 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintactico_analizadorLR'))
sys.path.append(lib_path5)

base_path = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(base_path, '..', '..', 'imagenes', 'portada.png')

from VentanaThompson import Conjuntos
from VentanaConjuntos import Conjuntos_afn
from VentanaAnalizadorLexico import VentanaAlexico #corregir los errores dados en el github
from VentanaPrimerosSiguientes import ventanaPYS_Aux 
#from VentanaPYS_YamilJose import *
from VentanaCanonica import ventana_coleccion
#from Interfaz import *
from Tabla_Analizador_Sintacticov2 import InterfazTablaAS
from analisisSintacticoLR import analisisSintactico

#no implementado
def abrir():
    fichero = filedialog.askopenfilename(title="Abrir", initialdir="D:", filetypes=(("ficheros de texto", "*.txt"), ("ficheros de python", "*.py")))
    if fichero:
        print(f"Archivo seleccionado: {fichero}")

def mensaje():
    valor = messagebox.askquestion("AFND", "Estamos trabajando, desea salir!?")
    if valor == "yes":
        raiz.destroy()

def bucle():
    valor = messagebox.askretrycancel("Pendiente", "Aún no está listo")
    while valor == True:
        valor = messagebox.askretrycancel("Pendiente", "Que aún no está listo, dije")

def ventanaSecundaria():
    # Crear una nueva ventana (secundaria)
    ventana = Toplevel(raiz)
    ventana.geometry("400x300")
    ventana.title("Ventana Secundaria")

    # Cuando se cierre esta ventana, la ventana principal aparecerá de nuevo
    ventana.protocol("WM_DELETE_WINDOW", lambda: mostrarVentanaPrincipal())

def mostrarVentanaPrincipal():
    # Mostrar la ventana principal después de cerrar la secundaria
    raiz.deiconify()

def ventanaPrincipal_Aux():
    global raiz
    raiz = Tk()
    raiz.config(background="dark turquoise")
    raiz.geometry("800x500") 
    raiz.title("Equipo5")

    # Cargar la imagen de fondo
    try:
        background_image = PhotoImage(file=image_path)
    except TclError:
        print("Error al cargar la imagen")
        background_image = None  # O alguna imagen por defecto

    if background_image:
        # Crear un Canvas para poner la imagen de fondo
        canvas = Canvas(raiz, width=1500, height=700)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Menú
    menuop = Menu(raiz)
    raiz.config(menu=menuop)
    font1 = ("Times New Roman", 10)

    opc = Menu(menuop, tearoff=0)
    opc.add_command(label="Algoritmo de Thomson(AFND)", command=lambda: Conjuntos(), font=font1)
    opc.add_command(label="Construcción de conjuntos(AFD)", command=lambda: Conjuntos_afn(), font=font1)
    opc.add_command(label="Analizador Lexico", command=lambda: VentanaAlexico(), font=font1)
    
    opc2 = Menu(menuop, tearoff=0)
    opc2.add_command(label="Explorador de Archivos", command=lambda: abrir(), font=font1)

    opc3 = Menu(menuop, tearoff=0, font=font1)  
    opc3.add_command(label="Primeros y Siguientes", command=lambda: ventanaPYS_Aux(), font=font1)
    opc3.add_command(label="Coleccion Canonica", command=lambda: ventana_coleccion(), font=font1)
    opc3.add_command(label="Tabla de analisis sintactico LR", command=lambda: InterfazTablaAS(), font=font1)
    opc3.add_command(label="Analisis Sintactico LR", command=lambda: analisisSintactico(), font=font1)
    
    menuop.add_cascade(label="Abrir", menu=opc2)
    menuop.add_cascade(label="Análisis léxico", menu=opc)
    menuop.add_cascade(label="Análisis sintáctico", menu=opc3)
    menuop.add_cascade(label="Análisis semántico", menu=opc2, state="disabled")
    

    raiz.mainloop()

def abrirVentanaSecundaria():
    # Ocultar la ventana principal antes de abrir la secundaria
    raiz.withdraw()
    ventanaSecundaria()
