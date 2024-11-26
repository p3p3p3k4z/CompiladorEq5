from tkinter import Tk

class Ventana:
    def __init__(self, ancho=300, alto=250, titulo="Ventana", color_fondo="white"):
        self.root = Tk()
        self.root.geometry(f"{ancho}x{alto}")
        self.root.title(titulo)
        self.root.configure(bg=color_fondo)

    def ejecutar(self):
        # Ejecutar el bucle principal de la ventana
        self.root.mainloop()

    def cambiar_titulo(self, nuevo_titulo):
        self.root.title(nuevo_titulo)

    def cambiar_tamano(self, ancho, alto):
        self.root.geometry(f"{ancho}x{alto}")

    def cambiar_color_fondo(self, color):
        self.root.configure(bg=color)
