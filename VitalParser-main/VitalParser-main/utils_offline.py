
import pandas as pd
import subprocess
import os
from datetime import datetime

VITALRECORDER_EXE = "./Vital.exe"  # ajusta la ruta

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


def trim_algorithms_csv_by_time(
    csv_in: str,
    csv_out: str,
    start_dt: datetime,
    end_dt: datetime,
    *,
    unix_unit: str = "s",   # OJO: "s" si time está como 1761200453.64
):
    if not os.path.isfile(csv_in):
        print(f"Aviso: no existe el archivo {csv_in}.")
        return

    df = pd.read_csv(csv_in)

    if "time" not in df.columns:
        print(f"Aviso: {csv_in} no tiene columna 'time'. Columnas: {df.columns.tolist()}")
        return

    # Asegurar numérico
    df["time"] = pd.to_numeric(df["time"], errors="coerce")

    print("Primeras filas del CSV:")
    print(df.head())

    # datetime -> segundos Unix
    start_ts = start_dt.timestamp()
    end_ts = end_dt.timestamp()

    # Ajustar a unidad real de la columna
    if unix_unit == "ms":
        start_ts *= 1000.0
        end_ts *= 1000.0

    print(f"start_dt = {start_dt} -> {start_ts}")
    print(f"end_dt   = {end_dt} -> {end_ts}")
    print(f"Rango 'time' en CSV: min={df['time'].min()}, max={df['time'].max()}")

    mask = (df["time"] >= start_ts) & (df["time"] <= end_ts)
    df_trimmed = df.loc[mask].copy()

    print(f"Filas totales: {len(df)}, filas dentro de rango: {len(df_trimmed)}")

    if df_trimmed.empty:
        print("Aviso: ningún dato dentro del rango de tiempo especificado.")
        return

    df_trimmed.to_csv(csv_out, index=False)
    print(f"CSV recortado guardado en: {csv_out}")

from datetime import datetime

def datetime_to_unix(dt: datetime, unit: str = "s") -> float:
    """
    Convierte un datetime a Unix timestamp.

    unit:
      - "s"  -> segundos (float)
      - "ms" -> milisegundos
      - "us" -> microsegundos
    """
    ts = dt.timestamp()  # segundos desde epoch, con decimales

    if unit == "s":
        return ts
    elif unit == "ms":
        return ts * 1000.0
    elif unit == "us":
        return ts * 1_000_000.0
    else:
        raise ValueError("unit must be 's', 'ms' or 'us'")
    
def open_in_vitalrecorder(vital_path: str):
    if not vital_path or not os.path.isfile(vital_path):
        print(f"Aviso: no existe el archivo {vital_path}, no se puede abrir en VitalRecorder.")
        return
    try:
        subprocess.Popen([VITALRECORDER_EXE, vital_path])
        print(f"Abierto en VitalRecorder: {vital_path}")
    except Exception as e:
        print(f"Error al abrir VitalRecorder con {vital_path}: {e}")

