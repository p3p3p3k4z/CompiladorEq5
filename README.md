# Proyecto Compilador
Este proyecto tiene la finalidad implementar en un programa el algoritmo de Thompson, el cual permite obtener un Autómata Finito No Determinista a partir de una expresión regular.

- Thompson (Expresión regular -> AFN) 18 de Octubre
- Construcción de conjuntos (AFN -> AFD) 25 de Octubre

##CORRECIONES
- La tabla no muestra correctamente los estados epsilon
- Verficar que la tabla gene re correcto diagrama de estados

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

## Actualizaciones
- Corrección de Interfaz para LINUX. Comentar la linea de codigo donde se meciona esta configuracion para usuarios windows
- Chechar una posible mejora para la dimension de ventanas, equipo de interfaz

**Asignacion y Reporte de Tareas**
<https://drive.google.com/drive/folders/139GimlpaTpR47Wv7oUby-iAOCpY8NWAb?usp=drive_link>

# Suerte en el proyecto 🐧

---
## Minitutorial de Github
Github es una herramienta que nos permite la documentación y control de versiones del código

#### Obtén el repositorio
Esto nos ayuda a obtener todo el repositorio en nuestra PC personal y poder tener acceso al código
```bash
git clone https://github.com/p3p3p3k4z/Compilador.git
```
#### Crea tu Primer Commit
Esto te ayudara a poder subir tus cambios o tu código a github. Recuerda hacer esto en la carpeta donde esta tu espacio de trabajo

**1.Inicia Git**
```bash
git init
```

**2.Añadir archivos**
Añade todos los archivos de tu espacio de trabajo
```bash
git add .
```
Añade un archivo
```bash
git add main.py
```
Añade una carpeta
```bash
git add carpeta/
```

**3.Hacer tu commit**
Aquí darás un breve mensaje que fue lo que cambiaste
```bash
git commit -m "archivos corregidos"
```

**4.Añadir el repositorio**
```bash
git remote add origin https://github.com/p3p3p3k4z/Compilador.git
```

**5.Subir tus cambios**
```bash
git push -u origin main
```
En caso de Fallas
```bash
git push -u origin main --force
```

A continuación te pedirá tu usuario, después tu contraseña o llave.
Felicidades!!! Ya sabes usar github

#### Hacer cambios
```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

#### Recibir cambios
Cuando alguien actualiza su codigo es necesario recibir el codigo mas actualizado
```bash
git pull origin main
```

---

## Herramientas recomendadas
Estas son herramientas que recomiendo usar, aunque no es necesario usarlas.
#### IDE
**Thonny**
Este es un ide enfocado en python, el cual tiene distintas funcionalidades. Ademas de la integración de librerías comunes, asi como poder añadir cualquier otra de forma facil.

```bash
sudo apt install thonny
```
**Geany**
Este es un ide general y de bajos recursos. Ideal para cualquier lenguaje de programación 
```bash
sudo apt install geany
```

#### Notas y Documentación
**Obsidian**
Permite la creación de notas en formatos .md
Ideal para notas y documentación
<https://obsidian.md/download>

Te recomiendo descargar el paquete .deb (linux)
Para instalarlo
```bash
sudo dpkg -i [archivo.deb]
```

---
## Linux
Como pueden notar la mayoría de las cosas que he comentado en este archivo van enfocado en Linux.
Como RECOMENDACIÓN sugiero usar linux, aunque no importa el entorno de trabajo que uses. Pero tarde que temprano terminaras usando. Hay miles de rezones para integrarte a este mundo.

Te invito a comenzar a usar Linux !!!

**Distribuciones Recomendadas**
- Linux Mint
- Ubuntu 20
- Xubuntu

Si necesitas ayuda, orientación o quieres instalar linux en tu PC. Puedes pedirme ayuda, estaré encantado de poder ayudarte ^^

**¿Ya tienes Linux?**
Muy bien. Te dejo una pagina personal donde podrás conocer mas comando o información:
<https://www.notion.so/fr4km3nt4d0/Linux-0c507a98dc2b49fcb6d77d4ebab3b20e?pvs=4>

¿No sabes como configurar tu sistema? Te dejo un script hecho por mi para configurar tu sistema semi-automaticamente:
<https://github.com/p3p3p3k4z/script_Debian.git>

![linux](https://www.fondos12.com/data/big/6/linux-vs-windows-6426-1920x1200__wallpaper_480x300.jpg)

