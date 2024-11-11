import tkinter as tk
from PIL import Image, ImageTk  # sudo apt-get install python3-pil.imagetk
from ventana import Ventana 

class VentanaImagen(Ventana):
    def __init__(self, ancho=300, alto=250, titulo="Ventana con Imagen"):
        super().__init__(ancho, alto, titulo)  # Llamar al constructor de la clase base Ventana

        # Inicializamos la imagen
        self.imagen_original = None
        self.imagen_escalada = None

        # Etiqueta para mostrar la imagen
        self.etiqueta_imagen = tk.Label(self.root)
        self.etiqueta_imagen.pack(fill=tk.BOTH, expand=True)

        # Escuchar cambios en el tamaño de la ventana
        self.root.bind("<Configure>", self.redimensionar_imagen)

    def cargar_imagen(self, ruta_imagen):
        """
        Cargar la imagen desde el archivo.
        :param ruta_imagen: Ruta del archivo de la imagen (debe ser un formato soportado por Tkinter).
        """
        try:
            # Cargar la imagen usando PIL
            self.imagen_original = Image.open(ruta_imagen)
            print(f"Imagen cargada correctamente desde {ruta_imagen}.")
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def escalar_imagen(self, ancho_nuevo, alto_nuevo):
        """
        Escalar la imagen a las nuevas dimensiones, manteniendo las proporciones.
        :param ancho_nuevo: Nuevo ancho de la imagen.
        :param alto_nuevo: Nuevo alto de la imagen.
        """
        if self.imagen_original:
            try:
                # Mantener las proporciones de la imagen
                ratio = min(ancho_nuevo / self.imagen_original.width, alto_nuevo / self.imagen_original.height)
                ancho_redimensionado = int(self.imagen_original.width * ratio)
                alto_redimensionado = int(self.imagen_original.height * ratio)

                # Redimensionar la imagen
                self.imagen_escalada = self.imagen_original.resize((ancho_redimensionado, alto_redimensionado), Image.ANTIALIAS)
                print(f"Imagen escalada a {ancho_redimensionado}x{alto_redimensionado}.")
            except Exception as e:
                print(f"Error al escalar la imagen: {e}")
        else:
            print("Primero debes cargar la imagen antes de escalarla.")

    def mostrar_imagen(self):
        """
        Mostrar la imagen escalada en la ventana.
        """
        if self.imagen_escalada:
            # Convertir la imagen escalada a un formato que Tkinter pueda manejar
            imagen_tk = ImageTk.PhotoImage(self.imagen_escalada)
            self.etiqueta_imagen.config(image=imagen_tk)
            self.etiqueta_imagen.image = imagen_tk  # Mantener referencia
            print("Imagen mostrada en la ventana.")
        else:
            print("No hay imagen escalada para mostrar.")

    def redimensionar_imagen(self, event):
        """
        Este método se llama cada vez que la ventana cambia de tamaño.
        Se recalcula el tamaño de la imagen para ajustarse al tamaño de la ventana.
        """
        # Obtener las nuevas dimensiones de la ventana
        ancho_ventana = event.width
        alto_ventana = event.height

        # Escalar la imagen en función del tamaño de la ventana
        if self.imagen_original:
            self.escalar_imagen(ancho_ventana, alto_ventana)
            self.mostrar_imagen()

'''
ventana = VentanaImagen(ancho=800, alto=600, titulo="Ventana con Imagen")

# Cargar la imagen
ventana.cargar_imagen("portada.png")

# Mostrar la imagen en la ventana
ventana.mostrar_imagen()

# Ejecutar el bucle principal de la ventana (esperando eventos)
ventana.ejecutar()
'''
