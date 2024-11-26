from tkinter import Tk, Menu
from ventana import Ventana

class MenuVentana(Ventana):
    def __init__(self, ancho=300, alto=250, titulo="Mi Ventana con Menú", color_fondo="white"):
        super().__init__(ancho, alto, titulo, color_fondo)
        self.menu_principal = Menu(self.root)
        self.root.config(menu=self.menu_principal)
        self.font = ("Times New Roman", 10)

    def agregar_submenu(self, label, opciones, estado="normal"):
        """
        Agrega un submenú al menú principal.
        :param label: nombre del submenú
        :param opciones: lista de opciones en el submenú, cada una debe ser un diccionario con las claves 'label', 'command', y 'state' (opcional)
        :param estado: estado del submenú ('normal' o 'disabled')
        """
        submenu = Menu(self.menu_principal, tearoff=0)
        for opcion in opciones:
            submenu.add_command(
                label=opcion.get("label", ""),
                command=opcion.get("command", None),
                state=opcion.get("state", "normal"),
                font=self.font
            )
        self.menu_principal.add_cascade(label=label, menu=submenu, state=estado)

'''
# Ejemplo de uso
if __name__ == "__main__":
    def Conjuntos():
        print("Ejecutando Conjuntos")

    def Conjuntos_afn():
        print("Ejecutando Conjuntos AFN")

    def abrir():
        print("Ejecutando abrir")

    # Crear instancia de MenuVentana
    ventana_con_menu = MenuVentana(ancho=850, alto=650, titulo="Pecera con Menú", color_fondo="cyan")

    # Agregar submenús y opciones
    ventana_con_menu.agregar_submenu("Análisis léxico", [
        {"label": "Algoritmo de Thomson(AFND)", "command": Conjuntos},
        {"label": "Construcción de conjuntos(AFD)", "command": Conjuntos_afn},
        {"label": "Analizador Léxico", "command": abrir, "state": "disabled"}
    ])

    ventana_con_menu.agregar_submenu("Análisis semántico", [
        {"label": "Calcular", "command": Conjuntos_afn}
    ], estado="disabled")

    ventana_con_menu.agregar_submenu("Análisis sintáctico", [
        {"label": "Abrir", "command": abrir}
    ], estado="disabled")

    # Ejecutar ventana
    ventana_con_menu.ejecutar()
'''
