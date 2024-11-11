from ventana import Ventana
from boton import Boton

# Crear la ventana
ventana = Ventana(ancho=400, alto=300, titulo="Ventana con Botones")

# Crear instancias de la clase Boton
iniciar_button = Boton(ventana.root, text="Iniciar")
archivo_button = Boton(ventana.root, text="Abrir Archivo")
clean_button = Boton(ventana.root, text="Limpiar")

# Agregar los botones a la ventana en posiciones específicas
ventana.agregar_boton(iniciar_button, 50, 50)
ventana.agregar_boton(archivo_button, 150, 50)
ventana.agregar_boton(clean_button, 100, 100)

# Cambiar tamaño de los botones
iniciar_button.cambiar_tamano(10, 2)
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

def abrir_ventana_nueva():
    # Crear una nueva instancia de la clase Ventana
    nueva_ventana = Ventana(ancho=300, alto=200, titulo="Nueva Ventana")
    
    # Crear un botón en la nueva ventana
    nuevo_boton = Boton(nueva_ventana.root, text="Cerrar", command=nueva_ventana.root.quit)
    nueva_ventana.agregar_boton(nuevo_boton, 50, 50)
    
    # Ejecutar la nueva ventana
    nueva_ventana.ejecutar()

# Cambiar comando del botón "Iniciar"
iniciar_button.boton.config(command=iniciar_proceso)
iniciar_button = Boton(ventana.root, text="Abrir Nueva Ventana", command=abrir_ventana_nueva)
ventana.agregar_boton(iniciar_button, 90, 170)

# Ejecutar la ventana
ventana.ejecutar()
