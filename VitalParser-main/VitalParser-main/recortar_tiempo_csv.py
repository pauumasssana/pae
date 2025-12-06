import pandas as pd
import time

def recortar_csv_por_tiempo(archivo_entrada, archivo_salida,
                            inicio_ts, fin_ts, columna_tiempo='time'):
    # Leer CSV
    df = pd.read_csv(archivo_entrada)

    # Asegurarse de que la columna time es numérica
    df[columna_tiempo] = pd.to_numeric(df[columna_tiempo], errors='coerce')

    # Filtrar por rango de timestamps
    df_filtrado = df[(df[columna_tiempo] >= inicio_ts) &
                     (df[columna_tiempo] <= fin_ts)]

    # Guardar resultado
    df_filtrado.to_csv(archivo_salida, index=False)
    print(f"Archivo recortado guardado en {archivo_salida}")

# Ejemplo:
# recortar_csv_por_tiempo('datos.csv', 'datos_recortados.csv', 1700000000, 1700003600)

