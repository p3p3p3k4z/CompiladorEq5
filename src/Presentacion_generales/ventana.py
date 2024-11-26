from tkinter import Tk

class Ventana:
    def __init__(self, ancho=400, alto=300, titulo="Ventana"):
        self.root = Tk()
        self.root.geometry(f"{ancho}x{alto}")
        self.root.title(titulo)
        self.botones = []  # Lista para almacenar los botones en la ventana

    def agregar_boton(self, boton, x, y):
        # Coloca el botón en una posición específica
        boton.mostrar(y, x)
        self.botones.append(boton)  # Agregar botón a la lista para controlarlo después

    def habilitar_botones(self):
        # Habilitar todos los botones en la lista
        for boton in self.botones:
            boton.habilitar()

    def ejecutar(self):
        # Ejecutar el bucle principal de la ventana
        self.root.mainloop()
