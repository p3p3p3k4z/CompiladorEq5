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
        return cadena
    
    def Sort_Transitions(self):
        self.l_transitions.sort(key = lambda transition: transition.getSymbol())
