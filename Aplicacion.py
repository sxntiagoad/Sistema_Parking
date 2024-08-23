import tkinter as tk
from tkinter import messagebox
from Ciudad import Ciudad
from Grafo import Grafo
import DataCenter

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Ruta Personalizada")

        frame = tk.Frame(root, padx=20, pady=20)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Selecciona tu punto de partida:", anchor="w").grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.grafo = Grafo().inicializar_grafo(DataCenter.ciudades_datos, DataCenter.aristas_datos)
        self.ciudades = self.grafo.getAllCities()
        #menu desplegable
        if self.ciudades:
            self.ciudad_seleccionada = tk.StringVar(root)
            self.ciudad_seleccionada.set(self.ciudades[0].name)

            self.menu_desplegable = tk.OptionMenu(frame, self.ciudad_seleccionada, *[ciudad.name for ciudad in self.ciudades])
            self.menu_desplegable.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            self.menu_desplegable.config(width=40)
        #los labels antes de los entrys para que el usuario sepa que ingresara
        tk.Label(frame, text="Clima preferido:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Label(frame, text="Atractivo turístico:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        tk.Label(frame, text="Actividades:").grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.clima_entry = tk.Entry(frame)
        self.atractivo_entry = tk.Entry(frame)
        self.actividades_entry = tk.Entry(frame)

        self.clima_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.atractivo_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.actividades_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(frame, text="¿Estás buscando la ruta más óptima en cuanto a km?").grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.ruta_optima_var = tk.BooleanVar()
        self.ruta_optima_var.set(False)

        tk.Button(frame, text="Sí", command=lambda: self.set_ruta_optima(True)).grid(row=6, column=0, padx=10, pady=10)
        tk.Button(frame, text="No", command=lambda: self.set_ruta_optima(False)).grid(row=6, column=1, padx=10, pady=10)

        tk.Button(frame, text="Buscar Destinos", command=self.buscar_destinos).grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def set_ruta_optima(self, valor):  #esto obtiene lo que el usuario ingreso, para saber que proceso realizar
        self.ruta_optima_var.set(valor)

    def getRecomendaciones(self): #accede a los entrys para saber que ingreso el usuario y llama la fun para recomendar ciudades en base a sus pref
        clima = int(self.clima_entry.get())
        atractivo = self.atractivo_entry.get()
        actividades = self.actividades_entry.get()

        preferencias = {
            'clima': clima,
            'atractivo_turistico': atractivo,
            'actividades': actividades
        }
        #obtenemos recomendaciones llamando a la funcion de la clase grafo
        #filtra la lista de todas las recomendaciones, para que no se incluya la ciudad del punto destino
        recomendaciones = self.grafo.recomendar_destinos(preferencias)
        ciudad_seleccionada = self.ciudad_seleccionada.get() #con la fun ciudad_seleccionada sabe cual es la ciudad del punto de destino
        recomendaciones_filtradas = [ciudad for ciudad in recomendaciones if ciudad.name != ciudad_seleccionada]

        return recomendaciones_filtradas

    def buscar_destinos(self):
        try:
            clima = int(self.clima_entry.get())
            atractivo = self.atractivo_entry.get()
            actividades = self.actividades_entry.get()

            preferencias = {
                'clima': clima,
                'atractivo_turistico': atractivo,
                'actividades': actividades
            }

            punto_partida = self.ciudad_seleccionada.get()
            punto_partida_ciudad = next((ciudad for ciudad in self.ciudades if ciudad.name == punto_partida), None)
            if punto_partida_ciudad is None:
                messagebox.showerror("Error", "La ciudad de partida seleccionada no es válida.")
                return

            recomendaciones_filtradas = self.getRecomendaciones()
            if self.ruta_optima_var.get(): #si al usuario aparte de sus preferencias si quisiera tomar el camino mas optimo
                if recomendaciones_filtradas:
                    rutas_optimas = []
                    for destino_ciudad in recomendaciones_filtradas:
                        ruta = self.grafo.a_star(punto_partida_ciudad, destino_ciudad) #usa a_estrella
                        if ruta:
                            ruta_str = " -> ".join([f"{ciudad.name}" for ciudad in ruta])
                            rutas_optimas.append(f"Ruta a {destino_ciudad.name}: {ruta_str}")

                    if rutas_optimas:
                        resultados = "\n\n".join(rutas_optimas)
                        messagebox.showinfo("Rutas Óptimas", f"Las rutas óptimas son:\n{resultados}")
                    else:
                        messagebox.showinfo("Rutas Óptimas", "No se encontraron rutas óptimas.")
                else:
                    messagebox.showinfo("Recomendaciones",
                                        "No se encontraron destinos que coincidan con las preferencias.")
            else: #si solo le interesan sus preferencias y no le interesa escoger el camino mas optimo usa BFS que puede ser menos efectivo
                if recomendaciones_filtradas:
                    rutas = []
                    for destino_ciudad in recomendaciones_filtradas:
                        ruta = self.grafo.bfs(punto_partida_ciudad, destino_ciudad)
                        if ruta:
                            ruta_str = " -> ".join([f"{ciudad.name}" for ciudad in ruta])
                            rutas.append(f"Ruta a {destino_ciudad.name}: {ruta_str}")

                    if rutas:
                        resultados = "\n\n".join(rutas)
                        messagebox.showinfo("Rutas", f"Las rutas encontradas son:\n{resultados}")
                    else:
                        messagebox.showinfo("Rutas", "No se encontraron rutas.")
                else:
                    messagebox.showinfo("Recomendaciones",
                                        "No se encontraron destinos que coincidan con las preferencias.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para el clima.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
