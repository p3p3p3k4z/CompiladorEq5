import customtkinter as ctk  
from tkinter import filedialog, messagebox
import os
import sys

lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintacticoLR_canonica'))
sys.path.append(lib_path2)

from coleccion_canonica import main

def cargar_archivo(ruta_entry):
    # Ruta predefinida para abrir el cuadro de diálogo de archivo
    ruta_inicial = "../../pruebas_sintactico/gramaticas_canonicas"
    
    # Si la ruta inicial no existe, usa la ruta actual
    if not os.path.exists(ruta_inicial):
        ruta_inicial = os.getcwd()
    
    archivo = filedialog.askopenfilename(initialdir=ruta_inicial, filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        ruta_entry.delete(0, ctk.END)
        ruta_entry.insert(0, archivo)

def ejecutar_main(ruta_entry, texto_salida):
    ruta = ruta_entry.get()
    if not ruta:
        messagebox.showerror("Error", "Por favor, selecciona un archivo.")
        return

    try:
        resultados = main(ruta)
        texto_salida.delete("0.0", ctk.END)
        for resultado in resultados:
            texto_salida.insert(ctk.END, str(resultado) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {str(e)}")

def ventana_coleccion():
    # ventana principal
    ctk.set_appearance_mode("Dark")  # Puedes cambiar los colores para futuras entregas
    ctk.set_default_color_theme("green")

    ventana = ctk.CTk()
    ventana.title("Colección Canónica")
    ventana.geometry("800x600")  # Tamaño

    # Widgets
    titulo = ctk.CTkLabel(ventana, text="Generador de Colección Canónica", font=("Arial", 20, "bold"))
    titulo.pack(pady=10)

    # Frame para cargar archivo
    frame_carga = ctk.CTkFrame(ventana)
    frame_carga.pack(pady=10, padx=10, fill="x")

    ruta_label = ctk.CTkLabel(frame_carga, text="Ruta del archivo:", font=("Arial", 14))
    ruta_label.grid(row=0, column=0, padx=10, pady=10)

    ruta_entry = ctk.CTkEntry(frame_carga, width=400)
    ruta_entry.grid(row=0, column=1, padx=10, pady=10)

    btn_cargar = ctk.CTkButton(frame_carga, text="Cargar Archivo", command=lambda: cargar_archivo(ruta_entry))
    btn_cargar.grid(row=0, column=2, padx=10, pady=10)

    # Botón para ejecutar
    btn_ejecutar = ctk.CTkButton(ventana, text="Generar Colección Canónica", command=lambda: ejecutar_main(ruta_entry, texto_salida), width=200)
    btn_ejecutar.pack(pady=10)

    # Cuadro de texto para mostrar resultados
    texto_salida = ctk.CTkTextbox(ventana, width=760, height=400, font=("Arial", 12))
    texto_salida.pack(pady=10, padx=10)

    # Iniciar la aplicación
    ventana.mainloop()

