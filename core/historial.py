import pandas as pd

class Historial:
    def __init__(self, columnas):
        # Generamos una tabla de manera dinamica, y com las columnas exactas
        self.columnas = columnas
        self.datos = {col: [] for col in columnas}
    # Agrega de forma segura los valores a las listas correspondientes
    def agregar(self, fila):
        for col in self.columnas:
            self.datos[col].append(fila.get(col,None))
    # Devuelve los datos crudos
    def obtener_datos(self):
        return self.datos
    # Devuelve los datos en formato Pandas con una cantidad de decimales especifica
    def obtener_dataframe(self, decimales=6):
        df = pd.DataFrame(self.datos)
        return df.style.format(f"{{:.{decimales}f}}")