import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys

lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorSintacticoLR_primerosYsiguientes'))
sys.path.append(lib_path2)

from Primeros_Siguientes import *

# Variable global para almacenar la dirección del archivo
direccionArchivo = ""

# Función para mostrar resultados en la tabla
def mostrarResultados(datos):
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
    global direccionArchivo
    direccionArchivo = cargarDireccion()
    if not direccionArchivo:
        print("Error al cargar archivo")
        return
    mostrarContenidoArchivo(direccionArchivo)  # Mostrar contenido del archivo
    btnCalcular.config(state=tk.NORMAL)  # Habilitar el botón "Calcular Primeros y Siguientes"
    btnLimpiar.config(state=tk.NORMAL)

# Función para mostrar el contenido del archivo en el área de texto
def mostrarContenidoArchivo(direccionArchivo):
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
    global direccionArchivo
    direccionArchivo = ""  # Limpiar la variable de dirección del archivo
    textArea.delete(1.0, tk.END)  # Limpiar el área de texto
    for item in treeview.get_children():
        treeview.delete(item)  # Limpiar los datos de la tabla
    btnCalcular.config(state=tk.DISABLED)  # Deshabilitar el botón "Calcular Primeros y Siguientes"

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("ALGORITMO DE PRIMEROS Y SIGUIENTES")
ventana.geometry("1000x700")

# Crear un frame para los botones y colocarlos verticalmente
frameBotones = tk.Frame(ventana)
frameBotones.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Crear los botones
btnCargar = tk.Button(frameBotones, text="Cargar Archivo", command=obtenerDireccion)
btnCargar.pack(pady=10, fill=tk.X)

btnCalcular = tk.Button(frameBotones, text="Calcular Primeros y Siguientes", command=calcular, state=tk.DISABLED)
btnCalcular.pack(pady=10, fill=tk.X)

btnLimpiar = tk.Button(frameBotones, text="Limpiar Tabla", command=limpiarTabla, state=tk.DISABLED)
btnLimpiar.pack(pady=10, fill=tk.X)

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
