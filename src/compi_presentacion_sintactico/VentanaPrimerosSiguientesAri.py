import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import customtkinter as ctk 

lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintacticoLR_primerosYsiguientes'))
sys.path.append(lib_path2)

from Primeros_Siguientes import *

direccionArchivo = ""
treeview = None
textArea = None
btnCalcular = None
btnLimpiar = None

# Función para mostrar resultados en la tabla
def mostrarResultados(datos):
    global treeview
    # Limpiar la tabla
    for item in treeview.get_children():
        treeview.delete(item)

    # Insertar los datos en la tabla
    for item in datos:
        noTerminal = item[0]
        primeros = ' '.join(item[1])
        siguientes = ' '.join(item[2])
        treeview.insert("", "end", values=(noTerminal, primeros, siguientes))

# Función para cargar y obtener la dirección del archivo
def obtenerDireccion():
    global direccionArchivo, btnCalcular, btnLimpiar, textArea
    direccionArchivo = cargarDireccion()
    if not direccionArchivo:
        print("Error al cargar archivo")
        return
    mostrarContenidoArchivo(direccionArchivo)  # Mostrar contenido del archivo
    btnCalcular.configure(state="normal") # Habilitar el botón "Calcular Primeros y Siguientes"
    btnLimpiar.configure(state="normal")

# Función para mostrar el contenido del archivo en el área de texto
def mostrarContenidoArchivo(direccionArchivo):
    global textArea  
    try:
        with open(direccionArchivo, 'r') as file:
            contenido = file.read()
            textArea.delete(1.0, tk.END)  # Limpiar el área de texto
            textArea.insert(tk.END, contenido)  # Insertar el contenido del archivo
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {str(e)}")

# Función para calcular Primeros y Siguientes
def calcular():
    global direccionArchivo
    try:
        noTerminales, terminales = cargarDatos(direccionArchivo)
        reglasProduccion = getReglasProduccion(direccionArchivo)
        datos = mainPyS(noTerminales, terminales, reglasProduccion)
        mostrarResultados(datos)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo: {str(e)}")

# Función para limpiar el contenido del archivo y la tabla
def limpiarTabla():
    global direccionArchivo, textArea, treeview, btnCalcular, btnLimpiar
    direccionArchivo = ""  # Limpiar la variable de dirección del archivo
    textArea.delete(1.0, tk.END)  # Limpiar el área de texto
    for item in treeview.get_children():
        treeview.delete(item)  # Limpiar los datos de la tabla
    btnCalcular.configure(state="disabled")  # Deshabilitar el botón "Calcular Primeros y Siguientes"



def ventanaPYS_Aux():
    global treeview, textArea, btnCalcular, btnLimpiar
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("green") 
    # Crear la ventana principal
    ventana = ctk.CTk()
    ventana.title("ALGORITMO DE PRIMEROS Y SIGUIENTES")
    ventana.geometry("1000x700")

    # Crear un frame para los botones y colocarlos verticalmente
    frameBotones = ctk.CTkFrame(ventana, fg_color="transparent")
    frameBotones.pack(side=ctk.LEFT, padx=10, pady=700/3, fill=ctk.Y)

    # Crear los botones
    btnCargar = ctk.CTkButton(frameBotones, text="Cargar Archivo", command=obtenerDireccion)
    btnCargar.pack(pady=10, fill=ctk.X)

    btnCalcular = ctk.CTkButton(frameBotones, text="Calcular Primeros y Siguientes", command=calcular)
    btnCalcular.pack(pady=10,fill=ctk.X)
    btnCalcular.configure(state="disabled")

    btnLimpiar =  ctk.CTkButton(frameBotones, text="Limpiar Tabla", command=limpiarTabla)
    btnLimpiar.pack(pady=10, fill=tk.X)
    btnLimpiar.configure(state="disabled")

    style = ttk.Style()
    style.theme_use("default")  
    style.configure("Treeview", 
                background="#b4c5e4",  # Fondo de las filas
                fieldbackground="white",  # Fondo vacío
                foreground="black")  # Color del texto
    style.configure("Treeview.Heading", 
                background="#3CB35A",  # Fondo de los encabezados
                foreground="white",   # Color del texto de los encabezados
                font=("Arial", 10, "bold"))
    # Crear un Treeview para mostrar los resultados sin la columna "Contenido"
    columns = ("NoTerminal", "Primeros", "Siguientes")
    treeview = ttk.Treeview(ventana, columns=columns, show="headings")
    treeview.heading("NoTerminal", text="No Terminal")
    treeview.heading("Primeros", text="Primeros")
    treeview.heading("Siguientes", text="Siguientes")
    treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Crear un área de texto para mostrar el contenido del archivo
    textArea = tk.Text(ventana, height=10, width=80)
    textArea.pack(pady=10)

    # Iniciar la interfaz
    ventana.mainloop()

#ventanaPYS_Aux()