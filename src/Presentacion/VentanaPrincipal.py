import os
import sys
from customtkinter import *
import pygame
import PIL

# Asegúrate de que las rutas de las librerías sean correctas
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Presentacion_Alexico'))
sys.path.append(lib_path)
lib_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Presentacion_sintactico'))
sys.path.append(lib_path2)
lib_path3 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Coleccion_canonica'))
sys.path.append(lib_path3)

from ventana_extra import MenuVentana
from VentanaConjuntos import *
from VentanaThompson import *
from inter import *

# Configuración global de customtkinter
set_appearance_mode("dark")  # Opciones: "dark" o "light"
set_default_color_theme("blue")  # Tema de colores

# Inicializar pygame para audio
pygame.mixer.init()

# Ruta del archivo de audio
AUDIO_PATH = "../../musica/main_theme.mp3"

# Variable de estado de música
is_playing = False

def toggle_music(button):
    global is_playing
    if not is_playing:
        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play()
        button.configure(text="")  # Detener música
        is_playing = True
    else:
        pygame.mixer.music.stop()
        button.configure(text="")  # Iniciar música
        is_playing = False

def ventanaPrincipal():
    global raiz
    raiz = CTk()
    raiz.geometry("800x500")
    raiz.title("Equipo5")

    # Crear el marco izquierdo para los botones
    menu_frame = CTkFrame(raiz, corner_radius=10, width=300)
    menu_frame.pack(side="left", fill="y", padx=10, pady=10)

    CTkLabel(menu_frame, text="Menú Principal", font=("Times New Roman", 18, "bold")).pack(pady=20)

    # Botón para abrir el análisis léxico
    btn_lexico = CTkButton(
        menu_frame, 
        text="Análisis Léxico", 
        command=lambda: abrirMenuLexico(), 
        corner_radius=10, 
        font=("Times New Roman", 14),
        height=50,
        width=250
    )
    btn_lexico.pack(pady=15)

    # Botón para abrir el análisis sintáctico
    btn_sintactico = CTkButton(
        menu_frame, 
        text="Análisis Sintáctico", 
        command=lambda: abrirMenuSintactico(), 
        corner_radius=10, 
        font=("Times New Roman", 14),
        height=50,
        width=250
    )
    btn_sintactico.pack(pady=15)

    # Botón deshabilitado para análisis semántico
    btn_semantico = CTkButton(
        menu_frame, 
        text="Análisis Semántico (Deshabilitado)", 
        state="disabled", 
        corner_radius=10, 
        font=("Times New Roman", 14),
        height=50,
        width=250
    )
    btn_semantico.pack(pady=15)

    # Botón para música con ícono
    icon_path = "../../imagenes/icon_music.png"
    from PIL import Image  
    music_icon = CTkImage(Image.open(icon_path), size=(20, 20))
    btn_music = CTkButton(
        menu_frame,
        text="",
        image=music_icon,
        compound="left",
        command=lambda: toggle_music(btn_music),
        corner_radius=5,
        font=("Times New Roman", 14),
        height=50,
        width=50
    )
    btn_music.pack(pady=5)

    # Marco para el contenido principal
    content_frame = CTkFrame(raiz, corner_radius=10)
    content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Cargar la imagen de los listados
    listado_image_path = "../../imagenes/portada_gato.png"  # Ruta de la imagen
    listado_image = Image.open(listado_image_path)
    listado_image = listado_image.resize((600, 500))  # Ajustar el tamaño si es necesario
    listado_image = CTkImage(listado_image, size=(600, 500))

    # Crear un label con la imagen y ponerlo a la derecha
    CTkLabel(content_frame, image=listado_image).pack(side="left", padx=10)
    
    CTkLabel(content_frame, text="COMPILADORES", font=("Times New Roman", 24, "bold")).pack(pady=10)

    integrantes = """
Equipo 5:

- Mario Enrique Gallardo
- Christian Josue Campos Lopez
- Yamil
- Ariadna Betsabe Espina Ramirez
- Jose Perez
- Irving Tristan Perez Zurita
    """
    CTkLabel(content_frame, text=integrantes, font=("Times New Roman", 16), justify="left").pack(pady=10)

    raiz.mainloop()

def abrirMenuLexico():
    # Crear ventana de análisis léxico
    menu_lexico = CTkToplevel(raiz)
    menu_lexico.geometry("400x300")
    menu_lexico.title("Opciones de Análisis Léxico")

    CTkLabel(menu_lexico, text="Análisis Léxico", font=("Times New Roman", 16, "bold")).pack(pady=10)

    CTkButton(
        menu_lexico, 
        text="Algoritmo de Thomson (AFND)", 
        command=lambda: Conjuntos(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

    CTkButton(
        menu_lexico, 
        text="Construcción de conjuntos (AFD)", 
        command=lambda: Conjuntos_afn(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

    CTkButton(
        menu_lexico, 
        text="Analizador Léxico", 
        command=lambda: Prueba(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

def abrirMenuSintactico():
    # Crear ventana de análisis sintáctico
    menu_sintactico = CTkToplevel(raiz)
    menu_sintactico.geometry("400x300")
    menu_sintactico.title("Opciones de Análisis Sintáctico")

    CTkLabel(menu_sintactico, text="Análisis Sintáctico", font=("Times New Roman", 16, "bold")).pack(pady=10)

    CTkButton(
        menu_sintactico, 
        text="Primeros y Siguientes", 
        command=lambda: ventanita(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)
    
    CTkButton(
        menu_sintactico, 
        text="Algoritmo de Coleccion Canonica", 
        command=lambda: ventana_coleccion(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)

    CTkButton(
        menu_sintactico, 
        text="Otra opción", 
        command=lambda: bucle(), 
        corner_radius=10,
        font=("Times New Roman", 12)
    ).pack(pady=10)
