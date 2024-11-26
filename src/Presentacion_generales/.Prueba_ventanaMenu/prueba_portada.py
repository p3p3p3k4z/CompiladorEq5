from tkinter import Tk, Label, Menu
from PIL import Image, ImageTk

class Ventana:
    def __init__(self, ancho=300, alto=250, titulo="Ventana"):
        self.root = Tk()
        self.root.geometry(f"{ancho}x{alto}")
        self.root.title(titulo)

    def ejecutar(self):
        self.root.mainloop()

class VentanaImagen(Ventana):
    def __init__(self, ancho=300, alto=250, titulo="Ventana con Imagen", color_fondo="white"):
        super().__init__(ancho, alto, titulo)  # Llamar al constructor de la clase base Ventana
        self.color_fondo = color_fondo  # Almacenar color_fondo

        # Configurar fondo de la ventana
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
                self.imagen_escalada = self.imagen_original.resize((ancho_redimensionado, alto_redimensionado), Image.LANCZOS)
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

if __name__ == "__main__":
    def Conjuntos():
        print("Ejecutando Conjuntos")

    def Conjuntos_afn():
        print("Ejecutando Conjuntos AFN")

    def abrir():
        print("Ejecutando abrir")

    # Crear instancia de MenuVentana
    ventana_con_menu = MenuVentana(ancho=850, alto=650, titulo="Pecera con Menú", color_fondo="cyan")
    ventana_con_menu.cargar_imagen("portada.png")

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
