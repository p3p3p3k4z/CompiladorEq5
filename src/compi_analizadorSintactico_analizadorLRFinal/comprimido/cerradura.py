def cerradura(conjuntoI, reglas):
    lista_I = list(conjuntoI)
    lista_r = list(reglas)
    nueva_I = lista_I[1]    # Se crea la nueva lista I solo con las reglas de producción
    for elemento in nueva_I:        # Se recorren las reglas de la lista nueva

        j = 0
        for i in range(0, len(elemento[1])):    # Se recorre la lista de producciones de cada regla
            if elemento[1][i] == '•':           # Si una producción es el símbolo •
                j = i                           # devuelve la posición siguiente a tal símbolo
                break

        simbNT = ''                                 # Por defecto se asume un símbolo vacío
        if j < len(elemento[1])-1:                  # Si aún se puede aumentar el índice obtenido
            simbNT = elemento[1][j+1]               # Se saca el primer símbolo tras el •
        
        for regla in lista_r:              # Para cada regla en la lista
            if regla[0] == simbNT:                  # Se comparan el símbolo tras el • y la base de la regla, y si son iguales...
                nv_regla = ["", []]
                nv_regla[0] = regla[0]
                for simbolo in regla[1]:
                    nv_regla[1].append(simbolo)
                # Se crea una nueva regla tomando como base la regla ya existente
                nv_regla[1].insert(0, '•')             # Se inserta el símbolo • al inicio de las producciones
                if not(nv_regla in nueva_I):
                    nueva_I.append(nv_regla)            # Y se agrega a la nueva lista de reglas

    return nueva_I
