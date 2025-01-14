import re
from tkinter import *
from tkinter import filedialog

# Definir patrones para el análisis léxico
patterns = {
    "P_reservada": r'\b(autobreak|case|const|continue|default|enum|extern|goto|include|define|ifdef|ifndef|endif|undef|error|pragma|register|short|signed|sizeof|static|struct|typedef|union|unsigned|volatile|main|printf|scanf|return|switch|do|else|for|if|while|char|void|long|double|int|float|string)\b',
    "Biblioteca": r'<\s*[a-zA-Z0-9_]+\.h\s*>',
    "ID": r'\b[a-zA-Z_]\w*\b',
    "Nfloat": r'\b\d*\.\d+([eE][+-]?\d+)?\b|\b\d+\.\d*\b',
    "Nint": r'\b\d+\b',
    "String": r'"([^"\\]*(?:\\.[^"\\]*)*)"',
    "Operadores": r'(\+|\-|\*|\/|<|>|\+=|-=|==|%|!=|<=|>=|&&|\|\||=|#|&|:)',
    "Puntuacion": r'[;{}\[\](),.]',
    "Saltos": r'\s+',
}

regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns.items())
compiled_regex = re.compile(regex, re.MULTILINE | re.DOTALL)

def quitar_comentarios(code):
    # Elimina comentarios de línea y de bloque
    code = re.sub(r'//.*?$|/\*.*?\*/', '', code, flags=re.MULTILINE | re.DOTALL)
    return code

def analizador_lex(code):
    tokens = []
    errores = []
    variables = {}  # Diccionario para almacenar las variables y sus valores

    code = quitar_comentarios(code)  # Elimina los comentarios antes de analizar
    ultimo_token = 0
    linea_actual = 1

    variable_pattern = re.compile(r'\b([a-zA-Z_]\w*)\s*=\s*([0-9\.\-]+|".*?")\s*(;|\n|\s)*')  # Expresión regular para detectar asignaciones

    for match in compiled_regex.finditer(code):
        start, end = match.span()
        
        # Revisar si hay algún error entre tokens y registrar el número de línea correspondiente
        if ultimo_token < start:
            error_texto = code[ultimo_token:start]
            lineas_entre_tokens = error_texto.count('\n')
            
            if error_texto.strip():  # Solo agregar si hay texto no vacío
                errores.append((linea_actual, error_texto.strip()))
                
            linea_actual += lineas_entre_tokens
        
        # Obtener tipo y valor del token
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        
        # Actualizar la línea actual según el número de saltos de línea en el token actual
        linea_actual += code[ultimo_token:end].count('\n')
        
        if tipo_token == "Saltos":
            ultimo_token = end
            continue
        
        if tipo_token not in ["ID", "String"]:
            tipo_token = valor_token
        
        tokens.append((linea_actual, valor_token, tipo_token))
        ultimo_token = end

    # Buscar asignaciones de variables en todo el código
    for var_match in variable_pattern.finditer(code):
        var_name = var_match.group(1).strip()
        var_value = var_match.group(2).strip()
        variables[var_name] = var_value  # Almacenar el último valor asignado a la variable

    # Si hay texto restante después del último token, también se marca como error
    if ultimo_token < len(code):
        error_texto = code[ultimo_token:]
        if error_texto.strip():  # Solo agrega si hay texto no vacío
            errores.append((linea_actual, error_texto.strip()))
    
    return tokens, errores, variables

