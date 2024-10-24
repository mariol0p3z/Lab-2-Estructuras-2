from nodo import Nodo

class Arbol_B:
    def __init__(self, grado):
        self.raiz = Nodo(True)
        self.grado = grado
        
    def mostrar(self):
        self.raiz.mostrar()

    def insertar(self, k):
        raiz = self.raiz
        if len(raiz.llaves) == (2*self.grado) - 1:
            tmp = Nodo()
            self.raiz = tmp
            tmp.hijos.append(raiz)
            self.dividirNodo(tmp, 0)
            self.insertarNodo(tmp,k)
        else:
            self.insertarNodo(raiz, k)

    def insertarNodo(self,x, k):
        i = len(x.llaves) -1
        if x.Eshoja:
            x.llaves.append(None)
            while i >= 0 and x.llaves[i]['dpi'] > k['dpi']:
                x.llaves[i + 1] = x.llaves[i]
                i -= 1
            x.llaves[i+1] = k
        else:
            while i >= 0 and x.llaves[i]['dpi'] > k['dpi']:
                i -= 1
            i += 1
            if len(x.hijos[i].llaves) == (2*self.grado) - 1:
                self.dividirNodo(x, i)
                if x.llaves[i]['dpi'] < k['dpi']:
                    i += 1
            self.insertarNodo(x.hijos[i], k)
    
    def dividirNodo(self,x, i):
        t = self.grado
        y = x.hijos[i]
        z = Nodo(y.Eshoja)
        x.llaves.insert(i, y.llaves[t-1])
        z.llaves = y.llaves[t:(2*t) -1]
        y.llaves = y.llaves[0:(t-1)]
        if not y.Eshoja:
            z.hijos = y.hijos[t:(2*t)]
            y.hijos = y.hijos[0:t]
        x.hijos.insert(i + 1, z)

    def buscar(self, k, x = None):
        if x is None:
            x = self.raiz
        i = x.buscarLlaves(k)
        if i < len(x.llaves) and x.llaves[i]['dpi'] == k['dpi']:
            return x,i
        if x.Eshoja:
            return None
        return self.buscar(k, x.hijos[i])

    def buscar_por_nombre_y_dpi(self, dpi, nombre, x = None):
        if x is None:
            x = self.raiz
        i = x.buscarLlaves({'dpi':dpi})
        if i < len(x.llaves) and x.llaves[i]['dpi'] == dpi:
            if x.llaves[i]['name'].lower() == nombre.lower():
                return x.llaves[i]
            else:
                return None
        if x.Eshoja:
            return None
        return self.buscar_por_nombre_y_dpi(dpi, nombre, x.hijos[i])
    
    def buscarNombre(self, nombre, x = None):
        if x is None:
            x = self.raiz
        resultados = []
        for llave in x.llaves:
            if llave['name'].lower() == nombre.lower():
                resultados.append(llave)
        if not x.Eshoja:
            for hijo in x.hijos:
                resultados.extend(self.buscarNombre(nombre, hijo))
        return resultados

    def eliminar(self, k):
        self.eliminarNodo(self.raiz, k)
        if len(self.raiz.llaves) == 0:
            if not self.raiz.Eshoja:
                self.raiz = self.raiz.hijos[0]
            else:
                self.raiz = None

    def eliminarNodo(self, x, k):
        i = x.buscarLlaves(k)
        if i < len(x.llaves) and x.llaves[i]["dpi"] == k["dpi"] and x.llaves[i]["name"].lower() == k["name"].lower():
            if x.Eshoja:
                x.llaves.pop(i)
            else:
                self.eliminarNodoInterno(x, k, i)
        else:
            if x.Eshoja:
                return
            f = (i == len(x.llaves))
            if len(x.hijos[i].llaves) < self.grado:
                self.llenar(x, i)
            if f and i > len(x.llaves):
                self.eliminarNodo(x.hijos[i-1], k)
            else:
                self.eliminarNodo(x.hijos[i], k)

    def eliminarNodoInterno(self, x, k, i):
        t = self.grado
        if len(x.hijos[i].llaves) >= t:
            anterior = self.getAnterior(x, i)
            x.llaves[i] = anterior
            self.eliminarNodo(x.hijos[i], anterior)
        elif len(x.hijos[i+1].llaves) >= t:
            siguiente = self.getSiguiente(x, i)
            x.llaves[i] = siguiente
            self.eliminarNodo(x.hijos[i+1], siguiente)
        else:
            self.unir(x, i)
            self.eliminarNodo(x.hijos[i], k)

    def getAnterior(self, x, i):
        tmp = x.hijos[i]
        while not tmp.Eshoja:
            tmp = tmp.hijos[len(tmp.llaves)]
        return tmp.llaves[len(tmp.llaves) -1]

    def getSiguiente(self, x, i):
        tmp = x.hijos[i + 1]
        while not tmp.Eshoja:
            tmp = tmp.hijos[0]
        return tmp.llaves[0]

    def actualizar(self, dpi, nombre, nuevos_valores):
        nodo = self.buscar_por_nombre_y_dpi(dpi, nombre)
        if nodo:
            nodo.update(nuevos_valores)
            #print(f"Datos actualizados: {nodo}")
        else:
            print("No se encontro el dato para actualizar")

    def llenar(self, x,i):
        if i != 0 and len(x.hijos[i-1].llaves) >= self.grado:
            self.prestarAnterior(x,i)
        elif i != len(x.hijos) -1 and len(x.hijos[i+1].llaves) >= self.grado:
            self.prestarSiguiente(x,i)
        else:
            if i != len(x.hijos) -1:
                self.unir(x, i)
            else:
                self.unir(x, i -1)
    
    def prestarAnterior(self, x, i):
        hijo = x.hijos[i]
        hermano = x.hijos[i-1]
        hijo.llaves.insert(0, x.llaves[i -1])
        if not hijo.Eshoja:
            hijo.hijos.insert(0, hermano.hijos.pop())
        x.llaves[i-1] = hermano.llaves.pop()

    def prestarSiguiente(self, x, i):
        hijo = x.hijos[i]
        hermano = x.hijos[i+1]
        hijo.llaves.append(x.llaves[i])
        if not hijo.Eshoja:
            hijo.hijos.append(hermano.hijos.pop(0))
        x.llaves[i] = hermano.llaves.pop(0)

    def unir(self, x, i):
        hijo = x.hijos[i]
        hermano = x.hijos[i+1]
        hijo.llaves.append(x.llaves.pop(i))
        hijo.llaves.extend(hermano.llaves)
        if not hijo.Eshoja:
            hijo.hijos.extend(hermano.hijos)
        x.hijos.pop(i+1)
        if x == self.raiz and len(x.llaves) == 0:
            self.raiz = hijo