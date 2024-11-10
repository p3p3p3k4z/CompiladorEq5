from tkinter import *

class Ventana:
    def __init__(self, ancho=300, alto=250, titulo="Mi Ventana", color_fondo="white"):
        # Inicializar la ventana principal
        self.root = Tk()
        self.root.geometry(f"{ancho}x{alto}")
        self.root.title(titulo)
        self.root.configure(bg=color_fondo)

        # Lista para almacenar los botones
        self.botones = []

    def cambiar_titulo(self, nuevo_titulo):
        # Cambiar el título de la ventana
        self.root.title(nuevo_titulo)

    def cambiar_tamano(self, ancho, alto):
        # Cambiar el tamaño de la ventana
        self.root.geometry(f"{ancho}x{alto}")

    def cambiar_color_fondo(self, color):
        # Cambiar el color de fondo de la ventana
        self.root.configure(bg=color)

    def agregar_boton(self, boton, x, y):
        # Mostrar un botón en la ventana y añadirlo a la lista de botones
        boton.mostrar(x, y)
        self.botones.append(boton)

    def habilitar_botones(self):
        # Habilitar todos los botones en la lista
        for boton in self.botones:
            boton.habilitar()

    def deshabilitar_botones(self):
        # Deshabilitar todos los botones en la lista
        for boton in self.botones:
            boton.deshabilitar()

    def cambiar_fuente_botones(self, tipo_fuente="Helvetica", tamaño=12, negrita=False, cursiva=False):
        # Cambiar la fuente de todos los botones en la ventana
        for boton in self.botones:
            boton.cambiar_fuente(tipo_fuente, tamaño, negrita, cursiva)

    def ejecutar(self):
        # Ejecutar el bucle principal de la ventana
        self.root.mainloop()

    def maximizar(self):
        # Maximizar la ventana
        self.root.state('zoomed')

    def minimizar(self):
        # Minimizar la ventana
        self.root.iconify()

    def ajustar(self):
        # Restaurar la ventana a su tamaño original
        self.root.state('normal')
