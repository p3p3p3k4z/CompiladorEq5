import sys
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintacticoLR_primerosYsiguientes'))
sys.path.append(lib_path2)

from primeros_siguientes_YamilJose import CargarGramatica, Primero, Siguientes

# Variables globales para los botones y objetos
cargar_gramatica_obj = None
primero_obj = None
siguiente_obj = None
mostrar_primero_btn = None
mostrar_siguiente_btn = None
limpiar_btn = None
cargar_btn = None

def ventanita_PYS_YJ():    # Configuración de la ventana
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Calculadora de PRIMERO y SIGUIENTE - Equipo #5")
    ventana.geometry("1200x700")

    titulo = ctk.CTkLabel(ventana, text="Calculadora de PRIMERO y SIGUIENTE\nEquipo #5", font=("Helvetica", 18, "bold"))
    titulo.pack(pady=10)

    boton_frame = ctk.CTkFrame(ventana)
    boton_frame.pack(pady=5)

    global cargar_btn, mostrar_primero_btn, mostrar_siguiente_btn, limpiar_btn

    cargar_btn = ctk.CTkButton(boton_frame, text="Elegir Gramática", command=lambda: cargar_gramatica(cargar_btn, mostrar_primero_btn, mostrar_siguiente_btn, limpiar_btn))
    cargar_btn.grid(row=0, column=0, padx=10)

    mostrar_primero_btn = ctk.CTkButton(boton_frame, text="Mostrar PRIMERO", command=lambda: mostrar_primero(mostrar_primero_btn, mostrar_siguiente_btn), state="disabled")
    mostrar_primero_btn.grid(row=0, column=1, padx=10)

    mostrar_siguiente_btn = ctk.CTkButton(boton_frame, text="Mostrar SIGUIENTE", command=lambda: mostrar_siguiente(mostrar_siguiente_btn, limpiar_btn), state="disabled")
    mostrar_siguiente_btn.grid(row=0, column=2, padx=10)

    limpiar_btn = ctk.CTkButton(boton_frame, text="Limpiar Campos", command=limpiar_campos, state="disabled")
    limpiar_btn.grid(row=0, column=3, padx=10)

    output_frame = ctk.CTkFrame(ventana)
    output_frame.pack(pady=15)

    gramatica_text = ctk.CTkTextbox(output_frame, height=400, width=400)
    gramatica_text.grid(row=0, column=0, padx=10)

    primeros_text = ctk.CTkTextbox(output_frame, height=400, width=400)
    primeros_text.grid(row=0, column=1, padx=10)

    siguientes_text = ctk.CTkTextbox(output_frame, height=400, width=400)
    siguientes_text.grid(row=0, column=2, padx=10)

    # Asignar las cajas de texto a las funciones globales para poder modificar su contenido
    global gramatica_text_global, primeros_text_global, siguientes_text_global
    gramatica_text_global = gramatica_text
    primeros_text_global = primeros_text
    siguientes_text_global = siguientes_text

    ventana.mainloop()

# Función para cargar la gramática desde un archivo
def cargar_gramatica(cargar_btn, mostrar_primero_btn, mostrar_siguiente_btn, limpiar_btn):
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
            mostrar_primero_btn.configure(state="normal")
            mostrar_siguiente_btn.configure(state="disabled")
            limpiar_btn.configure(state="disabled")

            with open(archivo_path, 'r') as file:
                gramatica_text_global.delete("0.0", "end")
                gramatica_text_global.insert("0.0", file.read())

            # Deshabilitar el botón Cargar Gramática después de cargar el archivo
            cargar_btn.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la gramática: {str(e)}")


# Función para mostrar el conjunto PRIMERO
def mostrar_primero(mostrar_primero_btn, mostrar_siguiente_btn):
    global siguiente_obj
    resultado_primero = primero_obj.resultados()
    primeros_text_global.delete("0.0", "end")
    primeros_text_global.insert("0.0", resultado_primero)

    siguiente_obj = Siguientes(cargar_gramatica_obj, primero_obj)
    mostrar_primero_btn.configure(state="disabled")
    mostrar_siguiente_btn.configure(state="normal")

# Función para mostrar el conjunto SIGUIENTE
def mostrar_siguiente(mostrar_siguiente_btn, limpiar_btn):
    resultado_siguiente = siguiente_obj.resultados()
    siguientes_text_global.delete("0.0", "end")
    siguientes_text_global.insert("0.0", resultado_siguiente)

    mostrar_siguiente_btn.configure(state="disabled")
    limpiar_btn.configure(state="normal")

# Función para limpiar los campos
def limpiar_campos():
    gramatica_text_global.delete("0.0", "end")
    primeros_text_global.delete("0.0", "end")
    siguientes_text_global.delete("0.0", "end")

    mostrar_primero_btn.configure(state="disabled")
    mostrar_siguiente_btn.configure(state="disabled")
    limpiar_btn.configure(state="disabled")
    cargar_btn.configure(state="normal")  # Habilitar el botón Cargar Gramática al limpiar
