# Airports-System
This project implements a system to manage and analyze flight routes between airports using graph data structures and algorithms. The system provides functionalities for calculating optimal routes based on different criteria such as cost, travel time, and number of layovers. Additionally, it allows the identification of the most important airports based on their centrality in the network.

# Commands
- **`camino_mas barato|rapido <origen> <destino>`**: Finds the cheapest or fastest route between two cities. Example:
```
  camino_mas rapido,San Diego,New York
  SAN -> JFK
```
- **`camino_escalas <origen> <destino>`**: Finds the route with the fewest layovers between two cities. Example:
```
  camino_escalas San Diego,New York
  SAN -> JFK
```
- **`centralidad <n>`**: Displays the top `n` most important airports based on their centrality. Example:
```
  centralidad 5
  ATL, ORD, LAX, DFW, DEN
```
- **`nueva_aerolinea <output_file>`**: Exports the optimized routes for a new airline to the specified output file.
- **`itinerario <itinerary_file>`**: Plans a cultural itinerary by visiting specified cities in a particular order.
- **`exportar_kml <output_file>`**: Exports the last calculated route to a KML file.



# Usage
```
./flycombi aeropuertos.csv vuelos.csv
```
