class Transition:
    
    def __init__(self, sy = None, st = None):#constructor1 con nada
        symbol = ""
        next_state = -1
        
    def __init__(self, sy, st):
        self.symbol = sy#Simbolo
        self.next_state = st#a donde lleva
    #gets y sets
    def getSymbol(self):
        return self.symbol
    
    def getState(self):
        return self.next_state
    
    def setSymbol(self, sy):
        self.symbol = sy
    
    def setState(self, st):
        self.next_state = st
        
    def __str__(self):#duvuelve el siguiente estado en forma de cadena
        #return "Symbol: " + self.symbol + " Next State: " + str(self.next_state)+ "\n"
        return str(self.next_state) 
    

class State:
    def __init__(self, i, transition, ini, fin):
        self.id = i #Id es el numero de estado
        self.l_transitions = []#almacena transiciones
        if transition != None:#si se da una transicion al crear el estado se añade a la lista
            self.l_transitions = [transition] #la transicion dada sera la primera transicion
        self.initial_state = ini #dice si es estado inicial
        self.final_state = fin#indica si es final
    #gets y sets
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
        self.l_transitions.append(t)#añadimos transciones
    
    def displayTransitions(self):#mostramos las transciones
        i = 0
        NTransitions = len(self.l_transitions)
        for s in self.l_transitions:
            if (self.l_transitions[i] != None and i < NTransitions):
                print("El estado: " + str(self.l_transitions[i].getState()) + " con simbolo: " + self.l_transitions[i].getSymbol())
                i+=1
    def __str__(self):
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
        self.l_transitions.sort(key = lambda transition: transition.getSymbol())#el criterio de ordenamiento es getsymbol

class Node:
    def __init__(self, s):
        self.state = s
        self.next = None

# Clase para la lista enlazada
class LinkedList:
    def __init__(self):#constructor donde decimos que la lista esta vacia a la hora de la creacion
        self.head = None

    def is_empty(self):#verifica si la lista esta vacia
        return self.head is None

    def append(self, state):#añade un nuevo nodo al final de la pila
        new_node = Node(state)
        if not self.head:
            self.head = new_node#si la lista vacia head sera el nuevo nodo
        else:
            current = self.head
            while current.next:#si no es asi se recorre las lista hasta encontrar el ultimo nodo
                current = current.next
            current.next = new_node#se enlaza el nuevo nodo al final
    
    def prepend(self, state):#añade un nodo al principio de la pila
        new_node = Node(state)#crea un nodo
        new_node.next = self.head#enlaza el primer nodo con el antigua primer nodo
        self.head = new_node#actualiza head para que apunte al nuevo primer nodo

    def delete(self, state):
        if not self.head:#si la lista esta vacia el metodo terminna aqui
            return

        if self.head.state == state:#si la cabeza coincide con el valor que deseamos eliminar
            self.head = self.head.next#actualizamos la cabeza para que apunte al nodo siguiente
            return

        current = self.head#recorremos la lista, si encontramos un nodo cuyo estado coincide con
        while current.next:#el valor que deseamos eliminar cambiamos el puntero next del nodo actual para
            if current.next.state == state:#saltar el nodo a eliminar
                current.next = current.next.next
                return
            current = current.next #en caso de que no avanzamos al siguiente nodo
    
    def getTail(self): #Obtiene el ultimo estado de la lista
        if not self.head:#comprobacion para una lista vacia
            return None
        current = self.head#comienas desde la cabeza de la lista
        while current.next:#avanzamos hasta el ultimo nodo cuyovalor sea none
            current = current.next
        return current.state #regresas el ultimo nodo de la lista
    
    def getLastNode(self): #Obtiene el ultimo nodo de la lista
        current = self.head#se inicializa con el primer nodo de la lista
        while current.next: #mientra la variable no sea none(ninguna)
            current = current.next #en cada iteracion current se mueve al nodo siguiente
        return current
       
    def CountNodes(self):#contar el numero total de nodos
        if not self.head:#comprueba si lalista esta vacia
            return None
        count = 1
        current = self.head
        while current.next:#se repite hasta que current sea none, es decir hasta llegar al ultimo nodo
            current = current.next
            count+=1
        return count#regresa el numero total de nodos en la lista
    
    def concatenateWith(self, List):#unir dos listas, añadiendo la segunda al final de la primera
        self.getLastNode().next = List.head#hacemos que el ultino nodo apunte al primero de la siguiente
    
    def display(self):#Mostrar en la consola el estado de cada nodo de la lista enlazada y las transiciones.
        current = self.head#current se inicializa con el primer nodo
        while current:#continuara hasta que current sea none
            print(current.state)#imprimimos el estado del nodo actual
            current.state.displayTransitions()#mostramos la transcion de el estado del nodo actual
            current = current.next#decimos que current apunta al nodo siguiente
            if current != None:
                print(end=" -> ")#y lo imprimimos en caso de que no se none
    
