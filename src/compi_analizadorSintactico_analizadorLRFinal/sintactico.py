from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from interfazPyS import *
from InterfazCanonica import *
from TablaAnalisisSintactico import *
from analisisSintacticoLR import *
from Analizador_Sintactico import *

def DesplegarAlgoritmoSintactico(opcion):
    arr=["Primeros y siguientes","Colección canónica","Tabla Analisis Sintactico","Análisis Sintáctico LR", "Analizador Sintactico"]
    if opcion==arr[0]:
        interfazPyS()
    elif opcion==arr[1]:
        InterfazCanonica()
    elif opcion == arr[2]:
        InterfazTablaAS()
    elif opcion == arr[3]:
        analisisSintactico()
    elif opcion == arr[4]:
        analizadorSintacticoJava()
        
    else:
        messagebox.showerror("Error","Aún no existe esa opción")
    return

