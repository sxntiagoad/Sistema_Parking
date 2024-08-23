import heapq
import math
from Ciudad import Ciudad
from Arista import Arista

class Grafo:
    def __init__(self):
        self.adjacents = {}  # diccionario para guardar las ciudades

    def agregar_ciudad(self, ciudad):
        if ciudad not in self.adjacents:  # asegura que la ciudad no esté ya en el grafo
            self.adjacents[ciudad] = []

    def agregar_arista(self, origen, destino, distancia):
        if origen in self.adjacents and destino in self.adjacents:
            self.adjacents[origen].append(Arista(destino, distancia))
            self.adjacents[destino].append(Arista(origen, distancia))
    #para calcular distancias y usarlas al momento de inicializar el grafo para sus aristas
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Radio de la Tierra en kilómetros
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def inicializar_grafo(self, ciudades_datos, aristas_datos):
        nombre_a_ciudad = {}
        for ciudad_datos in ciudades_datos:
            ciudad = Ciudad(*ciudad_datos)
            nombre_a_ciudad[ciudad.name] = ciudad
            self.agregar_ciudad(ciudad)

        for (nombre_origen, nombre_destino) in aristas_datos:
            ciudad_origen = nombre_a_ciudad.get(nombre_origen)
            ciudad_destino = nombre_a_ciudad.get(nombre_destino)
            if ciudad_origen and ciudad_destino:
                distancia = self.haversine(ciudad_origen.lat, ciudad_origen.lon, ciudad_destino.lat, ciudad_destino.lon)
                self.agregar_arista(ciudad_origen, ciudad_destino, distancia)

        return self

    def obtener_adyacentes(self, ciudad):
        return self.adjacents.get(ciudad, [])

    def getAllCities(self):
        return list(self.adjacents.keys())

    #algoritmo para recomendar destinos
    def recomendar_destinos(self, preferencias):
        resultados = []
        for ciudad in self.adjacents.keys():
            if (abs(preferencias['clima'] - ciudad.weather) <= 1 and
                    (preferencias['atractivo_turistico'].lower() in ciudad.tAttraction.lower()) and
                    (preferencias['actividades'].lower() in ciudad.tActivities.lower())):
                resultados.append(ciudad)
        return resultados
    #en caso de que no necesite el camino mas corto y se quiera enfocar en las preferencias
    def bfs(self, inicio, meta):
        queue = [(inicio, [inicio])]
        visitados = set()

        while queue:
            (current, path) = queue.pop(0)
            if current in visitados:
                continue
            visitados.add(current)

            for arista in self.adjacents[current]:
                if arista.destino in visitados:
                    continue
                if arista.destino == meta:
                    return path + [arista.destino]
                queue.append((arista.destino, path + [arista.destino]))

        return None
    #para encontrar el camino mas efectivo
    def a_star(self, inicio, meta):
        open_set = []
        heapq.heappush(open_set, (0, inicio))
        came_from = {}
        g_score = {ciudad: float('inf') for ciudad in self.adjacents}
        g_score[inicio] = 0
        f_score = {ciudad: float('inf') for ciudad in self.adjacents}
        f_score[inicio] = self.haversine(inicio.lat, inicio.lon, meta.lat, meta.lon)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == meta:
                total_path = [current]
                while current in came_from:
                    current = came_from[current]
                    total_path.append(current)
                return total_path[::-1]

            for arista in self.adjacents[current]:
                tentative_g_score = g_score[current] + arista.distancia
                if tentative_g_score < g_score[arista.destino]:
                    came_from[arista.destino] = current
                    g_score[arista.destino] = tentative_g_score
                    f_score[arista.destino] = g_score[arista.destino] + self.haversine(arista.destino.lat, arista.destino.lon, meta.lat, meta.lon)
                    heapq.heappush(open_set, (f_score[arista.destino], arista.destino))

        return None
