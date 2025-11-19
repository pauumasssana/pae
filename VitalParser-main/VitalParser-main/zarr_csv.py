import zarr
import pandas as pd

def zarr_signal_to_csv(zarr_path, signal_name, output_csv):
    zroot = zarr.open(zarr_path, mode='r')  # <--- Cambiado!
    base = f"signals/Intellivue/{signal_name}"
    timestamps = zroot[f"{base}/time_ms"][:]
    values = zroot[f"{base}/value"][:]
    df = pd.DataFrame({'timestamp': timestamps, 'value': values})
    df.to_csv(output_csv, index=False)
    return df.head()

# Ejemplo:
zarr_signal_to_csv('test_alg.zarr', 'ABP_HR', 'abp_hr_signal.csv')
