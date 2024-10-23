def cerradura_epsilon(estados, funcion_transiciones):
    # Inicializar la cerradura-ε con los estados iniciales
    cerradura = set(estados)
    
    # Crear una pila e inicializarla con los estados dados
    pila = list(estados)
    
    # Mientras la pila no esté vacía
    while pila:
        # Sacar el estado de la parte superior de la pila
        t = pila.pop()
        
        # Obtener las transiciones ε desde el estado t usando la función proporcionada
        for v in funcion_transiciones(t):
            # Si el estado v no está ya en la cerradura-ε
            if v not in cerradura:
                # Añadir v a la cerradura-ε
                cerradura.add(v)
                # Meter v en la pila para explorar sus transiciones
                pila.append(v)

    return cerradura

def funcion_transiciones(estado):
    # Esta función debería devolver todos los estados alcanzables queda pendiente para los compañeros responsables de implementar la funcion
    # desde el estado dado a través de transiciones
    return transiciones_epsilon.get(estado, [])
