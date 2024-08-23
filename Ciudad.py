import math
class Ciudad:
    def __init__(self, name, weather, tAttraction, tActivities, lat, lon):
        self.name = name
        self.weather = weather
        self.tAttraction = tAttraction
        self.tActivities = tActivities
        self.lat = lat
        self.lon = lon

    def distancia(self, otra_ciudad):
        # Distancia euclidiana entre dos ciudades basada en sus coordenadas geográficas
        return math.sqrt((self.lat - otra_ciudad.lat) ** 2 + (self.lon - otra_ciudad.lon) ** 2)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)