import numpy as np
import pandas as pd
import vitaldb
import time

def obtener_nombres_columnas(csv_path):
    df = pd.read_csv(csv_path)
    # Excluye la primera columna y devuelve el resto de los nombres
    columnas = list(df.columns[1:])
    return columnas

def calcular_intervalos_tiempo(csv_path):
    # Leer el archivo CSV
    df = pd.read_csv(csv_path)
    # Calcular la diferencia entre timestamps consecutivos
    df['time'] = df['time'].diff()
    # Calcular la media de los intervalos (excluyendo el primer NaN)
    # Usamos dropna para evitar el NaN inicial y cualquier otro NaN
    mean_interval = df['time'].iloc[1:].dropna().mean()
    # Devolver la media como float
    return float(mean_interval)

time_diff = calcular_intervalos_tiempo('resultado_algoritmos.csv')
print(f"Intervalo de tiempo promedio entre muestras: {time_diff} segundos")
tipos_valores = obtener_nombres_columnas('resultado_algoritmos.csv')

algoritmos_vital = vitaldb.read_csv('resultado_algoritmos.csv', track_names=tipos_valores, exclude=None, interval=time_diff)
algoritmos_vital.to_vital('algoritmos.vital', compresslevel=1)
