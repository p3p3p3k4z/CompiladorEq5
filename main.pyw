from tkinter import ttk
from Procesamiento import *
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
raiz = Tk()
#raiz.geometry("1500x300")
#raiz.geometry(f"{raiz.winfo_screenwidth()}x{raiz.winfo_screenheight()}+0+0")
raiz.config(background="dark turquoise")
raiz.geometry("800x500") 
raiz.title("Compilador Team 5")

# Cargar la imagen de fondo (solo formatos .png o .gif son soportados por Tkinter)
background_image = PhotoImage(file="portada.png")  # Asegúrate de usar una imagen en formato .png

# Crear un Canvas para poner la imagen de fondo
canvas = Canvas(raiz, width=1500, height=700)
canvas.pack(fill="both", expand=True)

# Colocar la imagen en el Canvas
canvas.create_image(0, 0, image=background_image, anchor="nw")

def abrir():
    fichero=filedialog.askopenfilename(title="Abrir", initialdir="D:", filetypes=(("ficheros de texto","*.txt"),("ficheros de python","*.py")))
    #filetypes nos ayuda a hacer una busqueda seleccionada entre los tipos de archivos
def mensaje():
    valor = messagebox.askquestion("AFND", "Estamos trabajando, desea salir!?")
    #con askquestion nos muestra un si y no, con askokcancel muestra ok y cancelar regresa valores booleanos
    #askretrycancel muestra reintentar y cancelar 
    if valor == "yes":
        raiz.destroy()
def bucle():
    valor=messagebox.askretrycancel("Pendiente", "Aun no esta listo")
    while valor == TRUE :
        valor=messagebox.askretrycancel("Pendiente", "Que aun no esta listo dije")

menuop = Menu(raiz)
raiz.config(menu=menuop)

font1=("Times New Roman",10)

opc = Menu(menuop, tearoff=0)#tearoff=0 hace que desaparesca la lagrima es decir una linea que aparece
opc.add_command(label="calcular", command=lambda:Conjuntos(),font=font1)

opc2 = Menu(menuop, tearoff=0)
opc2.add_command(label="Calcular", command=bucle, font=font1)

opc3 = Menu(menuop, tearoff=0,font=font1)
opc3.add_command(label="Abrir", command=abrir)

menuop.add_cascade(label="AFND", menu=opc)#con esto decimos cual sera el nombre de lo de arriba del menu
menuop.add_cascade(label="AFD", menu=opc2)
menuop.add_cascade(label="SEARCH", menu=opc3)
raiz.mainloop()
