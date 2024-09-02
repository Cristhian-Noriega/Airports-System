#!/usr/bin/python3

import sys
import auxiliares as aux
import comandos as cmd
from grafo import Grafo
    
def main(aeropuertos, vuelos):
    vertices, dict_aeropuertos, dict_ciudades = aux.cargar_aeropuertos(aeropuertos)
    grafo = Grafo(False, vertices)
    aux.cargar_vuelos(grafo, vuelos, dict_aeropuertos)
    comandos = cmd.cargar_comandos()
    pila_comandos = []
    for entrada in sys.stdin:
        input = parsear_entrada(entrada)
        comando = input[0]
        parametros = input[1:]
       
        if comandos.get(comando) is not None:
            msg = comandos[comando](grafo, parametros, dict_ciudades, dict_aeropuertos, pila_comandos)
            if msg != "":
                print(msg)

def parsear_entrada(entrada):
    comando = ""
    parametros = ""
   
    for i, caracter in enumerate(entrada):
        if caracter == " ":
            comando = entrada[:i]
            parametros = entrada[i+1:]
            break
    
    parametros = parametros.rstrip().split(",")
    comando = [comando.rstrip()]
    return comando + parametros

if __name__ ==  '__main__':
    aeropuertos = sys.argv[1]
    vuelos = sys.argv[2]
    main(aeropuertos, vuelos)