import os
import sys
from customtkinter import *
from tkinter import messagebox

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
from ventana_prisig import *

# Configuración global de customtkinter
set_appearance_mode("dark")  # Opciones: "dark" o "light"
set_default_color_theme("blue")  # Tema de colores

def ventanaPrincipal():
    global raiz
    raiz = CTk()
    raiz.geometry("800x500")
    raiz.title("Equipo5")

    # Crear el marco izquierdo para los botones
    menu_frame = CTkFrame(raiz, corner_radius=10, width=300)
    menu_frame.pack(side="left", fill="y", padx=10, pady=10)

    CTkLabel(menu_frame, text="Menú Principal", font=("Times New Roman", 18, "bold")).pack(pady=20)

    # Botón para abrir el análisis léxico
    btn_lexico = CTkButton(
        menu_frame, 
        text="Análisis Léxico", 
        command=lambda: abrirMenuLexico(), 
        corner_radius=10, 
        font=("Times New Roman", 14),
        height=50,
        width=250
    )
    btn_lexico.pack(pady=15)

    # Botón para abrir el análisis sintáctico
    btn_sintactico = CTkButton(
        menu_frame, 
        text="Análisis Sintáctico", 
        command=lambda: abrirMenuSintactico(), 
        corner_radius=10, 
        font=("Times New Roman", 14),
        height=50,
        width=250
    )
    btn_sintactico.pack(pady=15)

    # Botón deshabilitado para análisis semántico
    btn_semantico = CTkButton(
        menu_frame, 
        text="Análisis Semántico (Deshabilitado)", 
        state="disabled", 
        corner_radius=10, 
        font=("Times New Roman", 14),
        height=50,
        width=250
    )
    btn_semantico.pack(pady=15)

    # Marco para el contenido principal
    content_frame = CTkFrame(raiz, corner_radius=10)
    content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    CTkLabel(content_frame, text="COMPILADORES", font=("Times New Roman", 24, "bold")).pack(pady=10)

    integrantes = """
Equipo 5:

- Mario Enrique Gallardo
- Christian Josue Campos Lopez
- Yamil
- Ariadna Betsabe Espina Ramirez
- Jose Perez
- Irving Tristan Perez Zurita
    """
    CTkLabel(content_frame, text=integrantes, font=("Times New Roman", 16), justify="left").pack(pady=10)

    raiz.mainloop()

def abrirMenuLexico():
    # Crear ventana de análisis léxico
    menu_lexico = CTkToplevel(raiz)
    menu_lexico.geometry("400x300")
    menu_lexico.title("Opciones de Análisis Léxico")

    CTkLabel(menu_lexico, text="Análisis Léxico", font=("Times New Roman", 16, "bold")).pack(pady=10)

    CTkButton(
        menu_lexico, 
        text="Algoritmo de Thomson (AFND)", 
        command=lambda: Conjuntos(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

    CTkButton(
        menu_lexico, 
        text="Construcción de conjuntos (AFD)", 
        command=lambda: Conjuntos_afn(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

    CTkButton(
        menu_lexico, 
        text="Analizador Léxico", 
        command=lambda: Prueba(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

def abrirMenuSintactico():
    # Crear ventana de análisis sintáctico
    menu_sintactico = CTkToplevel(raiz)
    menu_sintactico.geometry("400x300")
    menu_sintactico.title("Opciones de Análisis Sintáctico")

    CTkLabel(menu_sintactico, text="Análisis Sintáctico", font=("Times New Roman", 16, "bold")).pack(pady=10)

    CTkButton(
        menu_sintactico, 
        text="Primeros y Siguientes", 
        command=lambda: ventanita(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

    CTkButton(
        menu_sintactico, 
        text="Otra opción", 
        command=lambda: bucle(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)