def CorrectNumerarion(List, adder):#Actualiza el numero de los estados
    current = List.head#primer nodo de la lista
    while current:#hasta que current sea none
            current.state.setId(current.state.getId()+adder)  #obtenemos el id y despues establecemos el nuevo id
            if current.state.getTransitions() != None:#si gettransitions no devuelve none procedemos
                for t in current.state.l_transitions:#Se itera sobre la lista
                    t.setState(t.getState() + adder)#se establece un nuevo estado se le asigna su estado actua mas adder
            current = current.next #apunta al siguiente nodo de la lista
    return#no regresa nada


def SingleLetter(sym):#modifica y une dos automatas para tener uno solo
    List_SingleLetter = LinkedList()#inicializamos una lista con la lista enlazada vacia
    t = Transition(sym, 1)#creamos una instancia de transicion
    state1 = State(0, t, True, False)#creamos el primer estado, donde no es un estado final pero si inicial
    state2 = State(1,None, False, True)#creamos el segundo estado y aqui viceversa 
    
    #Creamos el nodo
    List_SingleLetter.append(state1)
    List_SingleLetter.append(state2)#añadimos el estado 1 y el estado dos a las lista

    #List_SingleLetter.display() #por si
    return List_SingleLetter#regresamos la lista de estados y procesos en consola

def Concatenation(L1,L2):#modificamos la lista para que el estado final no sea final
    L1.getTail().setFinalState(False)
    
    
    #Copiamos las transiciones del estado que se va a borrar 
    for t in L2.head.state.l_transitions: #recorremos sobre las transiciones del estado inicial
        t.setState(t.getState() + L1.getTail().getId()) #Corregimos la numeracion de los estados internos
        L1.getTail().addTransition(t)#añadimos la transicion correjida al ultimo estadp


    #Eliminamos el estado inicial de la segunda lista    
    L2.delete(L2.head.state)
    
    #Corregimos la numeracion de la segunda lista aumentandole 1 a cada estado
    sum = L1.getTail().getId() + 1#añadimos 1 al id del ultimo estado
    sum = sum - L2.head.state.getId()#restamos el id del primer nuevo estado
    CorrectNumerarion(L2,sum)#hacemos el ajuste de los ids con el nuevo valor calculado
    
    #Concatenamos las listas
    L1.concatenateWith(L2)
    
    #Imprimimos la lista
    #L1.display()
    
    return L1#regresa la lista L1 que ahora contiene todos los estado y transiciones de ambas listas

def Union(L1, L2): #L1 y L2 son listas enlazadas
    CorrectNumerarion(L1, 1)#se corrijen los ids para evitar problemas
    CorrectNumerarion(L2, L1.getTail().getId() + 1)#se empieza a enumerar desde el valor dispoble despues de L1
    
    L1.head.state.setIniState(False) #El primer estado de la primera lista ya no es inicial, ya que se creara un nuevo estado inicial
    new_initial_state = State(0, Transition("λ", L1.head.state.getId()), True, False)#se crea el estado inicial,
    #con una transicion λ que apunta al antes primer estado
    new_initial_state.addTransition(Transition("λ", L2.head.state.getId()))
    #se añade una transicion que permite unir el nuevo estado al estado inicial del segundo automata
    L1.prepend(new_initial_state)
    #el estado inicial sera insertado al principio de la lista L1

    #creamos un nuevo estado final
    new_final_state = State(L2.getTail().getId() + 1, None, False, True)
    
    #El estado final de ambos automatas ya no es un estado final
    L1.getTail().setFinalState(False)
    L2.getTail().setFinalState(False)
    
    #añadimos una transicion de ambos estados finales al nuevo estadp final
    L1.getTail().addTransition(Transition("λ", new_final_state.getId()))
    L2.getTail().addTransition(Transition("λ", new_final_state.getId()))
    #lo añadimos al final de la lista L2
    L2.append(new_final_state)
    #unimos las listas L1 y L2
    L1.concatenateWith(L2)
    #Imprimimos la lista
    
    #nos regresa la lista unida
    return L1
    
