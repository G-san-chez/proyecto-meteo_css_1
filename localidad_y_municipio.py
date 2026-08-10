class Localidad:
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

class Municipio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_localidades = []  # Guarda objetos Localidad

    def agregar_localidad(self, localidad):
        self.lista_localidades.append(localidad)