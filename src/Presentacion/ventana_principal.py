import os
import sys

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Presentacion_Alexico'))
sys.path.append(lib_path)

from ventana_extra import MenuVentana

def Conjuntos():
    print("Ejecutando Conjuntos")

def Conjuntos_afn():
    print("Ejecutando Conjuntos AFN")

def abrir():
    print("Ejecutando abrir")

def VentanaPrincipal():
    # Crear instancia de MenuVentana
    ventana_con_menu = MenuVentana(ancho=850, alto=650, titulo="Pecera con Menú", color_fondo="cyan")
    ventana_con_menu.cargar_imagen("../../imagenes/portada.png")

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