def Cerradura_de_Kleene(List): #Recibe como parametro una única lista enlazada
    CorrectNumerarion(List,1) #Corregimos la numeracion de la lista comenzando desde 1
    
    #decimos que el estado final e inicial dejan de serlo
    List.head.state.setIniState(False) 
    List.getTail().setFinalState(False) 
    
    t1 = Transition("λ",List.head.state.getId())  #Creamos una transicion desde el nuevo estado inicial
    #al anterior estado inicial
    t2 = Transition("λ",List.getTail().getId()+1) #Transicion del anterior estado final al nuevo estado final
    state1 = State(0,t1,True,False) #Creamos el nuevo estado inicial
    state1.addTransition(t2) 
    List.prepend(state1) #Añadimos el estado inicial a la lista
    
    state2 = State(List.getTail().getId()+1,None,False,True) #Creamos un nuevo estado final
    t3 = Transition("λ",List.getTail().getId()+1) #Transicion para ir al estado final
    t4 = Transition("λ",List.head.state.getId()+1) #Transicion para ir al anterior estado inicial
    List.getTail().addTransition(t3) #Añadimos las transiciones
    List.getTail().addTransition(t4) 
    List.append(state2) #Añadimos el estado final a la lista
    
    #List.display()
    #regresamos la lista modificada
    return List
    

def Cerradura_Opcional(L):
    #Corregimos la numeracion de la lista
    CorrectNumerarion(L,1)
    #el estado inicial deja de ser inicial
    L.head.state.setIniState(False)
    #el estado final deja de ser final
    L.getTail().setFinalState(False)
    
    t1 = Transition("λ",L.head.state.getId()) #Creamos una transicion para ir del nuevo estado inicial al anterior estado inicial
    t2 = Transition("λ",L.getTail().getId()+1) #Transicion para llegar al estado final desde el nuevo estado inicial
    state1 = State(0,t1,True,False) #Creamos el nuevo primer estado
    state1.addTransition(t2)#agregamos las transiciones
    
    L.prepend(state1) #Añadimos el estado inicial al principio de la lista
    
    t3 = Transition("λ",L.getTail().getId()+1) #Transicion para llegar al nuevo estado final desde el anterior estado final
    L.getTail().addTransition(t3) #Añadimos la transicion al final de la lista
    state2 = State(L.getTail().getId()+1,None,False,True) #Declaramos el nuevo estado final
    L.append(state2) #Añadimos el estado final a la lista
    
    #Impresion de la lista
    #L.display()
    
    return L#regresamos la lista modificada

def Cerradura_Positiva(L):
    #Corregimos la numeracion de la lista
    CorrectNumerarion(L,1)
    #El estado inicial deja de serlo
    L.head.state.setIniState(False)
    #El estado final deja de serlo
    L.getTail().setFinalState(False)
    
    t1 = Transition("λ",L.head.state.getId()) #Añadimos una transicion del nuevo estado inicial al anterior estado inicial
    state1 = State(0,t1,True,False) #creamos el nuevo esatdo
    L.prepend(state1) #Añadimos el estado al inicio de la pila
    
    t2 = Transition("λ",L.getTail().getId()+1) #Transicion para ir al nuevo estado final desde el anterior estado final
    t3 = Transition("λ",L.head.state.getId()+1) #Transicion para ir al estado inicial desde el estado final
    L.getTail().addTransition(t2) 
    L.getTail().addTransition(t3)#añadimos las transiciones 
    state2 = State(L.getTail().getId()+1,None,False,True) #creamos el nuevo estado final
    L.append(state2) #Añadimos el estado final a la lista
    
    #Imprimimos la lista
    #L.display()
    #regresamos la lista
    return L   
    
#########################################################################################################
#########################################################################################################

import re#nos permite trabajar con expresiones regulares en python

