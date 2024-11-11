from tkinter import Tk

class Ventana:
    def __init__(self, ancho=300, alto=250, titulo="Ventana"):
        self.root = Tk()
        self.root.geometry(f"{ancho}x{alto}")
        self.root.title(titulo)

    def ejecutar(self):
        self.root.mainloop()
