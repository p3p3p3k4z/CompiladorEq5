import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, END
import os
import sys

# Agregar las rutas de las librerías necesarias
lib_path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorLexico_thompson'))
sys.path.append(lib_path1)
lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorLexico_conjuntos'))
sys.path.append(lib_path2)

from thompson_aux import *
from conjuntos_aux import *
from thompson_automata import *

# Al iniciar, habilitamos solo "Seleccionar"

def xd_conjunto():
    # Inicializa la ventana principal
    ctk.set_appearance_mode("dark")  # Modo oscuro
    ctk.set_default_color_theme("green")  # Establece el tema verde oscuro

    ventana = ctk.CTkToplevel()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    #inicializar y desactivar botones 
    # Función para habilitar/deshabilitar los botones
    def habilitar_botones(estado):
        if estado == "seleccionar":
            boton1.configure(state="normal")
            boton2.configure(state="disabled")
            boton3.configure(state="disabled")
        elif estado == "generar":
            boton1.configure(state="disabled")
            boton2.configure(state="normal")
            boton3.configure(state="disabled")
        elif estado == "limpiar":
            boton1.configure(state="normal")
            boton2.configure(state="disabled")
            boton3.configure(state="normal")

    def abrir_archivo(alpha_entry, er_entry, lex_window):
        initial_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Pruebas_expresiones_reg"))
        lex_window.grab_set()
        alpha_entry.delete(0, END)
        er_entry.delete(0, END)
        
        direccion_archivo = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Abrir archivo",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        
        if not direccion_archivo:
            lex_window.grab_release()
            return
        
        with open(direccion_archivo, "r") as archivo:
            alfabeto = archivo.readline().strip()
            expresion_regular = archivo.readline().strip()
        
        expresion_regular = expresion_regular.replace("digitos", "d").replace("letras", "l")
        alfabeto = alfabeto.replace("letras", "l").replace("digitos", "d")
        
        alpha_entry.insert(0, alfabeto)
        er_entry.insert(0, expresion_regular)
        lex_window.grab_release()

        habilitar_botones("generar")

    #Limpiar
    def limpiar_tabla(canvas, tabla_frame_interno):
        # Limpiar el canvas
        canvas.delete("all")
        tabla_frame_interno.destroy()  # Eliminar el marco interno
        # Crear un nuevo marco interno vacío para futuras tablas
        tabla_frame_interno = ctk.CTkFrame(canvas, bg_color='#242727')
        canvas.create_window((0, 0), window=tabla_frame_interno, anchor="nw")
        # Restablecer el tamaño del canvas si es necesario
        canvas.config(scrollregion=canvas.bbox("all"))
        habilitar_botones("seleccionar")
        entrada_expresion.delete(0, tk.END)
        entrada_alfabeto.delete(0, tk.END)

    def obtener_automata(alfabeto, expresion_regular, tabla_frame_interno, canvas):
        try:
            expresion_postfija_resultado = expresion_postfija(expresion_regular)
            print(f"La expresión regular convertida a postfija es: {expresion_postfija_resultado}")
            Automata = evaluar_expresion_postfija(expresion_postfija_resultado)
        except Exception as e:
            print(f"Error al generar el autómata: {e}")
            return

        font1 = ("Display", 11)
        abecedario = list(alfabeto) + ["λ"]
        
        # Limpiar canvas existente
        canvas.delete("all")  # Limpiar canvas antes de redibujar
        canvas.config(bg='black')
        
        # Obtener el tamaño del canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Ancho y alto de las celdas
        ancho_celda = canvas_width // (len(abecedario) + 1)  # Ancho de celda calculado según el tamaño del canvas
        alto_celda = 40  # Alto fijo de las celdas
        
        # Crear encabezado de la tabla
        x_offset = 0
        y_offset = 0

        # Encabezado de "Estado"
        canvas.create_text(x_offset + ancho_celda / 2, y_offset + alto_celda / 2, text="Estado", font=fuente2,fill='#b4bdbd')

        # Crear encabezado para cada letra en el alfabeto
        for letra in abecedario:
            x_offset += ancho_celda  # Mover a la siguiente columna
            canvas.create_text(x_offset + ancho_celda / 2, y_offset + alto_celda / 2, text=str(letra), font=fuente2,fill='#b4bdbd')

        # Ajustar el y_offset para las filas de la tabla (debajo del encabezado)
        y_offset += 45 # Mover el offset Y para empezar las filas después del encabezado

        # Generar las filas de la tabla con los estados y transiciones
        i = 0.5
        nodo = Automata.head
        while nodo:
            x_offset = 0  # Resetear x_offset para cada fila

            num_estado = nodo.state.getId()

            # Generar el texto para la celda dependiendo del estado
            if num_estado == 0:
                texto_estado = str(num_estado) + " i"
            elif nodo.state.getFinalState():
                texto_estado = str(num_estado) + " f"
            else:
                texto_estado = str(num_estado)

            # Crear el texto para el estado
            canvas.create_text(x_offset + ancho_celda / 2, y_offset + (i * alto_celda), text=texto_estado, font=fuente2,fill='#b4bdbd')
            x_offset += ancho_celda  # Mover a la siguiente columna después del estado

            # Obtener las transiciones
            edos = nodo.state.getTransitions()
            for transition in edos:
                caracter = transition.getSymbol()

                # Comparar el caracter con el alfabeto
                for aux in abecedario:
                    if aux == caracter:
                        texto_transicion = str(nodo.state)  # Cambiar esto según la información que quieras mostrar
                        canvas.create_text(x_offset + ancho_celda / 2, y_offset + (i * alto_celda), text=texto_transicion, font=fuente2,fill='#b4bdbd')
                    else:
                        canvas.create_text(x_offset + ancho_celda / 2, y_offset + (i * alto_celda), text="-", font=fuente2,fill='#b4bdbd')
                    x_offset += ancho_celda  # Mover a la siguiente columna
            i += 1
            nodo = nodo.next

            # Dibujar las divisiones horizontales (líneas entre las filas)
            canvas.create_line(0, y_offset + (i * alto_celda)-60, canvas_width, y_offset + (i * alto_celda)-60, width=2,fill='#b4bdbd')

        # Dibujar la última línea horizontal (final de la tabla)
        canvas.create_line(0, y_offset + (i * alto_celda)-15, canvas_width, y_offset + (i * alto_celda)-15, width=2,fill='#b4bdbd')

        # Actualizar la región de desplazamiento
        canvas.config(scrollregion=canvas.bbox("all"))
        # Ajustar el tamaño del canvas dinámicamente
        canvas.config(width=canvas_width, height=y_offset + (i * alto_celda) + 50)  # Establecer el tamaño del canvas
        habilitar_botones("limpiar")

    
    fuente = ("Courier New", 15,"bold")  # Fuente Arial con tamaño 14

    fuente2 = ("Courier New", 18,"bold")  # Fuente Arial con tamaño 14

    ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    ventana.title("Algoritmo de Thompson")

    # Frame para los botones
    casa_btn = ctk.CTkFrame(ventana)
    casa_btn.pack(pady=50, padx=0)

    # Crear los botones y etiquetas
    etiqueta = ctk.CTkLabel(casa_btn, text="Seleccionar expresión regular:", width=300, anchor="w",font=fuente)
    etiqueta.grid(row=0, column=0, sticky="w", padx=10)

    boton1 = ctk.CTkButton(casa_btn, text="Seleccionar", width=120, height=30, font=fuente, command=lambda: abrir_archivo(entrada_alfabeto, entrada_expresion, ventana))
    boton1.grid(row=0, column=1, padx=10, pady=10)

    etiqueta2 = ctk.CTkLabel(casa_btn, text="Expresión Regular:", width=300, anchor="w",font=fuente)
    etiqueta2.grid(row=1, column=0, sticky="w", padx=10)
    entrada_expresion = ctk.CTkEntry(casa_btn, width=200, font=fuente)
    entrada_expresion.grid(row=1, column=1, padx=10, pady=5)

    etiqueta = ctk.CTkLabel(casa_btn, text="Alfabeto:", width=200, anchor="w",font=fuente)
    etiqueta.grid(row=2, column=0, sticky="w", padx=10)
    entrada_alfabeto = ctk.CTkEntry(casa_btn, width=200, font=fuente)
    entrada_alfabeto.grid(row=2, column=1, padx=10, pady=5)

    boton2 = ctk.CTkButton(casa_btn, text="Obtener Aútomata AFND", width=120, height=30, font=fuente, command=lambda: obtener_automata(entrada_alfabeto.get(), entrada_expresion.get(), tabla_frame_interno, canvas))
    boton2.grid(row=3, column=0, pady=10, padx=5)

    boton3 = ctk.CTkButton(casa_btn, text="Limpiar", width=120, height=30, font=fuente,command=lambda: limpiar_tabla(canvas, tabla_frame_interno))
    boton3.grid(row=3, column=1, pady=10, padx=10)

    casa_btn.grid_columnconfigure((0, 1, 2), weight=1)
    habilitar_botones("seleccionar")

    # Crear tabla y canvas para mostrar el autómata
    tabla_frame = ctk.CTkFrame(ventana, bg_color='#242727')
    tabla_frame.pack(padx=10, pady=20, fill="both", expand=True)

    canvas = ctk.CTkCanvas(tabla_frame)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.config(bg='#242727',highlightbackground='#242727')

    # Crear un marco dentro del canvas donde colocarás la tabla
    tabla_frame_interno = ctk.CTkFrame(canvas, bg_color='#242727')
    canvas.create_window((0, 0), window=tabla_frame_interno, anchor="nw")


    scrollbar = ctk.CTkScrollbar(tabla_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.config(yscrollcommand=scrollbar.set,bg='#242727',highlightbackground='#242727' )
    ventana.mainloop()  
