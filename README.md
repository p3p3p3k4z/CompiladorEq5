# Proyecto Compilador
Este proyecto tiene la finalidad implementar en un programa el algoritmo de Thompson, el cual permite obtener un Autómata Finito No Determinista a partir de una expresión regular.

- Thompson (Expresión regular -> AFN) 18 de Octubre

## Ejecutar
```bash
python3 main.pyw
```

## Actualizaciones
- Corrección de Interfaz para LINUX. Comentar la linea de codigo donde se meciona esta configuracion para usuarios windows
- Chechar una posible mejora para la dimension de ventanas, equipo de interfaz
- Implementacion requerida

--- 
## Notas
En el uso de la libreria tkinter
Para llamar inicializar la ventana
```python
#Configuracion para Windows
raiz.state("zoomed")
#Configuracion para Linux
raiz.attributes('-zoomed', True) 
```
En caso de no funcionar descomentar las siguientes lineas de codigo

```python
#raiz.geometry("800x500")
#raiz.geometry(f"{raiz.winfo_screenwidth()}x{raiz.winfo_screenheight()}+0+0")
```
Para la imagen
```
# Cargar la imagen de fondo (solo formatos .png o .gif son soportados por Tkinter)
background_image = PhotoImage(file="portada.png")  # Asegúrate de usar una imagen en formato .png

# Crear un Canvas para poner la imagen de fondo
canvas = Canvas(raiz, width=1500, height=700)
canvas.pack(fill="both", expand=True)

# Colocar la imagen en el Canvas
canvas.create_image(0, 0, image=background_image, anchor="nw")
```

---


**Asignacion y Reporte de Tareas**
<https://drive.google.com/drive/folders/139GimlpaTpR47Wv7oUby-iAOCpY8NWAb?usp=drive_link>

# Suerte en el proyecto 🐧
