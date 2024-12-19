import os
import re
from collections import defaultdict
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Clase para cargar gramática
class CargarGramatica:
    def __init__(self, filename):
        self.no_terminales = []  
        self.producciones = defaultdict(list)
        self.leer_gramatica(filename)

    def leer_gramatica(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"El archivo {filename} no existe.")
        with open(filename, 'r') as file:
            for linea in file:
                linea = linea.strip()
                if "->" in linea:
                    no_terminal, produccion = linea.split("->")
                    no_terminal = no_terminal.strip()
                    produccion = produccion.strip()
                    if no_terminal not in self.no_terminales:
                        self.no_terminales.append(no_terminal)
                    self.producciones[no_terminal].append(produccion)

    def get_no_terminales(self):
        return self.no_terminales

    def get_producciones(self):
        return self.producciones


# Clase para calcular PRIMERO
class Primero:
    def __init__(self, cargar_gramatica):
        self.primeros = defaultdict(set)
        self.producciones = cargar_gramatica.get_producciones()
        self.no_terminales = cargar_gramatica.get_no_terminales()
        self.calculados = set()
        self.calcular_primero()

    def resultados(self):
        resultado = ""
        for no_terminal in self.no_terminales:
            resultado += f"PRIMERO({no_terminal}) = {self.primeros[no_terminal]}\n"
        return resultado

    def calcular_primero(self):
        for no_terminal in self.no_terminales:
            if no_terminal not in self.calculados:
                self.primero_noTerminal(no_terminal)

    def primero_noTerminal(self, no_terminal):
        self.calculados.add(no_terminal)
        for produccion in self.producciones[no_terminal]:
            tokens = produccion.split()
            for token in tokens:
                if self.es_terminal(token):
                    self.primeros[no_terminal].add(token)
                    break
                else:
                    if token not in self.calculados:
                        self.primero_noTerminal(token)
                    self.primeros[no_terminal].update(self.primeros[token] - {'ϵ'})
                    if 'ϵ' not in self.primeros[token]:
                        break
            else:
                self.primeros[no_terminal].add('ϵ')

    def es_terminal(self, cadena):
        return not re.match(r"[A-Z]", cadena)


# Clase para calcular SIGUIENTES
class Siguientes:
    def __init__(self, cargar_gramatica, primero):
        self.siguientes = defaultdict(set)
        self.producciones = cargar_gramatica.get_producciones()
        self.primeros = primero.primeros
        self.no_terminales = cargar_gramatica.get_no_terminales()
        self.siguientes[self.no_terminales[0]].add('$')
        self.calcular_siguientes()

    def resultados(self):
        resultado = ""
        for no_terminal in self.no_terminales:
            resultado += f"SIGUIENTE({no_terminal}) = {self.siguientes[no_terminal]}\n"
        return resultado

    def calcular_siguientes(self):
        cambios = True
        while cambios:
            cambios = False
            for lhs, producciones in self.producciones.items():
                for produccion in producciones:
                    tokens = produccion.split()
                    for i, token in enumerate(tokens):
                        if token not in self.producciones:
                            continue
                        if i + 1 < len(tokens):
                            siguiente_token = tokens[i + 1]
                            if self.es_terminal(siguiente_token):
                                if siguiente_token not in self.siguientes[token]:
                                    self.siguientes[token].add(siguiente_token)
                                    cambios = True
                            else:
                                nuevos = self.primeros[siguiente_token] - {'ϵ'}
                                if not nuevos.issubset(self.siguientes[token]):
                                    self.siguientes[token].update(nuevos)
                                    cambios = True
                                if 'ϵ' in self.primeros[siguiente_token]:
                                    nuevos = self.siguientes[lhs]
                                    if not nuevos.issubset(self.siguientes[token]):
                                        self.siguientes[token].update(nuevos)
                                        cambios = True
                        else:
                            nuevos = self.siguientes[lhs]
                            if not nuevos.issubset(self.siguientes[token]):
                                self.siguientes[token].update(nuevos)
                                cambios = True

    def es_terminal(self, cadena):
        return not re.match(r"[A-Z]", cadena)


# Funciones
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
            mostrar_primero_btn.configure(state="normal")
            mostrar_siguiente_btn.configure(state="disabled")

            with open(archivo_path, 'r') as file:
                gramatica_text.delete("0.0", "end")
                gramatica_text.insert("0.0", file.read())
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la gramática: {str(e)}")


def mostrar_primero():
    global siguiente_obj
    resultado_primero = primero_obj.resultados()
    primeros_text.delete("0.0", "end")
    primeros_text.insert("0.0", resultado_primero)

    siguiente_obj = Siguientes(cargar_gramatica_obj, primero_obj)
    mostrar_primero_btn.configure(state="disabled")
    mostrar_siguiente_btn.configure(state="normal")


def mostrar_siguiente():
    resultado_siguiente = siguiente_obj.resultados()
    siguientes_text.delete("0.0", "end")
    siguientes_text.insert("0.0", resultado_siguiente)

    mostrar_siguiente_btn.configure(state="disabled")
    limpiar_btn.configure(state="normal")


def limpiar_campos():
    gramatica_text.delete("0.0", "end")
    primeros_text.delete("0.0", "end")
    siguientes_text.delete("0.0", "end")

    mostrar_primero_btn.configure(state="disabled")
    mostrar_siguiente_btn.configure(state="disabled")
    limpiar_btn.configure(state="disabled")
    cargar_btn.configure(state="normal")
