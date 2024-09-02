import heapq
from aeropuerto import Aeropuerto
from collections import deque
from grafo import Grafo


def camino_minimo(grafo, desde_ciudad, hasta_ciudad, criterio, dict_ciudades): 
    desde = dict_ciudades.get(desde_ciudad)
    hasta = dict_ciudades.get(hasta_ciudad)
    
    if desde is None or hasta is None:
        return None
    
    caminos_minimos = []
    for aeropuerto_origen in desde:
        for aeropuerto_destino in hasta:
            padre, _ = _dijkstra(grafo, aeropuerto_origen, aeropuerto_destino, criterio)
            camino_minimo = _reconstruir_camino(padre, aeropuerto_destino)
            caminos_minimos.append(camino_minimo)

    mejor_camino = encontrar_camino_minimo(caminos_minimos, grafo, criterio)
       
    return mejor_camino

def encontrar_camino_minimo(caminos_minimos, grafo, criterio):
    mejor_camino = None
    mejor_peso = float("inf")
    
    for camino in caminos_minimos:
        if camino is not None:
            peso = calcular_peso_total(camino, grafo, criterio)
            if peso < mejor_peso:
                mejor_camino = camino
                mejor_peso = peso
    
    return [aeropuerto.obtener_codigo() for aeropuerto in mejor_camino]


def calcular_peso_total(camino, grafo, criterio):
    peso_total = 0
    for i in range(len(camino)-1):
        if i == len(camino) - 1:
            break
        aeropuerto_actual = camino[i]
        aeropuerto_siguiente = camino[i+1]
        if criterio == "rapido":
            peso_total+= int(grafo.peso_arista(aeropuerto_actual,aeropuerto_siguiente)[0])
        elif criterio == "barato":
            peso_total+= int(grafo.peso_arista(aeropuerto_actual,aeropuerto_siguiente)[1])
    
    return peso_total


def _dijkstra(grafo, origen, destino, criterio):
    distancia = {}
    padre = {}
    
    for v in grafo.obtener_vertices():
        distancia[v] = float("inf")
    
    for v in grafo.obtener_vertices():
        padre[v] = None
    
    distancia[origen] = 0
    padre[origen] = None
    heap = []
    contador = 0
    heapq.heappush(heap, (0, contador, origen))
    
    while heap:
        _, _, v = heapq.heappop(heap)
        if criterio!="centralidad":
            if v.obtener_ciudad() == destino.obtener_ciudad():
                return padre, distancia 
        
        for w in grafo.adyacentes(v):
            tiempo, precio, cant_vuelos = grafo.peso_arista(v,w)
            nueva_distancia = 0
            if criterio == "rapido":
                nueva_distancia = distancia[v] + int(tiempo)
            
            elif criterio == "barato":
                nueva_distancia = distancia[v] + int(precio)
    
            if nueva_distancia < distancia[w]:
                distancia[w] = nueva_distancia
                padre[w] = v
                contador += 1
                heapq.heappush(heap, (distancia[w], contador, w))

    return padre, distancia

def _reconstruir_camino(padre, destino): 
    camino = []
    v = destino
    
    while v is not None:
        camino.append(v)
        v = padre[v]  
        if v == destino:
            break
    
    return camino[::-1]

def centralidad(grafo):
    cent = {}
    for v in grafo:
        cent[v] = 0
    
    for v in grafo:
        
        padre, distancia = camino_minimo_centralidad(grafo,v)
        cent_aux = {}
        for w in grafo:
            cent_aux[w] = 0
        
        vertices_ordenados = _ordenar_vertices(grafo, distancia)

        for w, _ in vertices_ordenados:
            if padre[w] is None: 
                continue
            
            cent_aux[padre[w]] += 1 + cent_aux[w]
            
        for w in grafo:
            if w == v:
                continue
            
            cent[w] += cent_aux[w]
    
    return cent

def _ordenar_vertices(grafo, distancia):
    res = []
    for v in grafo:
        if distancia[v] == float("inf"):
            continue
        res.append((v, distancia[v]))
    
    return sorted(res, key=lambda x:x[1])[::-1] 

def camino_minimo_centralidad(grafo, origen):
    distancia = {}
    padre = {}
    
    for vertice in grafo:
        distancia[vertice] = float("inf")
        
    distancia[origen] = 0
    padre[origen] = None
    heap = []
    contador = 0
    heapq.heappush(heap, (0, contador, origen))
    
    while heap:
        _, _, v = heapq.heappop(heap)
        for w in grafo.adyacentes(v):
            _, _, cant_vuelos = grafo.peso_arista(v, w)
            peso = 1/int(cant_vuelos)
            
            if distancia[v] + peso < distancia[w]:
                distancia[w] = distancia[v] + peso
                padre[w] = v
                contador += 1
                heapq.heappush(heap, (distancia[w], contador, w))
    
    return padre, distancia

