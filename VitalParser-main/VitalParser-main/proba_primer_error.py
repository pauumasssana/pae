import numpy as np
import pandas as pd
import vitaldb
import time

def create_segments(seed=42):
    np.random.seed(seed)

    # usar un timebase común en timestamp unix (segundos desde epoch)
    start_ts = time.time()

    # Segmento 1: señal continua (senoidal) muestreada a alta frecuencia (200 Hz)
    fs1 = 200.0
    dur1 = 5.0
    t1 = np.arange(0, dur1, 1.0/fs1)
    x1 = 1.2 * np.sin(2 * np.pi * 2.0 * t1) + 0.2 * np.random.randn(t1.size)  # 2 Hz + ruido gaussiano
    # convertir tiempos a unix timestamp
    df1 = pd.DataFrame({"time": start_ts + t1, "value": x1})
    df1.attrs["type"] = "continuous"
    df1.attrs["sampling"] = f"{fs1} Hz"

    # Segmento 2: datos discretos (cuentas por segundo) muestreados a baja frecuencia (1 Hz)
    fs2 = 1.0
    dur2 = 60  # 60 segundos
    t2 = np.arange(0, dur2, 1.0/fs2)
    x2 = np.random.poisson(lam=3.0, size=t2.size)  # conteos por segundo
    df2 = pd.DataFrame({"time": start_ts + t2, "value": x2})
    df2.attrs["type"] = "discrete_counts"
    df2.attrs["sampling"] = f"{fs2} Hz"

    # Segmento 3: mediciones cuantizadas tomadas a intervalos irregulares (muestreo no uniforme)
    dur3 = 30.0
    mean_interval = 0.5  # media de intervalo entre mediciones (s)
    intervals = np.random.exponential(scale=mean_interval, size=2000)
    t3 = np.cumsum(intervals)
    t3 = t3[t3 <= dur3]
    # señal base lenta con ruido, cuantizada a pasos de 0.5 (simula resolución limitada del sensor)
    v3_cont = 50.0 + 5.0 * np.sin(2 * np.pi * 0.05 * t3) + 0.5 * np.random.randn(t3.size)
    x3 = np.round(v3_cont * 2.0) / 2.0  # cuantización 0.5
    df3 = pd.DataFrame({"time": start_ts + t3, "value": x3})
    df3.attrs["type"] = "quantized_irregular"
    df3.attrs["sampling"] = "irregular (exp. inter-arrival)"

    # Guardar CSVs en el directorio actual
    df1.to_csv("segment1_continuous_200Hz.csv", index=False)
    df2.to_csv("segment2_counts_1Hz.csv", index=False)
    df3.to_csv("segment3_quantized_irregular.csv", index=False)

    summaries = {
        "segment1": {"type": df1.attrs["type"], "sampling": df1.attrs["sampling"], "rows": len(df1)},
        "segment2": {"type": df2.attrs["type"], "sampling": df2.attrs["sampling"], "rows": len(df2)},
        "segment3": {"type": df3.attrs["type"], "sampling": df3.attrs["sampling"], "rows": len(df3)},
    }
    return df1, df2, df3, summaries

if __name__ == "__main__":
    s1, s2, s3, info = create_segments()
    print("Segmentos generados y guardados como CSV:")
    for k, v in info.items():
        print(f"- {k}: tipo={v['type']}, muestreo={v['sampling']}, filas={v['rows']}")

    # Crear CSV con solo las dos columnas de valores (sin tiempos)
    vals_df = pd.concat([
        s1['value'].reset_index(drop=True),
        s2['value'].reset_index(drop=True)
    ], axis=1)
    vals_df.columns = ['segment1_value', 'segment2_value']
    vals_df.to_csv("segments_values_only.csv", index=False)
    print(f"CSV creado: segments_values_only.csv (filas={len(vals_df)})")

    # --- Alineación: asignar cada fila de segment2 a bloques de 200 filas de segment1 ---
    block = 200
    n1 = len(s1)
    s2_vals = s2['value'].values

    # repetir cada valor de segment2 'block' veces
    expanded = np.repeat(s2_vals, block)

    # ajustar la longitud al número de filas de segment1
    if expanded.size < n1:
        pad = np.full(n1 - expanded.size, np.nan)
        expanded = np.concatenate([expanded, pad])
    else:
        expanded = expanded[:n1]

    aligned_df = pd.DataFrame({
        'segment1_value': s1['value'].reset_index(drop=True),
        'segment2_aligned': expanded
    })
    aligned_df.to_csv("segments_aligned_every200.csv", index=False)
    print(f"CSV creado: segments_aligned_every200.csv (filas={len(aligned_df)})")

    # Crear un objeto vitaldb para leer los segmentos
    segment1 = vitaldb.read_csv('segment1_continuous_200Hz.csv', track_names='value', exclude=None, interval=0.005)
    segment2 = vitaldb.read_csv('segment2_counts_1Hz.csv', track_names='value', exclude=None, interval=0.005)
    segment3 = vitaldb.read_csv('segment3_quantized_irregular.csv', track_names='value', exclude=None, interval=0.005)

    print(f"Segmento 1 leído: {segment1}")
    print(f"Segmento 2 leído: {segment2}")
    print(f"Segmento 3 leído: {segment3}")


segment1 = vitaldb.read_csv('segment1_continuous_200Hz.csv', track_names='value', exclude=None, interval=0.005)

segment1.to_vital('segment1.vital', compresslevel=1)

segment2 = vitaldb.read_csv('segment2_counts_1Hz.csv', track_names='value', exclude=None, interval=1)

segment2.to_vital('segment2.vital', compresslevel=1)

segments = vitaldb.read_csv('segments_aligned_every200.csv', track_names=['segment1_value', 'segment2_aligned'], exclude=None, interval=0.005)


segments.to_vital('segments.vital', compresslevel=1)

##proba = vitaldb.read_vital('fdrbsau47_250702_173541.vital', track_names='SNUADC/ECG_II', exclude=None, header_only=False, maxlen=None)

