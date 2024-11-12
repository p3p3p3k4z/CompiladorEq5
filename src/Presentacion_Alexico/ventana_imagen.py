from tkinter import Label
from PIL import Image, ImageTk
from ventana import Ventana

class VentanaImagen(Ventana):
    def __init__(self, ancho=300, alto=250, titulo="Ventana con Imagen", color_fondo="white"):
        super().__init__(ancho, alto, titulo)
        self.color_fondo = color_fondo
        self.root.config(bg=self.color_fondo)

        # Inicializamos la imagen
        self.imagen_original = None
        self.imagen_escalada = None

        # Etiqueta para mostrar la imagen
        self.etiqueta_imagen = Label(self.root)
        self.etiqueta_imagen.pack(fill="both", expand=True)

        # Escuchar cambios en el tamaño de la ventana
        self.root.bind("<Configure>", self.redimensionar_imagen)

    def cargar_imagen(self, ruta_imagen):
        """Cargar la imagen desde el archivo."""
        try:
            self.imagen_original = Image.open(ruta_imagen)
            print(f"Imagen cargada correctamente desde {ruta_imagen}.")
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def escalar_imagen(self, ancho_nuevo, alto_nuevo):
        if self.imagen_original:
            try:
                # Mantener las proporciones de la imagen
                ratio = min(ancho_nuevo / self.imagen_original.width, alto_nuevo / self.imagen_original.height)
                ancho_redimensionado = int(self.imagen_original.width * ratio)
                alto_redimensionado = int(self.imagen_original.height * ratio)

                # Intentamos usar Image.LANCZOS (para versiones recientes de Pillow)
                try:
                    self.imagen_escalada = self.imagen_original.resize(
                        (ancho_redimensionado, alto_redimensionado), Image.LANCZOS
                    )
                    print(f"Imagen escalada a {ancho_redimensionado}x{alto_redimensionado} usando LANCZOS.")
                except AttributeError:
                    # Si Image.LANCZOS no está disponible, usamos Image.ANTIALIAS para versiones antiguas de Pillow
                    self.imagen_escalada = self.imagen_original.resize(
                        (ancho_redimensionado, alto_redimensionado), Image.ANTIALIAS
                    )
                    print(f"Imagen escalada a {ancho_redimensionado}x{alto_redimensionado} usando ANTIALIAS.")
            except Exception as e:
                print(f"Error al escalar la imagen: {e}")
        else:
            print("Primero debes cargar la imagen antes de escalarla.")

    def mostrar_imagen(self):
        """Mostrar la imagen escalada en la ventana."""
        if self.imagen_escalada:
            imagen_tk = ImageTk.PhotoImage(self.imagen_escalada)
            self.etiqueta_imagen.config(image=imagen_tk)
            self.etiqueta_imagen.image = imagen_tk
            print("Imagen mostrada en la ventana.")
        else:
            print("No hay imagen escalada para mostrar.")

    def redimensionar_imagen(self, event):
        """Redimensiona la imagen al cambiar el tamaño de la ventana."""
        ancho_ventana = event.width
        alto_ventana = event.height
        if self.imagen_original:
            self.escalar_imagen(ancho_ventana, alto_ventana)
            self.mostrar_imagen()

