FLECHA =  "->"
COSTO = 0
TIEMPO = 1

class Grafo:
    def __init__(self, es_dirigido = False, vertices_iniciales = []): 
        self.es_dirigido = es_dirigido
        self.vertices = {v : {} for v in vertices_iniciales } 
        
    def __str__(self):
        acumulador = ""
        for v in self.vertices.keys():
            acumulador += f"{v} {FLECHA} "
            i = 0
            for w in self.vertices[v]:
                acumulador += f"{w}" 
                if i < len(self.vertices[v]) - 1:
                    acumulador += f" {FLECHA} " 
                i += 1
            print(acumulador)
            acumulador = ""
        return ""

    def __iter__(self):
        return self.vertices.__iter__()

    def agregar_vertice(self, vertice):
        if self.vertices.get(vertice) is None:
            self.vertices[vertice] = {} 
    
    def borrar_vertices(self, vertice):
        try:
           del self.vertices[vertice]
        except KeyError:
            print("El vertice no pertenece al grafo")
    
    def agregar_arista(self, origen, destino, peso = 1):
        if self.vertices.get(origen) is None:
            self.vertices[origen] = {destino : peso}
        else:
            aristas = self.vertices[origen]
            aristas[destino] = peso
        if not self.es_dirigido:
            if self.vertices.get(destino) is None:
                self.vertices[destino] = {origen : peso}
            else:
                aristas = self.vertices[destino]
                aristas[origen] =  peso

    def borrar_arista(self, v, w):
        if not self._pertenecen(v, w):
            raise ValueError("Los vertices no pertenecen al grafo")
        if not self.estan_unidos(v, w):
            raise ValueError("La arista no existe")
        
        ady = self.vertices.get(v)
        del ady[w]
        if not self.es_dirigido:
            ady = self.vertices.get(w)
            del ady[v]

    def estan_unidos(self, v, w):
        if self.vertices.get(v) is None:
          
            return False
    
        ady = self.vertices.get(v)
        return ady.get(w) is not None
    
    def peso_arista(self, v, w):
        if not self.estan_unidos(v, w):
            raise ValueError("Los vertices no estan conectados")    
        if not self._pertenecen(v, w):
            raise ValueError("Los vertices no pertenecen al grafo")
        ady = self.vertices.get(v)
        return ady[w]
        
    def obtener_vertices(self):
        return list(self.vertices.keys())
     
    def adyacentes(self, vertice):
        try:
            ady = self.vertices[vertice]
            return ady
        except KeyError:
            print("El vertice no pertenece al grafo")

    def _pertenecen(self, v, w):
        return v in self.vertices and w in self.vertices            


