#ESTE ARCHIVO ES PARA LA INTERFAZ DEL CODIGO QUE HIZO CRISTIAN AUN SIGUE CON ERRORES
import sys
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Agregar el directorio con la implementación de Primeros y Siguientes al path
lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintacticoLR_primerosYsiguientes'))
sys.path.append(lib_path2)

from Primeros_Siguientes import *

# Variables globales para gestionar los datos y botones
cargar_gramatica_obj = None
primero_obj = None
siguiente_obj = None
gramatica_text_global = None
primeros_text_global = None
siguientes_text_global = None

def VentanaPYS():
    # Configuración inicial de la ventana
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Calculadora de PRIMERO y SIGUIENTE - Equipo #5")
    ventana.geometry("1200x700")

    # Título principal
    titulo = ctk.CTkLabel(ventana, text="Calculadora de PRIMERO y SIGUIENTE\nEquipo #5", font=("Helvetica", 18, "bold"))
    titulo.pack(pady=10)

    # Marco para botones
    boton_frame = ctk.CTkFrame(ventana)
    boton_frame.pack(pady=5)

    global cargar_btn, mostrar_primero_btn, mostrar_siguiente_btn, limpiar_btn

    # Botón para cargar gramática
    cargar_btn = ctk.CTkButton(boton_frame, text="Elegir Gramática", command=cargar_gramatica)
    cargar_btn.grid(row=0, column=0, padx=10)

    # Botones para mostrar resultados y limpiar
    mostrar_primero_btn = ctk.CTkButton(boton_frame, text="Mostrar PRIMERO", command=mostrar_primero, state="disabled")
    mostrar_primero_btn.grid(row=0, column=1, padx=10)

    mostrar_siguiente_btn = ctk.CTkButton(boton_frame, text="Mostrar SIGUIENTE", command=mostrar_siguiente, state="disabled")
    mostrar_siguiente_btn.grid(row=0, column=2, padx=10)

    limpiar_btn = ctk.CTkButton(boton_frame, text="Limpiar Campos", command=limpiar_campos, state="disabled")
    limpiar_btn.grid(row=0, column=3, padx=10)

    # Marco para los cuadros de texto
    output_frame = ctk.CTkFrame(ventana)
    output_frame.pack(pady=15)

    global gramatica_text_global, primeros_text_global, siguientes_text_global

    # Textbox para mostrar la gramática
    gramatica_text_global = ctk.CTkTextbox(output_frame, height=400, width=400)
    gramatica_text_global.grid(row=0, column=0, padx=10)

    # Textbox para mostrar conjuntos PRIMERO
    primeros_text_global = ctk.CTkTextbox(output_frame, height=400, width=400)
    primeros_text_global.grid(row=0, column=1, padx=10)

    # Textbox para mostrar conjuntos SIGUIENTE
    siguientes_text_global = ctk.CTkTextbox(output_frame, height=400, width=400)
    siguientes_text_global.grid(row=0, column=2, padx=10)

    ventana.mainloop()

# Función para cargar gramática desde archivo
def cargar_gramatica():
    archivo_path = filedialog.askopenfilename(
        initialdir=os.path.abspath("../../Gramaticas"),
        filetypes=[("Text Files", "*.txt")],
        title="Seleccionar archivo de gramática"
    )
    if archivo_path:
        try:
            global cargar_gramatica_obj, primero_obj
            cargar_gramatica_obj = CargarGramatica(archivo_path)
            primero_obj = Primero(cargar_gramatica_obj)

            # Mostrar la gramática en el Textbox
            with open(archivo_path, 'r') as file:
                gramatica_text_global.delete("0.0", "end")
                gramatica_text_global.insert("0.0", file.read())

            # Habilitar botones
            mostrar_primero_btn.configure(state="normal")
            limpiar_btn.configure(state="normal")
            cargar_btn.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la gramática: {str(e)}")

# Función para calcular y mostrar el conjunto PRIMERO
def mostrar_primero():
    global siguiente_obj
    resultado_primero = primero_obj.resultados()
    primeros_text_global.delete("0.0", "end")
    primeros_text_global.insert("0.0", resultado_primero)

    # Preparar para calcular SIGUIENTE
    siguiente_obj = Siguientes(cargar_gramatica_obj, primero_obj)
    mostrar_primero_btn.configure(state="disabled")
    mostrar_siguiente_btn.configure(state="normal")

# Función para calcular y mostrar el conjunto SIGUIENTE
def mostrar_siguiente():
    resultado_siguiente = siguiente_obj.resultados()
    siguientes_text_global.delete("0.0", "end")
    siguientes_text_global.insert("0.0", resultado_siguiente)

    mostrar_siguiente_btn.configure(state="disabled")

# Función para limpiar los cuadros de texto
def limpiar_campos():
    gramatica_text_global.delete("0.0", "end")
    primeros_text_global.delete("0.0", "end")
    siguientes_text_global.delete("0.0", "end")

    # Restaurar el estado de los botones
    cargar_btn.configure(state="normal")
    mostrar_primero_btn.configure(state="disabled")
    mostrar_siguiente_btn.configure(state="disabled")
    limpiar_btn.configure(state="disabled")