def abrirArchivo(alphaEntry, erEntry, lexWindow, output_text, error_text, symbol_text):
    lexWindow.grab_set()
    alphaEntry.delete(0, END)
    erEntry.delete(0, END)
    output_text.delete(1.0, END)
    error_text.delete(1.0, END)
    symbol_text.delete(1.0, END)
    
    direccionArchivo = filedialog.askopenfilename(
        initialdir=r"D:\Sistemas\Proyect_Comp_Java\Proyecto_compilador\Pruebas_expresiones_reg",
        title="Abrir",
        filetypes=(("texto", "*.txt"),)
    )
    
    try:
        with open(direccionArchivo, 'r') as archivo:
            code = archivo.read()
            erEntry.insert(END, code)
           
            # Ejecutar el análisis léxico en el contenido del archivo 
            tokens, errores, variables = analizador_lex(code)
            
            # Encabezado para la salida del análisis léxico
            output_text.insert(END, f"{'# Línea':<10}{'Lexema':<20}{'-->':<5}{'Token':<10}\n")
            output_text.insert(END, "-" * 50 + "\n")
            
            for token in tokens:
                output_text.insert(END, f"# Línea {token[0]:<3}  {token[1]:<15} -->  {token[2]:<10}\n")
           
            # Encabezado para la salida de errores 
            error_text.insert(END, "# Línea       Descripción\n")
            error_text.insert(END, "-" * 40 + "\n")
            
            for error_linea, error_texto in errores:
                error_text.insert(END, f"# Línea {error_linea:<3}   Error: {error_texto}\n")
    
            # Mostrar variables y sus valores con ID numerado
            symbol_text.insert(END, "#Id        Valor:\n")
            symbol_text.insert(END, "-" * 40 + "\n")
            for idx, (var_name, var_value) in enumerate(variables.items(), start=1):
                symbol_text.insert(END, f"{idx:<10}{var_name}={var_value}\n")

    except Exception as e:
        output_text.insert(END, f"Error al abrir el archivo: {e}\n")

def Prueba():
    font1 = ("Times New Roman", 12)
    lexWindow = Toplevel()
    lexWindow.state("zoomed")
    lexWindow.title("Automata finito determinista")
    lexWindow.config(bg="#B5FFFF")
    
    archivoL = Label(lexWindow, text="Ingresa una expresion", width=20, bg="#FFB3C6", font=font1)
    archivoL.place(x=20, y=50)

    archivoButton = Button(lexWindow, text="Inspeccionar", width=26, 
                           command=lambda: (abrirArchivo(alphaEntry, erEntry, lexWindow, output_text, error_text, symbol_text)), 
                           bg="#FFB3C6", font=font1)
    archivoButton.place(x=210, y=47)
    archivoButton.config(bd="10", relief="raised")
    
    eregularL = Label(lexWindow, text="Expresión regular:", font=font1, width=20, bg="#FFB3C6")
    eregularL.place(x=20, y=100)

    erEntry = Entry(lexWindow, width=30, font=font1, bg="#FFB3C6")
    erEntry.place(x=210, y=101)

    alphaLabel = Label(lexWindow, text="Alfabeto", font=font1, width=20, bg="#FFB3C6")
    alphaLabel.place(x=20, y=150)

    alphaEntry = Entry(lexWindow, font=font1, width=30, bg="#FFB3C6")
    alphaEntry.place(x=210, y=151)

    # Cuadro de texto para la salida del análisis léxico con su scrollbar
    output_text = Text(lexWindow, wrap=WORD, width=60, height=15, bg="#FFFFFF", font=("Consolas", 10))
    output_text.place(x=20, y=220)
    output_text.insert(END, "Resultados del análisis léxico:\n")

    scrollbar_output = Scrollbar(lexWindow, command=output_text.yview)
    scrollbar_output.place(x=440, y=220, height=245)
    output_text.config(yscrollcommand=scrollbar_output.set)

    # Cuadro de texto para los errores de análisis con su scrollbar
    error_text = Text(lexWindow, wrap=WORD, width=40, height=15, bg="#FFCCCC", font=("Consolas", 10))
    error_text.place(x=500, y=220)
    error_text.insert(END, "Errores:\n")

    scrollbar_error = Scrollbar(lexWindow, command=error_text.yview)
    scrollbar_error.place(x=780, y=220, height=245)
    error_text.config(yscrollcommand=scrollbar_error.set)
    
     # Cuadro de texto para los símbolos con su scrollbar
    symbol_text = Text(lexWindow, wrap=WORD, width=40, height=15, bg="#E6FFCC", font=("Consolas", 10))
    symbol_text.place(x=840, y=220)
    symbol_text.insert(END, "Tabla de simbolos:\n")
    
    scrollbar_symbol = Scrollbar(lexWindow, command=symbol_text.yview)
    scrollbar_symbol.place(x=1120, y=220, height=245)
    symbol_text.config(yscrollcommand=scrollbar_symbol.set)


# Ejecución de la ventana principal
root = Tk()
root.title("Analizador Léxico")
Button(root, text="Abrir Prueba", command=Prueba).pack()
root.mainloop()
 