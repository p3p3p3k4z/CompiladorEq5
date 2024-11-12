import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# Asegúrate de que las rutas de las librerías sean correctas
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Presentacion_Alexico'))
sys.path.append(lib_path)
lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Presentacion_sintactico'))
sys.path.append(lib_path2)


# Aquí van tus imports personalizados
from ventana_extra import MenuVentana
from VentanaConjuntos import *
from VentanaThompson import *
from ventana_sint_aux import *

def abrir():
    fichero = filedialog.askopenfilename(title="Abrir", initialdir="D:", filetypes=(("ficheros de texto", "*.txt"), ("ficheros de python", "*.py")))
    if fichero:
        print(f"Archivo seleccionado: {fichero}")
        # Aquí puedes agregar la lógica para procesar el archivo

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

def ventanaPrincipal():
    global raiz
    raiz = Tk()
    raiz.config(background="dark turquoise")
    raiz.geometry("800x500") 
    raiz.title("Equipo5")

    # Cargar la imagen de fondo
    try:
        background_image = PhotoImage(file="../../imagenes/portada.png")
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

    opc2 = Menu(menuop, tearoff=0)
    opc2.add_command(label="Calcular", command=lambda: Conjuntos_afn(), font=font1)

    opc3 = Menu(menuop, tearoff=0, font=font1)
    opc3.add_command(label="Analizador Lexico", command=lambda: Prueba(), font=font1)

    menuop.add_cascade(label="Análisis léxico", menu=opc)
    menuop.add_cascade(label="Análisis sintáctico", menu=opc3)
    menuop.add_cascade(label="Análisis semántico", menu=opc2, state="disabled")
    

    raiz.mainloop()

def abrirVentanaSecundaria():
    # Ocultar la ventana principal antes de abrir la secundaria
    raiz.withdraw()
    ventanaSecundaria()