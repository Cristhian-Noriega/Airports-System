import aeropuerto
import csv
import heapq
from grafo import Grafo

def cargar_aeropuertos(aeropuertos):
    try:
        with open(aeropuertos, "r") as archivo:
            lista = []
            dict_aeropuertos = {}
            dict_ciudades = {}
            csv_reader = csv.reader(archivo, delimiter = ",")
            
            for linea in csv_reader:
                aeropuerto_obj = aeropuerto.Aeropuerto(linea)
                lista.append(aeropuerto_obj)
                dict_aeropuertos[aeropuerto_obj.obtener_codigo()] = aeropuerto_obj

                ciudad=linea[0]
                if ciudad in dict_ciudades:
                    dict_ciudades[ciudad].append(aeropuerto_obj)
                else:
                    dict_ciudades[ciudad]=[aeropuerto_obj]

            return lista, dict_aeropuertos, dict_ciudades
    
    except IOError:
        print(f"No se pudo abrir {aeropuertos}")
    
def cargar_vuelos(grafo, vuelos, aeropuertos):
    try:
        with open(vuelos, "r") as archivo:
            csv_reader = csv.reader(archivo, delimiter = ",")
            
            for linea in csv_reader:
                origen, destino, tiempo, precio, cant_vuelos = linea 

                
                aeropuerto_origen = aeropuertos[origen]
                aeropuerto_destino = aeropuertos[destino]
                #print(aeropuerto_origen.obtener_codigo(),aeropuerto_destino.obtener_codigo())
                grafo.agregar_arista(aeropuerto_origen, aeropuerto_destino, (tiempo, precio, cant_vuelos))
    
    except IOError:
        print(f"No se pudo abrir {vuelos}")

def validar_parametros(comando, parametros):
    cantidad_parametros = {
        "camino_mas": 3, 
        "camino_escalas": 2,
        "mas_importante": 1,
        "nueva_aerolinea": 1,
        "itinerario": 1, 
        "exportar_kml": 1 
    }
    
    return cantidad_parametros[comando] == len(parametros)

def obtener_heap_centrales(grafo):
    heap = heapq.Heap()
    for elem in grafo:
        heap.heappush(elem)
    return heap

def parsear_datos_kml(cadena):
    return cadena.split(" -> ")