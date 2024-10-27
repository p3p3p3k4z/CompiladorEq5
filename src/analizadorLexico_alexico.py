import re

from analizadorLexico_Thompson import *

# Función para generar el alfabeto a partir de las líneas del archivo
def generar_alfabeto(lineas):
    alfabeto = set()
    for linea in lineas:
        # Buscamos las líneas que comienzan con "alfabetoX:"
        match = re.match(r'^alfabeto(\d+): (.+)$', linea)
        if match:
            numero_alfabeto = match.group(1)
            contenido = match.group(2)
            # Si contiene "letras", agregamos todas las letras del alfabeto
            if contenido == 'letras':
                alfabeto.update('l')
               #alfabeto.update(set(chr(i) for i in range(65, 91)))
               #alfabeto.update(set(chr(i) for i in range(97, 123)))
            # Si contiene "digitos", agregamos los dígitos del 0 al 9
            elif contenido == 'digitos':
                #alfabeto.update(set(str(i) for i in range(10)))
                alfabeto.update('d')
            # De lo contrario, agregamos las letras únicas
            else:
                alfabeto.update(set(contenido))
    return sorted(alfabeto)

# Función para obtener la expresión regular
def obtener_expresion(lineas):
    for linea in lineas:
        if linea.startswith("expresion:"):
           #expresion = re.sub(r'^expresion: (.+)$', r'\1', linea)
           #expresion = expresion.Remplazar('digitos','(0|1|2|3|4|5|6|7|8|9)')
           #expresion = expresion.Remplazar('letras','(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|ñ|o|p|q|r|s|t|u|v|w|x|y|z)')
           #return expresion
            return re.sub(r'^expresion: (.+)$', r'\1', linea)


#Funciones para ver el procesamiento que se le dará a la exp regular
def expresion_postfija(expresion):
    def precedencia(op):
        precedencias = {'|': 1, '.': 2, '*': 3, '+': 4, '?':5}
        return precedencias.get(op, 0)

    def a_postfija(expresion):
        pila_operadores = []
        salida = []
        i = 0

        while i < len(expresion):
            token = expresion[i]

            if token.isalnum():
                salida.append(token)
            elif token == '(':
                pila_operadores.append(token)
            elif token == ')':
                while pila_operadores and pila_operadores[-1] != '(':
                    salida.append(pila_operadores.pop())
                pila_operadores.pop()
            else:
                while pila_operadores and precedencia(token) <= precedencia(pila_operadores[-1]):
                    salida.append(pila_operadores.pop())
                pila_operadores.append(token)
            i += 1

        while pila_operadores:
            salida.append(pila_operadores.pop())

        return ''.join(salida)

    return a_postfija(expresion)


def evaluar_expresion_postfija(expresion_postfija):
    pila = []
    Automata = LinkedList()
    
    for token in expresion_postfija:
        if token.isalnum():
            pila.append(token)
            
        elif token == '?':
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
                
            Automata = Cerradura_Opcional(operand1)
            pila.append(Automata)
            
        elif token == '*':
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
                
            Automata = Cerradura_de_Kleene(operand1)
            pila.append(Automata)
            
        elif token == '+':
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
                
            Automata = Cerradura_Positiva(operand1)
            pila.append(Automata)
            
        elif token == '.':
            operand2 = pila.pop()
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
            if type(operand2) != LinkedList:
                operand2 = SingleLetter(str(operand2))
            Automata = Concatenation(operand1,operand2)
            pila.append(Automata)
            
        elif token == '|':
            operand2 = pila.pop()
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
                
            if type(operand2) != LinkedList:
                operand2 = SingleLetter(str(operand2))
            
            Automata = Union(operand1,operand2)
            pila.append(Automata)
            
    # El resultado final debe estar en la cima de la pila
    return pila.pop()

'''
_______________________________________________________________________________________________________

Script para probar el procesamiento de expresiones regulares

_______________________________________________________________________________________________________
'''

#Comentario


#nombre_archivo = 'expresiones.txt'
## Leer el archivo de entrada
#archivo_entrada = nombre_archivo
#with open(archivo_entrada, 'r') as f:
#    lineas = f.readlines()
#
## Generar el alfabeto
#alfabeto = generar_alfabeto(lineas)
#
#
## Eliminar repeticiones en el alfabeto
#alfabeto = sorted(set(alfabeto))
#
## Obtener la expresión regular
#expresion_regular = obtener_expresion(lineas)
#expresion_postfija = expresion_postfija(expresion_regular)
#
#
#expresion_postfija = expresion_postfija.Remplazar('digitos','d')
#expresion_postfija = expresion_postfija.Remplazar('letras','l')
#Automata = evaluar_expresion_postfija(expresion_postfija)
#
#
##Imprimir resultados
#print("Expresión regular:", expresion_regular)
#print("Expresión regular en forma postfija:", expresion_postfija)
#
#
#Automata.display()
