
import pandas as pd
import subprocess
import os
from datetime import datetime

VITALRECORDER_EXE = "./Vital.exe"  # ajusta la ruta

def open_in_vitalrecorder(vital_path: str):
    if not os.path.isfile(vital_path):
        print(f"Aviso: no existe el archivo {vital_path}")
        return None
    return subprocess.Popen([VITALRECORDER_EXE, vital_path])


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


import pandas as pd
import os


def merge_selected_csv(names, directory, output):
    """
    names: lista de strings con el nombre de cada CSV SIN la extensión .csv
           p.ej. ["ShockIndex", "DrivingPressure"]
    directory: carpeta donde están los CSV
    output: nombre del CSV de salida
    """
    merged_df = None

    for name in names:
        file = os.path.join(directory, f"{name}.csv")

        if not os.path.isfile(file):
            print(f"Aviso: no se encontró el archivo {file}, se omite.")
            continue

        col_name = name
        df = pd.read_csv(file)

        if len(df.columns) < 2:
            print(f"Aviso: {file} no tiene al menos 2 columnas, se omite.")
            continue

        # Asegurarse de que esté ordenado por tiempo
        df = df.sort_values("time")

        second_col = df.columns[1]
        df = df.rename(columns={second_col: col_name})

        if merged_df is None:
            merged_df = df
        else:
            # merged_df y df deben estar ordenados por 'time'
            merged_df = merged_df.sort_values("time")
            df = df.sort_values("time")

            merged_df = pd.merge_asof(
                merged_df,
                df,
                on="time",
                direction="backward"  # toma el último valor conocido hacia atrás
            )

    if merged_df is not None:
        # Rellenar huecos con el último valor observado
        merged_df = merged_df.ffill()  # last observation carried forward
        merged_df.to_csv(output, index=False)
        print(f"Fichero fusionado guardado en: {output}")
    else:
        print("No se pudieron fusionar CSV (ningún archivo válido).")