def camino_minimo_escalas(grafo, origen, destino, dict_ciudades):
    aeropuertos_origen = dict_ciudades[origen]
    aeropuertos_destino = dict_ciudades[destino]
    mejor_camino = None
    for aeropuerto_origen in aeropuertos_origen:
        for aeropuerto_destino in aeropuertos_destino:
            padre, _ = _bfs(grafo,aeropuerto_origen,aeropuerto_destino)
            camino_minimo = _reconstruir_camino(padre, aeropuerto_destino)
            
            if mejor_camino is None or len(camino_minimo) < len(mejor_camino):
                mejor_camino = camino_minimo
    
    return [aeropuerto.obtener_codigo() for aeropuerto in mejor_camino]

def _bfs(grafo, origen, destino):
    distancia = {}
    padre = {}
    visitados = set()
    
    for v in grafo.obtener_vertices():
        distancia[v] = float("inf")
        padre[v] = None

    distancia[origen] = 0
    visitados.add(origen.obtener_codigo())
    q = deque()
    q.append(origen)

    while len(q) != 0:
        v = q.popleft()
        if v.obtener_ciudad() == destino:
                return padre,distancia
        for w in grafo.adyacentes(v):
            if w.obtener_codigo() not in visitados:
                distancia[w] = distancia[v] + 1
                padre[w] = v
                visitados.add(w.obtener_codigo())
                q.append(w)

    return padre, distancia

def orden_topologico(grafo):
    visitados = set()
    pila = [] 
    for v in grafo:
        if v not in visitados:
            visitados.add(v)
            _dfs(grafo, v, visitados, pila)
    return pila[::-1] 

def _dfs(grafo, v, visitados, pila):
    for w in grafo.adyacentes(v):
        if w not in visitados:
            visitados.add(w)
            _dfs(grafo, w, visitados, pila)
    
    pila.append(v)

def obtener_grafo_itinerario(ciudades):
    grafo = Grafo(es_dirigido = True, vertices_iniciales = ciudades[0])
    
    for ciudad_origen, ciudad_destino in ciudades[1:]:
        grafo.agregar_arista(ciudad_origen, ciudad_destino)

    return grafo

def camino_minimo_itinerario(grafo, origen, destino, dict_ciudades, aeropuerto_salida):
    if aeropuerto_salida is None:
        return camino_minimo(grafo,origen, destino, "rapido", dict_ciudades)
        
    else:
        return camino_minimo_con_origen(grafo, origen, destino, dict_ciudades, aeropuerto_salida)
        
def camino_minimo_con_origen(grafo, origen, destino, dict_ciudades, codigo_salida):
    desde = None
    hasta = dict_ciudades[destino]  
    for aeropuerto in dict_ciudades.get(origen):
        if aeropuerto.obtener_codigo() == codigo_salida:
            desde = aeropuerto
    
    caminos_totales = []
    
    for aeropuerto_destino in hasta: 
        camino = camino_minimo_escalas(grafo, desde.obtener_ciudad(), aeropuerto_destino.obtener_ciudad(), dict_ciudades)
        caminos_totales.append(camino)
    
    mejor_camino = min(caminos_totales, key=len)
    return mejor_camino

def mst_prim(grafo):
    v = grafo.obtener_vertices()[0]
    visitados = set()
    visitados.add(v)
    heap = []
    cont = 0
    arbol = Grafo(es_dirigido = False, vertices_iniciales = grafo.obtener_vertices())
    for w in grafo.adyacentes(v):
        heapq.heappush(heap,(int(grafo.peso_arista(v,w)[1]), cont, v, w))
        cont+=1
    while heap:
        _, _, v, w = heapq.heappop(heap)
        if w in visitados:
            continue
        arbol.agregar_arista(v, w, grafo.peso_arista(v,w))
        visitados.add(w)
        for u in grafo.adyacentes(w):
            if u not in visitados:
                cont+=1
                heapq.heappush(heap, (int(grafo.peso_arista(w,u)[1]), cont, w, u))
    return arbol

def obtener_vuelos(grafo):
    res = []
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
                tiempo, precio, cant_vuelos = grafo.peso_arista(v,w)
                res.append([v.obtener_codigo(), w.obtener_codigo(), tiempo, precio, cant_vuelos])
    
    return res


