from nodo import Node

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
   
#Obtiene el ultimo estado de la lista 
    def getTail(self): 
        current = self.head
        while current.next:
            current = current.next
        return current.state

#Obtiene el ultimo nodo de la lista    
    def getLastNode(self): 
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
