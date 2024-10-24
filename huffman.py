class Nodo_Huffman:
    def __init__(self, izquierda, derecha, frecuencia, simbolo):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = izquierda
        self.derecha = derecha


class TablaFrecuencias:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def obtenerContexto(self):
        contexto = {}
        for simbolo in self.mensaje:
            if simbolo in contexto:
                contexto[simbolo] += 1
            else:
                contexto[simbolo] = 1
        return contexto

    def obtenerPrioridadMinima(self, contexto):
        prioridad = []
        for llave, valor in contexto.items():
            prioridad.append((llave, valor))

        def LlavePrioridad(elemento):
            if isinstance(elemento[1], int):
                return elemento[1]
            else:
                return elemento[1].frecuencia 
        
        prioridad = sorted(prioridad, key = LlavePrioridad, reverse= True)
        return prioridad

class Huffman:
    def __crear_nodo(self, contexto, prioridad):
        nodo = None
        if isinstance(prioridad[0], str):
            nodo = Nodo_Huffman(None, None, prioridad[1], prioridad[0])
        else:
            nodo = contexto[prioridad[0]]
        return nodo
    
    def __crear_nuevo_arbol(self, izquierda, derecha, simbolo):
        return Nodo_Huffman(izquierda, derecha, izquierda.frecuencia + derecha.frecuencia, simbolo)
    
    def crearArbol(self, contexto, prioridad_min, contador):
        izq = prioridad_min.pop()
        nodo_izq = self.__crear_nodo(contexto, izq)
        del contexto[izq[0]]

        der = prioridad_min.pop()
        nodo_der = self.__crear_nodo(contexto, der)
        del contexto[der[0]]

        nuevo_arbol = self.__crear_nuevo_arbol(nodo_izq, nodo_der, contador)
        contexto[contador] = nuevo_arbol

        return contador + 1
    
    def getBitsTabla(self, nodo, ruta, tabla):
        if nodo.izquierda is None and nodo.derecha is None:
            tabla[nodo.simbolo] = ruta
            return
        if nodo.izquierda is not None:
            self.getBitsTabla(nodo.izquierda, ruta + '0', tabla)

        if nodo.derecha is not None:
            self.getBitsTabla(nodo.derecha, ruta + '1', tabla)
            