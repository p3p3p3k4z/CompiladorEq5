import re
from tkinter import *
from tkinter import filedialog
import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorLexico_alexico'))
sys.path.append(lib_path)

from lexico import *

def abrirArchivo(alphaEntry, erEntry, lexWindow, output_text, error_text, symbol_text):
    lexWindow.grab_set()
    alphaEntry.delete(0, END)
    erEntry.delete(0, END)
    output_text.delete(1.0, END)
    error_text.delete(1.0, END)
    symbol_text.delete(1.0, END)
    
    direccionArchivo = filedialog.askopenfilename(
        initialdir=r"../../codigos_fuentes",
        title="Abrir",
        filetypes=(("texto", "*.txt"),)
    )
    
    try:
        with open(direccionArchivo, 'r') as archivo:
            code = archivo.read()
            erEntry.insert(END, code)
           
            # Ejecutar el análisis léxico en el contenido del archivo 
            tokens, errores, variables = analizador_lex(code)
            
            # Encabezado para la salida del análisis léxico
            output_text.insert(END, f"{'# Línea':<10}{'Lexema':<20}{'-->':<5}{'Token':<10}\n")
            output_text.insert(END, "-" * 50 + "\n")
            
            for token in tokens:
                output_text.insert(END, f"# Línea {token[0]:<3}  {token[1]:<15} -->  {token[2]:<10}\n")
           
            # Encabezado para la salida de errores 
            error_text.insert(END, "# Línea       Descripción\n")
            error_text.insert(END, "-" * 40 + "\n")
            
            for error_linea, error_texto in errores:
                error_text.insert(END, f"# Línea {error_linea:<3}   Error: {error_texto}\n")
    
            # Mostrar variables y sus valores con ID numerado
            symbol_text.insert(END, "#Id        Valor:\n")
            symbol_text.insert(END, "-" * 40 + "\n")
            for idx, (var_name, var_value) in enumerate(variables.items(), start=1):
                symbol_text.insert(END, f"{idx:<10}{var_name}={var_value}\n")

    except Exception as e:
        output_text.insert(END, f"Error al abrir el archivo: {e}\n")

def VentanaAlexico():
    # Define la fuente principal para la interfaz
    font1 = ("Cicle", 12)
    
    # Crea la ventana secundaria para la interfaz del autómata
    lexWindow = Toplevel()
    
    # Intenta maximizar la ventana; si falla, ajusta manualmente el tamaño al de la pantalla
    try:
        lexWindow.attributes("-zoomed", True)
    except:
        lexWindow.geometry(f"{lexWindow.winfo_screenwidth()}x{lexWindow.winfo_screenheight()}+0+0")
    
    # Configura el título y el fondo de la ventana
    lexWindow.title("Analizador Lexico")
    lexWindow.config(bg="#1C1F26")  # Fondo color Dark Sea

    # Etiqueta para indicar al usuario que debe ingresar una expresión
    archivoL = Label(lexWindow, text="Ingresa una expresión", width=40, bg="#6F8087", font=font1, fg="white")
    archivoL.place(x=450, y=50)

    # Botón "Inspeccionar" para seleccionar el archivo
    archivoButton = Button(lexWindow, text="Inspeccionar", width=26, 
                           command=lambda: (abrirArchivo(alphaEntry, erEntry, lexWindow, output_text, error_text, symbol_text)), 
                           bg="#630606", fg="white", font=font1)
    archivoButton.place(x=1060, y=47)
    #archivoButton.config(bd=10, relief="raised")

    # Etiqueta para la entrada de expresión regular
    eregularL = Label(lexWindow, text="Expresión regular:", font=font1, width=36, bg="#6F8087", fg="white")
    eregularL.place(x=470, y=100)

    # Campo de entrada para la expresión regular
    erEntry = Entry(lexWindow, width=30, font=font1, bg="#E6E6FA", fg="black")
    erEntry.place(x=1050, y=101)

    # Etiqueta para la entrada de alfabeto
    alphaLabel = Label(lexWindow, text="Alfabeto", font=font1, width=30, bg="#6F8087", fg="white")
#     alphaLabel.place(x=490, y=150)

    # Campo de entrada para el alfabeto
    alphaEntry = Entry(lexWindow, font=font1, width=30, bg="#E6E6FA")
#     alphaEntry.place(x=1050, y=151)

    # Calcula posiciones para centrar las tablas en la pantalla (izquierda, centro, derecha)
    screen_width = lexWindow.winfo_screenwidth()
    table_width = 400  # Ancho aproximado de cada tabla de texto

    # Calcula posiciones centradas para cada tabla
    left_x = (screen_width // 4) - (table_width // 2) - 200
    center_x = (screen_width // 2) - (table_width // 2)
    right_x = (3 * screen_width // 4) - (table_width // 2) +100

    # Área de texto para mostrar los resultados del análisis léxico (izquierda)
    output_text = Text(lexWindow, wrap=WORD, width=60, height=25, bg="#448581", font=("Consolas", 10))
    output_text.place(x=left_x, y=320)
    output_text.insert(END, "Resultados del análisis léxico:\n")

    # Scrollbar para el área de texto de resultados
    scrollbar_output = Scrollbar(lexWindow, command=output_text.yview)
    scrollbar_output.place(x=left_x + 485, y=350, height=245)
    output_text.config(yscrollcommand=scrollbar_output.set)

    # Área de texto para mostrar errores (centro)
    error_text = Text(lexWindow, wrap=WORD, width=40, height=25, bg="#B33030", font=("Consolas", 10))
    error_text.place(x=center_x, y=320)
    error_text.insert(END, "Errores:\n")

    # Scrollbar para el área de texto de errores
    scrollbar_error = Scrollbar(lexWindow, command=error_text.yview)
    scrollbar_error.place(x=center_x + 320, y=350, height=245)
    error_text.config(yscrollcommand=scrollbar_error.set)

    # Área de texto para mostrar la tabla de símbolos (derecha)
    symbol_text = Text(lexWindow, wrap=WORD, width=40, height=25, bg="#31707F", font=("Consolas", 10))
    symbol_text.place(x=right_x, y=320)
    symbol_text.insert(END, "Tabla de símbolos:\n")

    # Scrollbar para el área de texto de tabla de símbolos
    scrollbar_symbol = Scrollbar(lexWindow, command=symbol_text.yview)
    scrollbar_symbol.place(x=right_x + 320, y=340, height=245)
    symbol_text.config(yscrollcommand=scrollbar_symbol.set)