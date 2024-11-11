from tkinter import Menu
from ventana_imagen import VentanaImagen

class MenuVentana(VentanaImagen):
    def __init__(self, ancho=300, alto=250, titulo="Ventana con Menú", color_fondo="white"):
        super().__init__(ancho, alto, titulo, color_fondo)
        
        # Crear un menú
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.submenus = []
    
    def agregar_submenu(self, titulo, opciones, estado="normal"):
        submenu = Menu(self.menu_bar, tearoff=0)
        for opcion in opciones:
            submenu.add_command(label=opcion['label'], command=opcion['command'], state=opcion.get('state', 'normal'))
        self.menu_bar.add_cascade(label=titulo, menu=submenu, state=estado)
