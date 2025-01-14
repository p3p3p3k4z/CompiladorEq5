import re
from tkinter import *
from tkinter import filedialog
import subprocess  # Para abrir Notepad++

# Definir patrones para el análisis léxico
patterns = {
    "P_reservada": r'\b(autobreak|case|const|continue|default|enum|extern|goto|include|define|ifdef|ifndef|endif|undef|error|pragma|register|short|signed|sizeof|static|struct|typedef|union|unsigned|volatile|main|printf|scanf|return|switch|do|else|for|if|while|char|void|long|double|int|float|string|break)\b',
    "Biblioteca": r'<\s*[a-zA-Z0-9_]+\.h\s*>',
    "ID": r'\b[a-zA-Z_]\w*\b',
    "Nfloat": r'\b\d*\.\d+([eE][+-]?\d+)?\b|\b\d+\.\d*\b',
    "Nint": r'\b\d+\b',
    "String": r'"([^"\\]*(?:\\.[^"\\]*)*)"',
    "Operadores": r'(\+\+|==|<=|>=|!=|\+=|-=|\+|\-|\*|\/|<|>|%|&&|\|\||=|#|&|:)',  # ++ primero
    "Puntuacion": r'[;{}\[\](),.]',
    "Saltos": r'\s+',
    "VariablesLocales": r'\b(int|float|double|char|long|short)\s+([a-zA-Z_]\w*(?:\s*\[\s*\d*\s*\])?\s*(?:=\s*[^,;]*)?\s*(?:,|;|\n))*',  # Variables locales
    "Constantes": r'#define\s+[a-zA-Z_]\w*\s+[^;]+',  # Constantes globales
}

regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns.items())
compiled_regex = re.compile(regex, re.MULTILINE | re.DOTALL)

def quitar_comentarios(code):
    # Reemplazar comentarios multilínea /* ... */ con la misma cantidad de saltos de línea
    code = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), code, flags=re.MULTILINE | re.DOTALL)
    # Eliminar comentarios de una línea // sin agregar saltos de línea adicionales
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    return code


# Nueva función para procesar variables
def procesar_variables(declaracion):
    variables = []
    # Dividir por comas para manejar múltiples variables
    partes = re.split(r'\s*,\s*', declaracion)
    
    for parte in partes:
        # Limpiar la parte
        parte = parte.strip()
        if not parte:
            continue
            
        # Extraer nombre base sin inicialización
        nombre = re.split(r'\s*=\s*', parte)[0]
        
        # Limpiar punteros y arrays
        nombre = re.sub(r'\s*\[\s*\d*\s*\]', '', nombre)
        nombre = nombre.replace('*', '').strip()
        
        if nombre and nombre.isidentifier():
            variables.append(nombre)
            
    return variables

# Expresión regular para variables
variable_pattern = re.compile(r'\b(int|float|double|char|short|long|void|struct|unsigned)\s*((?:\*?\s*[a-zA-Z_]\w*(?:\s*\[\s*\d*\s*\])?(?:\s*=\s*[^,;]*)?(?:\s*,\s*)?)+)\s*;')

def analizador_sintactico(code):
    tokens = []
    errores = []
    variables = {}

    code_tokens = quitar_comentarios(code)
    code_vars = quitar_comentarios(code)
    code_vars = re.sub(r'(?:printf|scanf)\s*\([^)]*\)|"[^"]*"|#include\s*<[^>]*>', '', code_vars)
    ultimo_token = 0
    linea_actual = 1

    # Filtrar las palabras reservadas para no mostrarlas
    palabras_reservadas = set([
        "auto", "break", "case", "char", "const", "continue", "default", "do", 
        "double", "else", "enum", "extern", "float", "for", "goto", "if", 
        "int", "long", "register", "return", "short", "signed", "sizeof", 
        "static", "struct", "switch", "typedef", "union", "unsigned", "void",
        "volatile", "while", "main", "printf", "scanf"
        # Directivas de preprocesador
        "include", "define", "ifdef", "ifndef", "endif"
    ])

