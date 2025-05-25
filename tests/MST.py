def arbol_expansion_minima(num_nodos, aristas, arista_forzada=None):
    # Codigo para resolver ejercicio Arbol de expansión mínima (MST)
    # Actividad 5.2
    padre = list(range(num_nodos))
    rango = [0] * num_nodos

    def encontrar(nodo):
        while padre[nodo] != nodo:
            padre[nodo] = padre[padre[nodo]]
            nodo = padre[nodo]
        return nodo

    def unir(nodo1, nodo2):
        raiz1, raiz2 = encontrar(nodo1), encontrar(nodo2)
        if raiz1 == raiz2:
            return False
        if rango[raiz1] < rango[raiz2]:
            padre[raiz1] = raiz2
        else:
            padre[raiz2] = raiz1
            if rango[raiz1] == rango[raiz2]:
                rango[raiz1] += 1
        return True

    mst = []
    costo_total = 0


    if arista_forzada:
        peso, nodo1, nodo2 = arista_forzada
        if unir(nodo1, nodo2):
            mst.append((peso, nodo1, nodo2))
            costo_total += peso

    aristas = sorted(aristas)
    for peso, nodo1, nodo2 in aristas:
        if arista_forzada and (peso, nodo1, nodo2) == arista_forzada:
            continue  
        if unir(nodo1, nodo2):
            mst.append((peso, nodo1, nodo2))
            costo_total += peso
        if len(mst) == num_nodos - 1:
            break

    return mst, costo_total

# Datos del ejercicio      LA-CH        NY - DC     CH - NY     DE - DA     CH - DA     LA - SE 
aristas =               [(2000, 0, 1), (200, 2, 3),(800, 1, 2),(780, 4, 5),(900, 1, 5),(1100, 0, 6)]

mst, costo_total = arbol_expansion_minima(7, aristas, (2600, 0, 1))
print("MST:", mst)
print("Costo total:", costo_total)
