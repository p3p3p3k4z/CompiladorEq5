import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, END
import os
import sys

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

lib_path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorLexico_thompson'))
sys.path.append(lib_path1)
lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compi_analizadorLexico_conjuntos'))
sys.path.append(lib_path2)

from thompson_aux import *
from conjuntos_aux import *
from thompson_automata import *




 #botones


#----------------------------------------------------------------------------------
def mini ():
    fuente2 = ("Courier New", 18,"bold")  
    arrLabels = []  # Declaración global
    #Inicializar la ventana principal en el modo dark greeen
    ctk.set_appearance_mode("dark")  # Modo oscuro
    ctk.set_default_color_theme("green")  # Establece el tema verde oscuro
    def habilitar_botones(estado):
        if estado == "seleccionar":
            boton1.configure(state="normal")
            boton2.configure(state="disabled")
            boton3.configure(state="disabled")
        elif estado == "generar":
            boton1.configure(state="normal")
            boton2.configure(state="normal")
            boton3.configure(state="disabled")
        elif estado == "limpiar":
            boton1.configure(state="disabled")
            boton2.configure(state="disabled")
            boton3.configure(state="normal")
    
#FUNCIONES
    def obtener_automata(alfabeto, expresion_regular, tabla_frame , canvas):
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
        canvas.create_text(x_offset + ancho_celda / 2, y_offset + alto_celda / 2, text="Estado", font=fuente2,fill='white')

        # Crear encabezado para cada letra en el alfabeto
        for letra in abecedario:
            x_offset += ancho_celda  # Mover a la siguiente columna
            canvas.create_text(x_offset + ancho_celda / 2, y_offset + alto_celda / 2, text=str(letra), font=fuente2,fill='white')

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
            canvas.create_text(x_offset + ancho_celda / 2, y_offset + (i * alto_celda), text=texto_estado, font=fuente2,fill='white')
            x_offset += ancho_celda  # Mover a la siguiente columna después del estado

            # Obtener las transiciones
            edos = nodo.state.getTransitions()
            for transition in edos:
                caracter = transition.getSymbol()

                # Comparar el caracter con el alfabeto
                for aux in abecedario:
                    if aux == caracter:
                        texto_transicion = str(nodo.state)  # Cambiar esto según la información que quieras mostrar
                        canvas.create_text(x_offset + ancho_celda / 2, y_offset + (i * alto_celda), text=texto_transicion, font=fuente2,fill='white')
                    else:
                        canvas.create_text(x_offset + ancho_celda / 2, y_offset + (i * alto_celda), text="-", font=fuente2,fill='white')
                    x_offset += ancho_celda  # Mover a la siguiente columna
            i += 1
            nodo = nodo.next

            # Dibujar las divisiones horizontales (líneas entre las filas)
            canvas.create_line(0, y_offset + (i * alto_celda)-60, canvas_width, y_offset + (i * alto_celda)-60, width=2,fill='white')

        # Dibujar la última línea horizontal (final de la tabla)
        canvas.create_line(0, y_offset + (i * alto_celda)-15, canvas_width, y_offset + (i * alto_celda)-15, width=2,fill='white')

        # Actualizar la región de desplazamiento
        canvas.config(scrollregion=canvas.bbox("all"))
        # Ajustar el tamaño del canvas dinámicamente
        canvas.config(width=canvas_width, height=y_offset + (i * alto_celda) + 50)  # Establecer el tamaño del canvas

    #Funcion abrir archivo
    def abrir_Archivo(alphaEntry, erEntry, lexWindow):
        initial_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Pruebas_expresiones_reg"))
        lexWindow.grab_set()
        alphaEntry.delete(0, END)
        erEntry.delete(0, END)
        
        direccionArchivo = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Abrir archivo",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        
        if not direccionArchivo:  # Si el usuario cancela la selección, no hace nada
            lexWindow.grab_release()
            return

        with open(direccionArchivo, "r") as archivo:
            alfabeto = archivo.readline().strip()
            expresionRegular = archivo.readline().strip()

        expresionRegular = expresionRegular.replace("digitos", "d").replace("letras", "l")
        alfabeto = alfabeto.replace("letras", "l")

        # Inicialización de banderas
        bandera_transformacion_digitos = 0
        bandera_transformacion_alfabeto = 0

        if "digitos" in alfabeto:
            alfabeto = alfabeto.replace("digitos", "d")
            bandera_transformacion_digitos = 1

        if "letras" in alfabeto:
            alfabeto = alfabeto.replace("letras", "l")
            bandera_transformacion_alfabeto = 1

        print(f"Alfabeto: {alfabeto} (Bandera dígitos: {bandera_transformacion_digitos}, Bandera letras: {bandera_transformacion_alfabeto})")
        print(f"Expresión Regular: {expresionRegular}")

        alphaEntry.insert(0, alfabeto)
        erEntry.insert(0, expresionRegular)
        lexWindow.grab_release()
        habilitar_botones("generar")
    
    #LIMPUAR
    def limpiar_tabla(canvas):
        # Eliminar todos los objetos almacenados en la lista
        for item in elementos_canvas:
            canvas.delete(item)
        
        # Vaciar las entradas de texto
        habilitar_botones("seleccionar")
        entrada_expresion.delete(0, tk.END)
        entrada_alfabeto.delete(0, tk.END)

        # Limpiar la lista de objetos
        elementos_canvas.clear()


    # Lista para almacenar las referencias de los objetos en el canvas
    elementos_canvas = []

    def printTableConjuntos(alfabeto, canvas, lexWindow, arrLabels, er):
        columna = 1
        abecedario = []
        numEstados = len(alfabeto)  # Número de estados
        if numEstados:  # Verificar que exista un alfabeto
            # Obtener el AFN y AFD
            expresion_reg = expresion_postfija(er)
            Automata = evaluar_expresion_postfija(expresion_reg)

            cerradura = []
            cerradura.append(0)
            cerradura = cerradura_e(cerradura, Automata.head, "λ")
            cerradura.append(0)
            NuevosEstados = AFD(cerradura, alfabeto, Automata.head)
            print(NuevosEstados)

            if not lexWindow.winfo_exists():  # Verifica si la ventana aún existe
             return
            # Imprimir el alfabeto y encabezados
            label_fantasma = ctk.CTkLabel(canvas, text="     ", width=10)
            ventana = canvas.create_window(0, 0, window=label_fantasma)
            elementos_canvas.append(ventana)
            fila = 0  # Fila de la tabla
            columna = 1  # Columna de la tabla

            # Verifica si el alfabeto contiene 'letra' o 'digito'
            bandera_letra = False
            if 'l' in alfabeto and 'd' in alfabeto:
                alfabeto_aux = alfabeto.replace('l', "")
                alfabeto_aux = alfabeto.replace('d', "")
                if len(alfabeto_aux) > 0:
                    bandera_letra = True
            elif 'l' in alfabeto:
                alfabeto_aux = alfabeto.replace('l', "")
                if len(alfabeto_aux) > 0:
                    bandera_letra = True

            # Imprimir el alfabeto
            idSimbolos = 1
            dictSimbolos = {}

            # Calcular el tamaño de las columnas
            num_columnas = len(alfabeto) + 1
            canvas_width = canvas.winfo_width()  # Obtener el ancho del canvas
            espacio_por_columna = canvas_width // 2 // num_columnas  # Calcular el espacio por columna
            margen_izquierdo = (canvas_width - (espacio_por_columna * num_columnas)) // 0.8 // num_columnas
            
            # Imprimir el número final de columnas
            print("Número total de columnas calculado:", num_columnas)
                
            for letra in alfabeto:
                label_fantasma = ctk.CTkLabel(canvas, text="     ", width=10)
                ventana = canvas.create_window(0, 0, window=label_fantasma)
                elementos_canvas.append(ventana)

                # Reemplaza 'l' por 'letra' y 'd' por 'digito'
                letra_aux = letra
                if letra == 'l':
                    letra_aux = "letra"
                elif letra == 'd':
                    letra_aux = "digito"

                ColumnaL = ctk.CTkLabel(canvas, text=letra_aux, width=15, font=fuente2)
                ventana = canvas.create_window(margen_izquierdo + columna * espacio_por_columna, fila * 50, window=ColumnaL)
                elementos_canvas.append(ventana)
                arrLabels.append(ColumnaL)
                abecedario.append(letra)
                dictSimbolos[idSimbolos] = letra

            
                if letra != 'l' and letra != 'd' and bandera_letra:
                    num_columnas+=1
                    columna += 1
                    idSimbolos += 1
                    letra_aux2 = "letra-" + letra_aux
                    ColumnaL = ctk.CTkLabel(canvas, text=letra_aux2, width=15, font=fuente2)
                    ventana = canvas.create_window(margen_izquierdo + columna * espacio_por_columna, fila * 50, window=ColumnaL)
                    elementos_canvas.append(ventana)
                    arrLabels.append(ColumnaL)
                    abecedario.append(letra)
                    dictSimbolos[idSimbolos] = letra_aux2
                columna += 1
                idSimbolos += 1
                print("Número de columnas ajustado:", num_columnas)
            # Imprimir "Estado" en la primera columna
            encabezadoL = ctk.CTkLabel(canvas, text="Estado", font=fuente2, width=10)
            ventana = canvas.create_window(margen_izquierdo + 0 * espacio_por_columna, fila * 50, window=encabezadoL)
            elementos_canvas.append(ventana)
            arrLabels.append(encabezadoL)
            abecedario.append("λ")


            # Dibujar la línea horizontal inicial (tapita)
            y_pos_tapita = fila * 50 - (espacio_por_columna // 4)  # Ajustar la posición Y para estar justo antes de los encabezados
            ancho_linea = margen_izquierdo + (num_columnas * espacio_por_columna)

            linea_tapita=canvas.create_line(
                margen_izquierdo - (espacio_por_columna // 2), 
                y_pos_tapita, 
                ancho_linea - (espacio_por_columna // 2),
                y_pos_tapita,  
                width=2, 
                fill='#b4bdbd'
                )
            elementos_canvas.append(linea_tapita)
            # Imprimir los estados y transiciones
            EstadoFinal = encontrarEstadoFinal(Automata.head)
            fila = 1
            tamañoLista = len(NuevosEstados)
            nodo = NuevosEstados
            for i in range(tamañoLista):
                columna = 0
                estados_no_renombrados = nodo[i][1]
                for auxxx in estados_no_renombrados:
                    if auxxx == 0:
                        celda = ctk.CTkLabel(canvas, text=nodo[i][0] + " i", width=10, font=fuente2)
                        break
                    elif auxxx == EstadoFinal:
                        celda = ctk.CTkLabel(canvas, text=nodo[i][0] + " f", width=10, font=fuente2)
                    else:
                        celda = ctk.CTkLabel(canvas, text=nodo[i][0], width=10, font=fuente2)

                # Calcular la posición exacta para la celda
                x_pos = margen_izquierdo - (espacio_por_columna // 2)
                y_pos = fila * 50

                ventana = canvas.create_window(margen_izquierdo + columna * espacio_por_columna, fila * 50, window=celda)
                elementos_canvas.append(ventana)

                columna = 1

                # Imprimir las transiciones
                for j in range(len(dictSimbolos)):
                    simbolo = dictSimbolos[columna]
                    transicionesDentro = nodo[i][2]
                    for transicion in transicionesDentro:
                        if transicion[1] == simbolo:
                            celda_sym = ctk.CTkLabel(canvas, text=transicion[2], width=15, height=15, font=fuente2)
                            ventana = canvas.create_window(margen_izquierdo + columna * espacio_por_columna, fila * 50, window=celda_sym)
                            elementos_canvas.append(ventana)
                            break
                        else:
                            celda_sym = ctk.CTkLabel(canvas, text="-", width=15, height=15, font=fuente2)
                            ventana = canvas.create_window(margen_izquierdo + columna * espacio_por_columna, fila * 50, window=celda_sym)
                            elementos_canvas.append(ventana)
                    columna += 1
               # Ajustar la posición de la línea horizontal
            
                y_pos_linea = (y_pos + (i * 50) +20 ) //2# Mueve la línea más abajo (ajustando el valor de 20)
                ancho_linea = margen_izquierdo + (num_columnas * espacio_por_columna )
                h=canvas.create_line(
                    margen_izquierdo-(espacio_por_columna//2), 
                    y_pos_linea,  # Posición Y ajustada
                    ancho_linea-(espacio_por_columna//2),
                    y_pos_linea,  # La misma posición Y para la línea horizontal
                    width=2, 
                    fill='#b4bdbd'
                )
                elementos_canvas.append(h)
                fila += 1
            
            y_pos_linea=y_pos+((i*50)//8)
            h2=canvas.create_line(
                margen_izquierdo-(espacio_por_columna//2), 
                y_pos_linea,  # Posición Y ajustada
                ancho_linea-(espacio_por_columna//2),
                y_pos_linea,  # La misma posición Y para la línea horizontal
                width=2, 
                fill='#b4bdbd'
                )
            elementos_canvas.append(h2)
            
            for col in range(num_columnas + 1):  # Incluye la primera columna de "Estado"
                x_pos_linea = (margen_izquierdo + col * espacio_por_columna)-(espacio_por_columna//2)  # Posición X de la línea
                y_inicio = 0-(espacio_por_columna//4)  # Inicio de la línea (arriba)
                y_fin = (fila * 50)-(espacio_por_columna//8.8)  # Fin de la línea (abajo), ajustado a la cantidad de filas

                v=canvas.create_line(
                    x_pos_linea, y_inicio,
                    x_pos_linea, y_fin,
                    width=2,
                    fill='#b4bdbd'
                )
                elementos_canvas.append(v)
            # Actualiza la tabla
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            lexWindow.grab_set()
            messagebox.showerror("Error", "Introduce un alfabeto")
            lexWindow.grab_release()

        habilitar_botones("limpiar")

    #Hacer la ventana con el tamaño de la pantalla completa
    ventana = ctk.CTkToplevel()  # Esto crea una ventana secundaria sin interferir con la principal
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()                     
    #Fuentes de letra
    fuente = ("Courier New", 16,"bold") 

    ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    ventana.title("Construcción de conjuntos-Aútomata Finito Determinista-")

    # Frame para los botones
    casa_btn = ctk.CTkFrame(ventana)
    casa_btn.pack(pady=50, padx=0)

    #Botones y etiquetas
    etiqueta = ctk.CTkLabel(casa_btn, text="Seleccionar una expresión regular:", width=300, anchor="w",font=fuente)
    etiqueta.grid(row=0, column=0, sticky="w", padx=10)

    boton1 = ctk.CTkButton(casa_btn, text="Seleccionar", width=120, height=30, font=fuente, command=lambda: abrir_Archivo(entrada_alfabeto, entrada_expresion, ventana))
    boton1.grid(row=0, column=1, padx=10, pady=10)

    etiqueta2 = ctk.CTkLabel(casa_btn, text="Expresión Regular:", width=300, anchor="w",font=fuente)
    etiqueta2.grid(row=1, column=0, sticky="w", padx=10)
    entrada_expresion = ctk.CTkEntry(casa_btn, width=200, font=fuente)
    entrada_expresion.grid(row=1, column=1, padx=10, pady=5)

    etiqueta = ctk.CTkLabel(casa_btn, text="Alfabeto:", width=200, anchor="w",font=fuente)
    etiqueta.grid(row=2, column=0, sticky="w", padx=10)
    entrada_alfabeto = ctk.CTkEntry(casa_btn, width=200, font=fuente)
    entrada_alfabeto.grid(row=2, column=1, padx=10, pady=5)

    boton2 = ctk.CTkButton(casa_btn, text="Obtener Aútomata AFD", width=120, height=30, font=fuente, 
                            command=lambda: printTableConjuntos(entrada_alfabeto.get(),  canvas, ventana, arrLabels, entrada_expresion.get()))

    boton2.grid(row=3, column=0, pady=10, padx=5)

    boton3 = ctk.CTkButton(casa_btn, text="Limpiar", width=120, height=30, font=fuente,command=lambda: limpiar_tabla(canvas))
    boton3.grid(row=3, column=1, pady=10, padx=10)           

    habilitar_botones("seleccionar")
    # Crear tabla y canvas para mostrar el autómata

    tabla_frame = ctk.CTkFrame(ventana)
    tabla_frame.pack(padx=10, pady=20, fill="both", expand=True)

    canvas = ctk.CTkCanvas(tabla_frame)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.config(bg='#242727',highlightbackground='#242727') 
    ventana.mainloop()  
#b4bdbd , #2e3232 Este color tambien se ve lindo
# Ejecuta la ventana





