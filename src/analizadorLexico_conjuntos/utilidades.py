def quita_duplicados(lista):
    nueva_lista = []
    for elem in lista:
        if elem not in nueva_lista:
            nueva_lista.append(elem)
    return nueva_lista

def unir_listas(lista1, lista2):
    for elem in lista2:
        if elem not in lista1:
            lista1.append(elem)
    lista1.sort()
    return lista1
