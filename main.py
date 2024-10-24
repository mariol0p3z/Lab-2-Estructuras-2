from arbolb import Arbol_B
import json
from huffman import *
class main():
    def __init__(self):
        self.arbol = Arbol_B(3)
        self.codificacion_dpi = {}
        self.arboles_huffman = {}
        self.dpi_empresas = {}
        self.huffman = Huffman()
    
    def leerArchivo(self, nombre_archivo):
        with open(nombre_archivo, mode ='r', encoding='utf-8') as archivo:
            try:
                for linea in archivo:
                    separacion = linea.split(";")
                    accion =  separacion[0]
                    dato = json.loads(separacion[1])
                    if 'companies' in dato:
                        self.procesarEmpresas(dato['dpi'], dato['companies'])
                    if accion == "INSERT":
                        self.arbol.insertar(dato)
                    elif accion == "PATCH":
                        self.arbol.actualizar(dato.get("dpi"), dato.get("name"), dato)
                    elif accion == "DELETE":
                        self.arbol.eliminar({"name": dato.get("name"), "dpi": dato.get("dpi")})
            except FileNotFoundError:
                print("Archivo no encontrado")
            finally:
                archivo.close()
        self.codificarDpiEmpresa()
                
    def buscarNombre(self, nombre):
        resultados = self.arbol.buscarNombre(nombre)
        
        if resultados:
            lista_resultados_json = []
            for resultado in resultados:
                codificacion_empresas = {}
                for empresa in resultado['companies']:
                    if empresa in self.codificacion_dpi and resultado['dpi'] in self.codificacion_dpi[empresa]:
                        dpi_codificado = self.codificacion_dpi[empresa][resultado['dpi']]
                    else:
                        dpi_codificado = resultado['dpi']  
                    codificacion_empresas[empresa] = dpi_codificado

                resultado_json = {
                    "name": resultado["name"],
                    "dpi": resultado["dpi"], 
                    "datebirth": resultado["datebirth"],
                    "address": resultado["address"],
                    "companies": codificacion_empresas 
                }
                
                lista_resultados_json.append(resultado_json)
            
            return json.dumps(lista_resultados_json, indent=4, ensure_ascii=False)
        else:
            return json.dumps({"error": "No se encontraron resultados para el nombre especificado"}, indent=4, ensure_ascii=False)
       
    def procesarEmpresas(self, dpi, empresas):
        for empresa in empresas:
            if empresa not in self.dpi_empresas:
                self.dpi_empresas[empresa] = [] 
            self.dpi_empresas[empresa].append(dpi)

    def codificarDpiEmpresa(self):
        for empresa, dpis in self.dpi_empresas.items():
            tabla_frecuencia = TablaFrecuencias(dpis)
            contexto = tabla_frecuencia.obtenerContexto()
            prioridad_minima = tabla_frecuencia.obtenerPrioridadMinima(contexto)
    
            contador = 0
            while len(prioridad_minima) > 1:
                contador = self.huffman.crearArbol(contexto, prioridad_minima, contador)
                prioridad_minima = tabla_frecuencia.obtenerPrioridadMinima(contexto)
            
            arbol_huffman = contexto[contador - 1]
            
            self.arboles_huffman[empresa] = arbol_huffman
            tabla_bits = {}
            self.huffman.getBitsTabla(arbol_huffman, "", tabla_bits)
            self.codificacion_dpi[empresa] = tabla_bits

    def decodificarDpi(self, empresa, dpi_codificado):
        if empresa not in self.arboles_huffman:
            return None
        
        arbol_huffman = self.arboles_huffman[empresa]
        nodo_actual = arbol_huffman
        
        dpi_decodificado = ""
        for bit in dpi_codificado:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            elif bit == '1':
                nodo_actual = nodo_actual.derecha
            
            if nodo_actual.izquierda is None and nodo_actual.derecha is None:
                dpi_decodificado = nodo_actual.simbolo
                nodo_actual = arbol_huffman 
        return dpi_decodificado

    def decodificarNombre(self, nombre):
        resultados = self.arbol.buscarNombre(nombre)
        
        if resultados:
            lista_resultados_json = []
            for resultado in resultados:
                decodificacion_empresas = {}
                for empresa in resultado['companies']:
                    if empresa in self.codificacion_dpi and resultado['dpi'] in self.codificacion_dpi[empresa]:
                        dpi_codificado = self.codificacion_dpi[empresa][resultado['dpi']]
                        dpi_decodificado = self.decodificarDpi(empresa, dpi_codificado)
                    else:
                        dpi_decodificado = resultado['dpi'] 
                    
                    decodificacion_empresas[empresa] = dpi_decodificado
                
                resultado_json = {
                    "name": resultado["name"],
                    "dpi": resultado["dpi"],  
                    "datebirth": resultado["datebirth"],
                    "address": resultado["address"],
                    "companies": decodificacion_empresas  
                }
                
                lista_resultados_json.append(resultado_json)
            
            return json.dumps(lista_resultados_json, indent=4, ensure_ascii=False)
        else:
            return json.dumps({"error": "No se encontraron resultados para el nombre especificado"}, indent=4, ensure_ascii=False)


    def exportarCodificacion(self, nombre_archivo, nombre_persona):
        with open(nombre_archivo, mode = 'w', encoding='utf-8') as archivo:
            archivo.write(self.buscarNombre(nombre_persona))
            print("Archivo generado exitosamente")

    def exportarDecodificacion(self, nombre_archivo, nombre_persona):
        with open(nombre_archivo, mode = 'w', encoding='utf-8') as archivo:
            archivo.write(self.decodificarNombre(nombre_persona))
            print("Archivo generado exitosamente")
        
if __name__ == '__main__':
    programa = main()
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    programa.leerArchivo(nombre_archivo)
    
    nombre_busqueda = input("Ingrese el nombre a buscar: ")

    programa.exportarCodificacion('Codificacion/'+nombre_busqueda+'_codificado.json', nombre_busqueda)
    programa.exportarDecodificacion('Decodificacion/'+nombre_busqueda+'_decodificado.json', nombre_busqueda)