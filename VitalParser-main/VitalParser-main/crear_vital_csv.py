import numpy as np
import pandas as pd
import vitaldb
import time

def obtener_nombres_columnas(csv_path):
    df = pd.read_csv(csv_path)
    # Excluye la primera columna y devuelve el resto de los nombres
    columnas = list(df.columns[1:])
    return columnas

tipos_valores = obtener_nombres_columnas('resultado_algoritmos.csv')

algoritmos_vital = vitaldb.read_csv('resultado_algoritmos.csv', track_names=tipos_valores, exclude=None, interval=0.005)
algoritmos_vital.to_vital('algoritmos.vital', compresslevel=1)
