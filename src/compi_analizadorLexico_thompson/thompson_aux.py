from lib.lista_enlazada import *
from lib.automata import *

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