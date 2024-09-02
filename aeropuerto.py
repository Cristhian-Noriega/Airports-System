CIUDAD = 0
CODIGO = 1
LATITUD = 2
LONGITUD = 3

class Aeropuerto():
    def __init__(self, lista):
        self.datos = lista

    def __str__(self):
        return f"Ciudad: {self.datos[CIUDAD]}, Codigo: {self.datos[CODIGO]}, Latitud: {self.datos[LATITUD]}, Longitud: {self.datos[LONGITUD]}"

    def obtener_ciudad(self):
        return self.datos[CIUDAD]
    
    def obtener_codigo(self):
        return self.datos[CODIGO]
    
    def obtener_latitud(self):
        return self.datos[LATITUD]
    
    def obtener_longitud(self):
        return self.datos[LONGITUD]
    
   