# Procesar tokens
    for match in compiled_regex.finditer(code_tokens):
        start, end = match.span()
        
        if ultimo_token < start:
            error_texto = code_tokens[ultimo_token:start]
            lineas_entre_tokens = error_texto.count('\n')
            
            if error_texto.strip():
                errores.append((linea_actual, error_texto.strip()))
                
            linea_actual += lineas_entre_tokens
        
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        
        linea_actual += code_tokens[ultimo_token:end].count('\n')        
        if tipo_token == "Saltos":
            ultimo_token = end
            continue
        
        if tipo_token == "Nint":
            tipo_token = "Nint"  # Mantener Nint como tipo
        elif tipo_token == "Nfloat":
            tipo_token = "Nfloat"  # Mantener Nfloat como tipo
        elif tipo_token not in ["ID", "String"]:
            tipo_token = valor_token
        
        tokens.append((linea_actual, valor_token, tipo_token))
        ultimo_token = end

    # Buscar declaraciones de variables
    for var_match in variable_pattern.finditer(code_vars):
        tipo_var = var_match.group(1)
        declaraciones = var_match.group(2)
        
        if declaraciones:
            vars_encontradas = procesar_variables(declaraciones)
            for var_name in vars_encontradas:
                if (var_name and 
                    var_name not in variables and 
                    var_name.isidentifier() and 
                    var_name not in palabras_reservadas):
                    variables[var_name] = tipo_var

    # Buscar variables usadas en el código
    used_vars = re.finditer(r'\b[a-zA-Z_]\w*\b', code_vars)
    for match in used_vars:
        var_name = match.group()
        if var_name.isidentifier() and var_name not in variables:
            variables[var_name] = 'unknown'

    # Filtrar las variables locales, excluyendo las palabras reservadas
    variables_locales = [var_name for var_name in variables if var_name not in palabras_reservadas]

    # Filtrar los tokens antes de imprimir
    #tokens_filtrados = [token for token in tokens if 'printf' not in token[1]]

    # Filtrar los errores que no contienen printf
    #errores_filtrados = [(error_linea, error_texto) for error_linea, error_texto in errores if 'printf' not in error_texto]

    return tokens, errores, variables_locales


def abrirArchivo(alphaEntry, erEntry, lexWindow, output_text, error_text, symbol_text):
    lexWindow.grab_set()
    alphaEntry.delete(0, END)
    erEntry.delete(0, END)
    output_text.delete(1.0, END)
    error_text.delete(1.0, END)
    symbol_text.delete(1.0, END)
    
    direccionArchivo = filedialog.askopenfilename(
        initialdir=r"../../codigos_fuentes",
        title="Abrir",
        filetypes=(("texto", "*.txt"),)
    )
    
    if direccionArchivo:  # Si se selecciona un archivo
        try:
            with open(direccionArchivo, 'r') as archivo:
                code = archivo.read()
                erEntry.insert(END, code)
                
                # Ejecutar el análisis léxico en el contenido del archivo
                tokens, errores, variables = analizador_sintactico(code)
                
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
            
                # Mostrar solo los nombres de las variables en la Tabla de símbolos
                symbol_text.insert(END, "#Id        Nombre del identificador:\n")
                symbol_text.insert(END, "-" * 40 + "\n")
                
                for idx, var_name in enumerate(variables, start=1):
                    symbol_text.insert(END, f"{idx:<10}{var_name}\n")
            
            # Abrir el archivo en Notepad++ sin bloquear la ejecución del programa
            subprocess.Popen([r"C:\Program Files\Notepad++\notepad++.exe", direccionArchivo])
        
        except FileNotFoundError:
            output_text.insert(END, "Error: Notepad++ no está instalado o no se encuentra en la ruta especificada.\n")
        except Exception as e:
            output_text.insert(END, f"Error al abrir el archivo: {e}\n")

def Prueba():
    font1 = ("Times New Roman", 12)
    lexWindow = Toplevel()
    try:
        lexWindow.state("zoomed")
    except:
        lexWindow.attributes('-zoomed', True)
        
    lexWindow.title("Automata finito determinista")
    lexWindow.config(bg="#B5FFFF")
    
    archivoL = Label(lexWindow, text="Ingresa una prueba", width=20, bg="#FFB3C6", font=font1)
    archivoL.place(x=20, y=50)

    archivoButton = Button(lexWindow, text="Inspeccionar", width=26, 
                           command=lambda: abrirArchivo(alphaEntry, erEntry, lexWindow, output_text, error_text, symbol_text), 
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
#root = Tk()
#root.title("Analizador Léxico")
#Button(root, text="Abrir Prueba", command=Prueba).pack()
#root.mainloop()