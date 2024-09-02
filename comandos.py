import biblioteca 
import auxiliares as aux 
import csv 
import aeropuerto
import random
     
def cargar_comandos():
    return {
        "camino_mas": camino_mas, 
        "camino_escalas": escalas,
        "centralidad": mas_importante,
        "nueva_aerolinea": nueva_aerolinea,
        "itinerario": itirenario_cultural, 
        "exportar_kml": exportar_a_kml 
    }

def camino_mas(grafo, parametros, dict_ciudades, dict_aeropuertos, pila):
    if not aux.validar_parametros("camino_mas", parametros):
        return "Los parametros son invalidos"
    
    tipo, origen, destino = parametros
    camino_minimo = biblioteca.camino_minimo(grafo, origen, destino, tipo, dict_ciudades)
    
    if camino_minimo is None:
        return "No se encontro un camino"
    
    else:
        camino = " -> ".join(camino_minimo)
        pila.append(camino)
        return camino

def escalas(grafo, parametros, dict_ciudades, dict_aeropuertos, pila):
    if not aux.validar_parametros("camino_escalas", parametros):
        return "Los parametros son invalidos"
    
    origen, destino = parametros
    camino_minimo = biblioteca.camino_minimo_escalas(grafo, origen, destino, dict_ciudades)
    
    if camino_minimo is None:
        return "No se encontro un camino"
    else:
        camino = " -> ".join(camino_minimo)
        pila.append(camino)
        return camino

def mas_importante(grafo, parametros, dict_ciudades, dict_aeropuertos, pila):
    if not aux.validar_parametros("mas_importante", parametros):
        return "Los parametros son invalidos"
    
    centrales = biblioteca.centralidad(grafo)
    lista = []
    cantidad = int(parametros[0])
    centrales_ordenados = sorted(centrales.items(), key=lambda x:x[1])[::-1]
    for i, aeropuerto in enumerate(dict(centrales_ordenados)):
        if i < cantidad:
            lista.append(aeropuerto.obtener_codigo())
    
    res = ", ".join(lista)
    return res
     
def nueva_aerolinea(grafo, parametros, dict_ciudades, dict_aeropuertos, pila):
    if not aux.validar_parametros("nueva_aerolinea", parametros):
        return "Los parametros son invalidos"
    
    aeropuertos = biblioteca.mst_prim(grafo)
    rutas = biblioteca.obtener_vuelos(aeropuertos)
    ruta_archivo = parametros[0]
    
    with open(ruta_archivo, "w") as archivo:
        writer = csv.writer(archivo)
        writer.writerows(rutas)

    return "OK"  

def itirenario_cultural(grafo, parametros, dict_ciudades, dict_aeropuertos, pila):
    if not aux.validar_parametros("itinerario", parametros):
        return "Los parametros son invalidos"
    
    ciudades = []
    
    with open(parametros[0]) as archivo:
        itinerario = csv.reader(archivo, delimiter=",")
        for linea in itinerario:
            ciudades.append(linea)
    
    grafo_itinerario = biblioteca.obtener_grafo_itinerario(ciudades)
    itinerario = biblioteca.orden_topologico(grafo_itinerario)
    print(", ".join(itinerario))
    aeropuerto_salida = None
    
    for i in range(len(itinerario)):
        if i + 1 == len(itinerario):
            break
        
        camino = biblioteca.camino_minimo_itinerario(grafo, itinerario[i], itinerario[i+1], dict_ciudades, aeropuerto_salida)
        aeropuerto_salida = camino[len(camino)-1]
        camino = " -> ".join(camino)
        print(camino) 
   
    return "" 

def exportar_a_kml(grafo, parametros, dict_ciudades, dict_aeropuertos, pila):
    if not aux.validar_parametros("exportar_kml", parametros):
        return "Los parametros son invalidos"
    
    if len(pila) == 0:
        return "No hay datos para exportar"
    
    ruta_archivo = parametros[0]
    datos = aux.parsear_datos_kml(pila.pop())
    aeropuertos = []
    
    with open(ruta_archivo, "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f'<kml xmlns="http://earth.google.com/kml/2.1">\n')
        f.write("<Document>\n")    
        f.write(f"<name>{ruta_archivo.split('.')[0]}</name>\n")
        f.write("\n")
        for dato in datos:
            aeropuerto = dict_aeropuertos[dato]
            aeropuertos.append(aeropuerto)
            
            f.write("<Placemark>\n")
            f.write(f"<name>{aeropuerto.obtener_codigo()}</name>\n")
            f.write(f"<Point>\n")
            f.write(f"<coordinates>{aeropuerto.obtener_longitud()}, {aeropuerto.obtener_latitud()}</coordinates>\n")
            f.write(f"</Point>\n")
            f.write("</Placemark>\n")
            f.write("\n")
            
        for i in range(len(aeropuertos)-1):
            act = aeropuertos[i]
            sig = aeropuertos[i+1]
            if i == len(aeropuertos)-1:
                break
            f.write("<Placemark>\n")
            f.write("<LineString>\n")
            f.write(f"<coordinates>{act.obtener_longitud()}, {act.obtener_latitud()} {sig.obtener_longitud()}, {sig.obtener_latitud()}</coordinates>\n")
            f.write("</LineString>\n")
            f.write("</Placemark>\n")
            f.write("\n")
            
        
        f.write("</Document>\n")
        f.write("</kml>\n")
        
    return "OK"
        
        
