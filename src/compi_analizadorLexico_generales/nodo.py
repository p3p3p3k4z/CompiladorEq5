class Node:
    def __init__(self,s, next_node=None, prev_node=None):
        self.state = s
        self.next = next_node
        self.prev = prev_node

    def __str__(self):
        return f"Nodo({self.state})"

    def __repr__(self):
        return f"Node(Estado={self.state}, Siguiente={repr(self.next)}, Previo={repr(self.prev)})"
