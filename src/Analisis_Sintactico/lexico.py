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