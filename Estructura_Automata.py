#define la clase trasicion
class Transition:
    
    def __init__(self, sy = None, st = None):
        symbol = ""
        next_state = -1
        
    def __init__(self, sy, st):
        self.symbol = sy
        self.next_state = st
    
    def getSymbol(self):
        return self.symbol
    
    def getState(self):
        return self.next_state
    
    def setSymbol(self, sy):
        self.symbol = sy
    
    def setState(self, st):
        self.next_state = st
        
    def __str__(self):
        #return "Symbol: " + self.symbol + " Next State: " + str(self.next_state)+ "\n"
        return str(self.next_state) 
    
#Creacion de la clase estado
class State:
    def __init__(self, i, transition, ini, fin):
        self.id = i #Id es el numero de estado
        self.l_transitions = []
        if transition != None:
            self.l_transitions = [transition] #Lista de 
        self.initial_state = ini
        self.final_state = fin
    
    def getIniState(self):
        return self.initial_state
    
    def getFinalState(self):
        return self.final_state
    
    def getTransitions(self):
        return self.l_transitions
    
    def getId(self):
        return self.id
    
    def setIniState(self, i):
        self.initial_state = i
    
    def setFinalState(self, f):
        self.final_state = f
    
    def setId(self, i):
        self.id = i
        
    def addTransition(self, t):
        if (self.getTransitions() == None):
            self.l_transitions = []
        self.l_transitions.append(t)
    
    def displayTransitions(self):
        i = 0
        NTransitions = len(self.l_transitions)
        for s in self.l_transitions:
            if (self.l_transitions[i] != None and i < NTransitions):
                print("To State: " + str(self.l_transitions[i].getState()) + " with Symbol: " + self.l_transitions[i].getSymbol())
                i+=1
    
    def __str__(self):
        #return "Id: " + str(self.id) + " | Initial State: " + str(self.initial_state) + " | Final State: " + str(self.final_state) + "\n"
        cadena = ""
        longitud = len(self.getTransitions())
        i = 1 
        
        for t in self.getTransitions():
            if i!=longitud:
                cadena1 = str(t) + " ," 
            else:
                cadena1 = str(t)
            cadena=cadena+cadena1
            i+=1
        #print(cadena)
        return cadena
    
    def Sort_Transitions(self):
        self.l_transitions.sort(key = lambda transition: transition.getSymbol())
#Para la lista _______________________________________________________________________

# Definición de la clase Node
#Para la lista _______________________________________________________________________

# Definición de la clase Node

class Node:
    def __init__(self, s):
        self.state = s
        self.next = None

# Clase para la lista enlazada
class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, state):
        new_node = Node(state)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    def prepend(self, state):
        new_node = Node(state)
        new_node.next = self.head
        self.head = new_node

    def delete(self, state):
        if not self.head:
            return

        if self.head.state == state:
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.state == state:
                current.next = current.next.next
                return
            current = current.next 
    
    def getTail(self): #Obtiene el ultimo estado de la lista
        current = self.head
        while current.next:
            current = current.next
        return current.state
    
    def getLastNode(self): #Obtiene el ultimo nodo de la lista
        current = self.head
        while current.next:
            current = current.next
        return current
    
    def getNode(self, n):
        if not self.head:
            return None
        count = 1
        current = self.head
        while current.next:
            current = current.next
            count+=1
        return count
    
    def CountNodes(self):
        if not self.head:
            return None
        count = 1
        current = self.head
        while current.next:
            current = current.next
            count+=1
        return count
    
    def concatenateWith(self, List):
        self.getLastNode().next = List.head
    
    def display(self):
        current = self.head
        while current:
            print(current.state)
            current.state.displayTransitions()
            current = current.next
            if current != None:
                print(end=" -> ")
    

'''
____________________________________________________________________________________________________

Se planea hacer una función por cada uno de los casos posibles

____________________________________________________________________________________________________
'''
def CorrectNumerarion(List, adder): 
    current = List.head
    while current:
            current.state.setId(current.state.getId()+adder)  
            if current.state.getTransitions() != None: #Se añadio esta condicion para evitar errores
                for t in current.state.l_transitions:
                    t.setState(t.getState() + adder)
            current = current.next 
    return


def SingleLetter(sym):
    List_SingleLetter = LinkedList()
    t = Transition(sym, 1)
    state1 = State(0, t, True, False)
    state2 = State(1,None, False, True)
    
    #Creamos el nodo
    List_SingleLetter.append(state1)
    List_SingleLetter.append(state2)

    #List_SingleLetter.display()
    return List_SingleLetter

def Concatenation(L1,L2):
    #Quitamos que el estado final de la primera lista sea final
    L1.getTail().setFinalState(False)
    
    
    #Copiamos las transiciones del estado que se va a borrar 
    for t in L2.head.state.l_transitions:
        t.setState(t.getState() + L1.getTail().getId()) #Corregimos la numeracion de los estados internos, no se le suma uno ya el inicial
        L1.getTail().addTransition(t)


    #Eliminamos el estado inicial de la segunda lista    
    L2.delete(L2.head.state)
    
    #Corregimos la numeracion de la segunda lista aumentandole 1 a cada estado
    sum = L1.getTail().getId() + 1
    sum = sum - L2.head.state.getId()
    CorrectNumerarion(L2,sum)
    
    #Concatenamos las listas
    L1.concatenateWith(L2)
    
    #Imprimimos la lista
    #L1.display()
    
    return L1

