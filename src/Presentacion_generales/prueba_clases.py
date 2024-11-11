from ventana import VentanaBase
from boton import Boton

# Crear la ventana principal
ventana = Ventana(ancho=400, alto=300, titulo="Ventana con Botones")

# Crear instancias de la clase Boton
iniciar_button = Boton(ventana.root, text="Iniciar")
archivo_button = Boton(ventana.root, text="Abrir Archivo")
clean_button = Boton(ventana.root, text="Limpiar")

# Agregar los botones a la ventana en posiciones específicas
ventana.agregar_boton(iniciar_button, 0, 1)
ventana.agregar_boton(archivo_button, 1, 0)
ventana.agregar_boton(clean_button, 2, 2)

# Cambiar tamaño de los botones
iniciar_button.cambiar_tamano(30, 2)
archivo_button.cambiar_tamano(15, 2)
clean_button.cambiar_tamano(12, 2)

# Cambiar colores de los botones
iniciar_button.cambiar_colores(bg_color="lightblue", fg_color="black")
archivo_button.cambiar_colores(bg_color="lightgreen", fg_color="black")
clean_button.cambiar_colores(bg_color="lightcoral", fg_color="white")

# Deshabilitar los botones "Abrir Archivo" y "Limpiar" inicialmente
archivo_button.deshabilitar()
clean_button.deshabilitar()

# Función para habilitar todos los botones al presionar el botón "Iniciar"
def iniciar_proceso():
    ventana.habilitar_botones()
    print("El proceso ha comenzado. Los botones están habilitados.")
    abrir_nueva_ventana_button.habilitar()  # Habilita el botón para abrir nueva ventana

# Función para abrir una nueva ventana
def abrir_ventana_nueva():
    # Crear una nueva instancia de la clase Ventana
    nueva_ventana = Ventana(ancho=300, alto=200, titulo="Nueva Ventana")
    
    # Crear un botón en la nueva ventana
    nuevo_boton = Boton(nueva_ventana.root, text="Cerrar", command=nueva_ventana.root.quit)
    nueva_ventana.agregar_boton(nuevo_boton, 1, 1)
    
    # Ejecutar la nueva ventana
    nueva_ventana.ejecutar()

# Asignar el comando al botón "Iniciar"
iniciar_button.boton.config(command=iniciar_proceso)#aqui metes la funcion

# Crear un nuevo botón "Abrir Nueva Ventana" deshabilitado inicialmente
abrir_nueva_ventana_button = Boton(ventana.root, text="Abrir Nueva Ventana", command=abrir_ventana_nueva)
abrir_nueva_ventana_button.deshabilitar()  # Deshabilitado inicialmente
ventana.agregar_boton(abrir_nueva_ventana_button, 3, 1)

# Ejecutar la ventana principal
ventana.ejecutar()