def generar_alfabeto(lineas):#se recibe una lista
    alfabeto = set() #se crea un conjunto vacio llamda alfabeto
    for linea in lineas:
        # Buscamos las líneas que comienzan con "alfabetoX:"
        match = re.match(r'^alfabeto(\d+): (.+)$', linea)#expresion regular para buscar alfabeto
        if match: #verificamos si obtuvo una respuesta
            numero_alfabeto = match.group(1)#se le asigna el numero del alfabeto
            contenido = match.group(2)#le asignamos el texto que sigue
            if contenido == 'letras':
                alfabeto.update('l')#cambiamos la palabra por un caracter
            elif contenido == 'digitos':
                #cambiamos la palabra por una letra
                alfabeto.update('d')
            # De lo contrario, agregamos las letras únicas
            else:
                alfabeto.update(set(contenido))
    return sorted(alfabeto) #regresamos el conjunto alfabeto en forma de lista ordenada

def obtener_expresion(lineas):#recibe una lista
    for linea in lineas:
        if linea.startswith("expresion:"): #se verifica si la expresion inicia con "Expresion"
            return re.sub(r'^expresion: (.+)$', r'\1', linea)
        #busca una expresion regular y la sustituye por una cadena vacia

def expresion_postfija(expresion):#recibe una expresion en notacion infija
    def precedencia(op):#asignamos la prioridad aqui
        precedencias = {'|': 1, '.': 2, '*': 3, '+': 4, '?':5}
        return precedencias.get(op, 0)

    def a_postfija(expresion):#funcion para convertir a posfija
        pila_operadores = []#almacena los operadores
        salida = []#lista con la expresion en postfija
        i = 0

        while i < len(expresion):
            token = expresion[i]

            if token.isalnum():#manejo de diferentes tokens
                salida.append(token)
            elif token == '(':
                pila_operadores.append(token)
            elif token == ')':
                #verifica que el último elemento añadido no sea (
                while pila_operadores and pila_operadores[-1] != '(':
                    #añadimos el elemento extraido a la pila salida
                    salida.append(pila_operadores.pop())
                pila_operadores.pop()#Eliminamos el ( de la pila
            else:
                while pila_operadores and precedencia(token) <= precedencia(pila_operadores[-1]):
                    salida.append(pila_operadores.pop())#añadimos un operador a la pila
                pila_operadores.append(token)#añadimos el operador
            i += 1

        while pila_operadores:
            salida.append(pila_operadores.pop())#añadimos los operadores restantes a la pila

        return ''.join(salida)#unimos los elementos de una lista en una unica cadena con '' como separacion
    #ejemplo tenienod 'a', 'b', '+' el resultado sera 'ab+'

    return a_postfija(expresion)#regresa la expresion infija en postfija


def evaluar_expresion_postfija(expresion_postfija):
    pila = []
    Automata = LinkedList()
    
    for token in expresion_postfija:#iteramos
        if token.isalnum():
            pila.append(token)#si es alfanumerico se añade a la pila de forma directa
            
        elif token == '?':
            operand1 = pila.pop()#extraemos de la pila el ultimo valor agregado
            if type(operand1) != LinkedList:#
                operand1 = SingleLetter(str(operand1))#si operand1 no es un automata, decimos que es 'a'
                
            Automata = Cerradura_Opcional(operand1)#lo procesamos con la cerradura
            pila.append(Automata) #agregamos el resultado a la pila
            
        elif token == '*':#lo mismo del paso anterior pero con diferente cerradura
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
                
            Automata = Cerradura_de_Kleene(operand1)
            pila.append(Automata)
            
        elif token == '+':#lo mismo pero con diferente cerradura
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
                
            Automata = Cerradura_Positiva(operand1)
            pila.append(Automata)
            
        elif token == '.':
            operand2 = pila.pop()#añadimos el ultimo elemento de la pila
            operand1 = pila.pop()#añadimos el pnultimo elemento de la pila
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))#verificamos si es un automata o no
            if type(operand2) != LinkedList:
                operand2 = SingleLetter(str(operand2))#de igual manera
            Automata = Concatenation(operand1,operand2)#llamamos a la funcion correspondiente
            pila.append(Automata)#añadimos a la pila
            
        elif token == '|':#lo mismo del anterior paso pero con diferente llamado de funcion
            operand2 = pila.pop()
            operand1 = pila.pop()
            if type(operand1) != LinkedList:
                operand1 = SingleLetter(str(operand1))
                
            if type(operand2) != LinkedList:
                operand2 = SingleLetter(str(operand2))
            
            Automata = Union(operand1,operand2)
            pila.append(Automata)
            
    #Regresamos el automata resultante
    return pila.pop()