def Union(L1, L2): #L1 y L2 son listas enlazadas
    CorrectNumerarion(L1, 1)
    CorrectNumerarion(L2, L1.getTail().getId() + 1)
    
    L1.head.state.setIniState(False) #El primer estado de la primera lista ya no es inicial
    new_initial_state = State(0, Transition("λ", L1.head.state.getId()), True, False)
    new_initial_state.addTransition(Transition("λ", L2.head.state.getId()))
    L1.prepend(new_initial_state)

    
    new_final_state = State(L2.getTail().getId() + 1, None, False, True)
    
    #actualiza que ya non el estado final
    L1.getTail().setFinalState(False)
    L2.getTail().setFinalState(False)
    
    
    L1.getTail().addTransition(Transition("λ", new_final_state.getId()))
    L2.getTail().addTransition(Transition("λ", new_final_state.getId()))
    L2.append(new_final_state)
    
    L1.concatenateWith(L2)
    #Imprimimos la lista
  
    return L1
    
def Cerradura_de_Kleene(List): #Recibe como parametro una única lista enlazada
    #Creamos las transiciones nueva y estados nuevos
    CorrectNumerarion(List,1) #Corregimos la numeracion de la lista
    
    List.head.state.setIniState(False) #El primer estado de la lista ya sera el inicial
    List.getTail().setFinalState(False) #El ultimo estado de la lista ya no sera final
    
    t1 = Transition("λ",List.head.state.getId())  #Transicion para llegar a la lista
    t2 = Transition("λ",List.getTail().getId()+1) #Transicion con el edo final
    state1 = State(0,t1,True,False) #Declaramos el nuevo estado inicial
    state1.addTransition(t2) 
    List.prepend(state1) #Añadimos el estado inicial a la lista
    
    state2 = State(List.getTail().getId()+1,None,False,True) #Declaramos el nuevo estado final
    t3 = Transition("λ",List.getTail().getId()+1) #Transicion para llegar al estado final
    t4 = Transition("λ",List.head.state.getId()+1) #Transicion para llegar al estado inicial + 1 (Lo que lo hace while)
    List.getTail().addTransition(t3) #Añadimos la transicion al estado final de la lista
    List.getTail().addTransition(t4) 
    List.append(state2) #Añadimos el estado final a la lista
    
    #List.display()
    
    return List
    

def Cerradura_Opcional(L):
    #Corregimos la numeracion de la lista, añadindo 1 porque agregaremos un nuevo edo inicial
    CorrectNumerarion(L,1)
    #Corregimos la bandera de estado inicial del primer estado de la lista
    L.head.state.setIniState(False)
    #Corregimos la bandera de estado final del ultimo estado de la lista
    L.getTail().setFinalState(False)
    #Creamos las transiciones nuevas y estados nuevos
    
    t1 = Transition("λ",L.head.state.getId()) #Transicion para llegar a la lista
    t2 = Transition("λ",L.getTail().getId()+1) #Transicion para llegar al estado final
    state1 = State(0,t1,True,False) #Declaramos el nuevo estado inicial
    state1.addTransition(t2)
    
    L.prepend(state1) #Añadimos el estado inicial a la lista
    
    t3 = Transition("λ",L.getTail().getId()+1) #Transicion para llegar al estado final
    L.getTail().addTransition(t3) #Añadimos la transicion al estado final de la lista
    state2 = State(L.getTail().getId()+1,None,False,True) #Declaramos el nuevo estado final
    L.append(state2) #Añadimos el estado final a la lista
    
    #Impresion de la lista
    #L.display()
    
    return L

def Cerradura_Positiva(L):
    #Corregimos la numeracion de la lista, ya que añadiremos un nuevo estado inicial
    CorrectNumerarion(L,1)
    #Corregimos la bandera de estado inicial del primer estado de la lista
    L.head.state.setIniState(False)
    #Corregimos la bandera de estado final del ultimo estado de la lista
    L.getTail().setFinalState(False)
    
    #Creamos las transiciones nuevas y estados nuevos
    t1 = Transition("λ",L.head.state.getId()) #Transicion para llegar a la lista
    state1 = State(0,t1,True,False) #Declaramos el nuevo estado inicial
    L.prepend(state1) #Añadimos el estado inicial a la lista
    
    t2 = Transition("λ",L.getTail().getId()+1) #Transicion para llegar al estado final
    t3 = Transition("λ",L.head.state.getId()+1) #Transicion para llegar al estado inicial + 1
    L.getTail().addTransition(t2) 
    L.getTail().addTransition(t3)
    state2 = State(L.getTail().getId()+1,None,False,True) #Declaramos el nuevo estado final
    L.append(state2) #Añadimos el estado final a la lista
    
    #Imprimimos la lista
    #L.display()
    
    return L   
    
#########################################################################################################
#########################################################################################################

import re

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
